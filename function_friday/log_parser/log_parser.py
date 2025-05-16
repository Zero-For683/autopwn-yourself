'''
Key problems I want to solve with this script:

What IPs accessed this server?

Which URLs did they hit, and how often?

Is one page getting hammered more than others?

Can I summarize this noisy log into something readable?
'''

import re


def ip_grab():
    # TODO: regex grab the IP address'
    with open('sample_access.log', 'r', encoding='utf-8') as f:
        read_data = f.read()
        print(read_data)

ip_grab()

def url_grab():
    # TODO: regex grab what part of the site they were trying to access
    return None


# TODO: summarize how often each url is getting hit

# TODO: quick TLDR summary of the site as it is