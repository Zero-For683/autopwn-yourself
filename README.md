# Hacker Dev Menu: Daily Python Projects for Offensive Security

This is my structured daily system for improving my Python skills and building practical offensive security tools. Each weekday has a dedicated theme, giving me repeatable, bite-sized coding tasks. Weekends are reserved for longer personal projects or reflection.

---

## Malware Monday

**Focus:** Payload crafting, obfuscation, and shellcode delivery  
Build the core primitives used in real-world offensive tooling and malware.

**Examples:**
- Encode payloads with base64, XOR, gzip, rot13
- Build Python stagers to drop and run payloads
- Simulate sandbox evasion (e.g., sleep loops, mouse movement checks)
- Recreate Metasploit/Cobalt Strike techniques in Python

**Repeatable by:**
Rebuilding known malware tricks and shellcode tools. Draw inspiration from:
- PayloadsAllTheThings
- Hacktricks
- Real malware analysis blogs
- Offesc courses

TL;DR - Build malware focusing on key principles we learn, endless source of content.

---

## Toolkit Tuesday

**Focus:** Build your own original utilities to support hacking workflows  
Make small, standalone tools you’d want in your personal toolkit.

**Examples:**
- Custom port scanner with color-coded output
- Hash identifier and formatter
- AD object lister via LDAP
- JWT inspector or decoder

**Repeatable by:**
Brainstorming common tasks that slow you down—and building something that fixes them. Focus on automation and convenience.


TL;DR - Build tools that are commonly used, but make them your own. 

---

## Web-Hacking Wednesday

**Focus:** Automate web vulnerability discovery and exploitation  
Use Python to build tools that help find and exploit bugs in real web apps.

**Examples:**
- URL crawlers and parameter fuzzers
- XSS/SSRF/CSRF scanners
- Auth bypass test scripts
- Burp-style PoC generators

**Repeatable by:**
Studying bug bounty writeups and PortSwigger Web Security Academy, then automating payload generation, fuzzing, or interaction.

It will take a while to have a "stack" for each bug class. Until then the "stacks" will be fairly weak

---

## Tool Rebuild Thursday

**Focus:** Rebuild popular tools to understand their internals  
Clone tools you use (or rely on) and recreate key functionality.

**Examples:**
- Rebuild part of ffuf to learn fuzzing
- Clone CrackMapExec’s SMB login scanner
- Emulate impacket scripts
- Reimplement `kerbrute` to brute-force usernames

**Repeatable by:**
Keeping a running list of tools you *use but don’t understand*. Pick one, dig into a feature, and rebuild it piece by piece.

TL;DR - Today is the day to study others who are better and not be a skid blindly using tools we dont understand

---

## Function Forge Friday

**Focus:** Take what you learned from the week (e.g., HTB, labs) and script it  
Turn a real-world technique into a single function or mini-script.

**Examples:**
- Function to parse `secretsdump` output into usable creds
- Payload encoder (Base64, XOR, etc.)
- Auto-exploit wrapper for a found CVE
- Script to automate reverse shell from a web RCE

**Repeatable by:**
Do any lab/HTB box. Pick one action that was tedious. Write a function that would’ve made it faster.

---

## Weekend Projects (Saturday & Sunday)

Reserved for:
- Larger personal tools
- Weekly or monthly project goals
- Experimentation and exploration
