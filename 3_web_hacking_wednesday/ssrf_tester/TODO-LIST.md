
1. Detect SSRF via OAST:
    - Having the script automatically start a nc listener, and confirm SSRF based on nc finding anything


2. SSRF parser discrepancies
    - scheme confusion
    - slashes confusion
    - backslash confusion
    - URL encoded data confusion
    - scheme mixup
    - https://claroty.com/team82/research/exploiting-url-parsing-confusion

3. Fix the damn spider. 
    The spider I run against the target doesn't click on links or spider like it should. This makes it
    so that it misses request headers that we could be testing the site against for SSRF. 

    I need to refactor the spider so it does a better job at spidering the site, as fast as possible. 