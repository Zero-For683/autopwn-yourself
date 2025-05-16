# 🧠 Hacker Dev Menu: Daily Python Projects for Offensive Security

This is my structured daily system for improving my Python skills and building practical offensive security tools. Each weekday has a dedicated theme, giving me repeatable, bite-sized coding tasks. Weekends are reserved for longer personal projects or reflection.

---

## 🦠 Malware Monday

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
- Red Team Tradecraft
- Real malware analysis blogs

---

## 🛠️ Toolkit Tuesday

**Focus:** Building your own standalone tools  
Write the kinds of CLI utilities that support your offensive workflow.

**Examples:**
- Port scanners, DNS brute-forcers, directory brute tools
- Nmap XML parser or greppable output analyzer
- Hash dump parsers, NTLM formatter
- HTTP header extractors

**Repeatable by:**
Reimplementing tools like:
- `dirb`, `ffuf`, `enum4linux`, `hashcat`, `dnsenum`, etc.

---

## 🌐 Web-Hacking Wednesday

**Focus:** Automate web vulnerability discovery and exploitation  
Use Python to build tools that help find and exploit bugs in real web apps.

**Examples:**
- URL crawlers and parameter fuzzers
- XSS/SSRF/CSRF scanners
- Auth bypass test scripts
- Burp-style PoC generators

**Repeatable by:**
Studying bug bounty writeups and PortSwigger Web Security Academy, then automating payload generation, fuzzing, or interaction.

---

## 🔁 Tool Rebuild Thursday

**Focus:** Clone real hacking tools to learn how they work  
Pick a tool and rebuild part or all of it from scratch.

**Examples:**
- Simple Nmap clone (TCP/UDP scan with banner grabbing)
- Sublist3r or ffuf reimplementation
- SQLMap-lite or CrackMapExec-lite
- Whois, DNS, FTP, HTTP tools

**Repeatable by:**
Keeping a long list of tools you use regularly and recreating 10–20% of their functionality. Learn by building.

---

## ⚙️ Function Friday

**Focus:** Python fluency through utility function development  
Write useful helper functions and small classes to reinforce core Python skills.

**Examples:**
- Regex extractors for IPs, URLs, emails
- Argparse templates and CLI scaffolding
- File parsing (CSV, JSON, XML)
- Subprocess wrappers and logging utilities

**Repeatable by:**
Turning small challenges or manual tasks into reusable scripts. Use LeetCode problems as input and turn them into mini tools with real output.

---

## 🧱 Weekend Projects (Saturday & Sunday)

Reserved for:
- Larger personal tools
- Weekly or monthly project goals
- Experimentation and exploration
