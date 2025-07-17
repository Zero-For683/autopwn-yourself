def ror13(x):
    return ((x >> 13) | (x << (32 - 13))) & 0xFFFFFFFF

def hash_ror13(name: bytes) -> int:
    h = 0
    for b in name:
        h = ror13(h)
        h = (h + b) & 0xFFFFFFFF
    return h

print(hex(hash_ror13(b"WSAGetLastError")))
