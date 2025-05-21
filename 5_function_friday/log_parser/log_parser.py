import re
import argparse
from collections import Counter



def ip_grab():
    # Grabs IP address and puts it in a list with a coutner. 
    ip_list = []
    for ip in lines:
        ips = re.search(r'(\d{1,3}\.){3}(\d{1,3})', ip)
        ip_list.append(ips.group(0))
    
    cnt = Counter()
    for address in ip_list:
        cnt[address] += 1
    return cnt



def url_grab():
    # TODO: regex grab what part of the site they were trying to access
    intel = []
    for url in lines:
        endpoint = re.search(r'(GET|POST|PUT|DELETE|PATCH|OPTIONS|HEAD|TRACE|CONNECT) (/\S*)', url)
        group1 = endpoint.group(1)
        group2 = endpoint.group(2)
        intel.append([group1, group2])
    
    cnt = Counter()
    for counter in intel:
        cnt[tuple(counter)] += 1
    
    return cnt



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse HTTP log files and extract intel quickly")
    parser.add_argument('--log', required=True, help="The path to the actual log file")
    parser.add_argument('--ips', action='store_true', help="Show Ip address and how often they show up")
    parser.add_argument('--urls', action='store_true', help="show method/URL/procotol counts")

    args = parser.parse_args()

    lines = []
    with open(args.log, 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(line)

    
    if args.ips:
        ip_counts = ip_grab()
        print("\n📡 IP Address Counts:")
        for ip, count in ip_counts.items():
            entry = f"{ip}"
            print(f"{entry.ljust(50)} {count} hits")

    if args.urls:
        url_counts = url_grab()
        print("\n🌐 Method/URL/Protocol Counts:")
        for (method, url), count in url_counts.items():
            entry = f"{method} {url}:"
            print(f"{entry.ljust(50)} {count} hits")