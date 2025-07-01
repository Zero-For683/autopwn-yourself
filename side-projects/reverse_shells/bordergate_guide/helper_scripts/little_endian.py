import binascii
import argparse
 
def encodeCommand(command):
    result = "".join("{:02x}".format(ord(c)) for c in command)
    ba = bytearray.fromhex(result)
    ba.reverse()
    ba.hex()
 
    input = ba.hex()
    input = input[::-1]
    n = 16
 
    byte_list = [input[i:i+n] for i in range(0, len(input), n)]
    for x in reversed(byte_list):
        print("mov rax, 0x" + x[::-1])
        print("push rax;")
 
 
argParser = argparse.ArgumentParser()
argParser.add_argument("-t", "--text", help="text to encode", required=True)
args = argParser.parse_args()
encodeCommand(args.text)