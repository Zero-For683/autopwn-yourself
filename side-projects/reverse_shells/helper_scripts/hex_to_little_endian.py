import socket
import binascii

# IP as string
ip = '192.168.1.244'

# Convert to packed binary format (big endian)
packed_ip = socket.inet_aton(ip)  # Result: b'\x7f\x00\x00\x01'

# Convert to integer (little endian) for pushing into a register
ip_hex_le = packed_ip[::-1].hex()  # Reverse the bytes
ip_int_le = int.from_bytes(packed_ip[::-1], byteorder='big')

print("Little-endian hex (for push): 0x" + ip_hex_le)
print("Integer to use in assembly: ", hex(ip_int_le))