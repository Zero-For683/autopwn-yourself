import urllib.parse
import html
import base64

def url_encode(s: str) -> str:
    # Percent-encode every reserved/unsafe char
    return urllib.parse.quote(s, safe="")

def url_encode_plus(s: str) -> str:
    # Like quote(), but also encodes spaces as “+”
    return urllib.parse.quote_plus(s)

def double_url_encode(s: str) -> str:
    # Run percent-encode twice
    return urllib.parse.quote(url_encode(s), safe="")

def html_entity_encode(s: str) -> str:
    # Turn < into &#60;, > into &#62;, etc.
    return "".join(f"&#{ord(c)};" for c in s)

def html_escape(s: str) -> str:
    # Escape &, <, >, " and '
    return html.escape(s, quote=True)

def base64_encode(s: str) -> str:
    # Useful for data: URIs or JSON contexts
    return base64.b64encode(s.encode()).decode()