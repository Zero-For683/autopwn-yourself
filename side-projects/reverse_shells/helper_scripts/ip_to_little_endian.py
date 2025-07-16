ip = input()

octets = map(int, ip.split("."))
little_endian = ''.join(f"{x:02x}" for x in reversed(list(octets)))

print(f"0x{little_endian}")