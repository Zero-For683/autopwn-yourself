https://medium.com/maxwell-cross-python-for-red-teaming/building-a-custom-c2-server-in-python-a-fresh-take-on-offensive-security-e3d8c09bc2ab
Made this rough-draft with this article, plan on adding my own functionality now that I understand how a C2 is supposed to work


TODO list:
    - Staged payload support (like meterpreter staged payloads) that downloads our full package to interact with our C2
    - Dedicated DB with list of pre-defined tasks to issue victims (file upload, download, etc)
    - Advanced sleep profiles (real AI-based "human behavior" models)
    - Make everything run in-memory
    - Dashboard to interact with our C2 (like msfconsole)