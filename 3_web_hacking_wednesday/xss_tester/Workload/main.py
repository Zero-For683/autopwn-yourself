#!/usr/bin/env python3
import argparse
import os
import sys

from marker import scan_requests
from burp_to_py import burp_to_json

def parse_args():
    parser = argparse.ArgumentParser(description="XSS Tester")
    parser.add_argument("--burp", "-b",required=True,help="Path to Burp Suite exported XML")
    parser.add_argument("--out", "-o",default="burp_requests",help="Directory to write the converted JSON files")
    parser.add_argument("--marker", "-m", default="z0f863", help="Unique marker string to inject")
    return parser.parse_args()

def main():
    args       = parse_args()


    #####################################################################
    # Burpsuite to JSON ↓
    xml_path   = args.burp
    output_dir = args.out

    if not os.path.isfile(xml_path):
        print(f"[!] Burp XML not found: {xml_path}")
        sys.exit(1)

    print(f"[+] Converting '{xml_path}' → JSON requests in '{output_dir}'")

    burp_to_json(output_dir, xml_path)
    # Burpsuite to JSON ↑
    ######################################################################
    # Marker ↓
    marker = args.marker

    scan_requests(output_dir, marker)
    # Marker ↑
    ######################################################################



if __name__ == "__main__":
    main()
