def hash_api(name: str, key: int) -> int:
    h = 0
    for c in name:
        x = ord(c) ^ key
        if x == 0:
            break  # stop when char ^ key == 0 → char == key
        h = (h - x) & 0xFF
    return h

for api in ["LoadLibraryA", "socket", "connect", "recv"]:
    print(f"{api:<12} → hash: 0x{hash_api(api, 0xF8):02X}  (key=0xF8)")
    print(f"{api:<12} → hash: 0x{hash_api(api, 0xC0):02X}  (key=0xC0)")