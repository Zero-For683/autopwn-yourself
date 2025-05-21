import unicodedata
import urllib.parse

class PayloadEncoder:
    def __init__(self, payloads):
        self.payloads = payloads

    def circle_alpha_unicode(self):
        unicode_dictionary = {
            **{chr(i): chr(0x24D0 + i - ord('a')) for i in range(ord('a'), ord('z') + 1)},  # Lowercase a-z
            **{chr(i): chr(0x24B6 + i - ord('A')) for i in range(ord('A'), ord('Z') + 1)},  # Uppercase A-Z
            **{chr(i): chr(0x24EA + i - ord('0')) for i in range(ord('0'), ord('9') + 1)}   # Digits 0-9
        }

        new_payloads = []
        for payload in self.payloads:
            scheme, rest = payload.split("://", 1) if "://" in payload else ("", payload)
            transformed_rest = "".join(unicode_dictionary.get(char, char) for char in rest)
            new_payloads.append(f"{scheme}://{transformed_rest}" if scheme else transformed_rest)

        self.payloads.extend(new_payloads)
        return self

    def fullwidth_unicode(self):
        mapping = {
            **{chr(i): chr(0xFF41 + i - ord('a')) for i in range(ord('a'), ord('z') + 1)},
            **{chr(i): chr(0xFF21 + i - ord('A')) for i in range(ord('A'), ord('Z') + 1)},
            **{'0': '０', '1': '１', '2': '２', '3': '３', '4': '４', '5': '５',
               '6': '６', '7': '７', '8': '８', '9': '９'}
        }

        new_payloads = []
        for payload in self.payloads:
            scheme, rest = payload.split("://", 1) if "://" in payload else ("", payload)
            transformed_rest = "".join(mapping.get(char, char) for char in rest)
            new_payloads.append(f"{scheme}://{transformed_rest}" if scheme else transformed_rest)

        self.payloads.extend(new_payloads)
        return self

    def browser_unicode(self):
        unicode_dictionary = {
            ':': '\uFE13',  '.': '\u3002', '[': '\uFE47',  ']': '\uFE48', '-': '\uFE63', '&': '\uFE60',
            ';': '\u037E', '_': '\uFE33', ',': '\uFE50',  '!': '\uFE15', "'": '\uFF07', '"': '\uFF02',
            '(': '\u207D',  ')': '\u207E', '{': '\uFE37',  '}': '\uFE38', '*': '\uFE61', '`': '\u1FEF',
            '+': '\u207A',  '=': '\u207C', '~': '\uFF5E', '$': '\uFE69', ' ': '\u00A0'
        }

        new_payloads = []
        for payload in self.payloads:
            scheme, rest = payload.split("://", 1) if "://" in payload else ("", payload)
            transformed_rest = "".join(unicode_dictionary.get(char, char) for char in rest)
            new_payloads.append(f"{scheme}://{transformed_rest}" if scheme else transformed_rest)

        self.payloads.extend(new_payloads)
        return self

    def escape_unicode(self):
        escaped_payloads = [
            "".join(f"\\u{ord(char):04X}" if ord(char) > 127 else char for char in payload)
            for payload in self.payloads
        ]
        self.payloads.extend(escaped_payloads)
        return self

    def url_encode_all(self):
        self.payloads.extend([urllib.parse.quote(payload, safe='') for payload in self.payloads])
        return self

    def url_encode_special(self):
        safe_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.payloads.extend([urllib.parse.quote(payload, safe=safe_chars) for payload in self.payloads])
        return self

    def double_url_encode_all(self):
        self.payloads.extend([
            urllib.parse.quote(urllib.parse.quote(payload, safe=''), safe='') for payload in self.payloads
        ])
        return self

    def double_url_encode_special(self):
        safe_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.payloads.extend([
            urllib.parse.quote(urllib.parse.quote(payload, safe=safe_chars), safe=safe_chars)
            for payload in self.payloads
        ])
        return self

    def get_payloads(self):
        return self.payloads
