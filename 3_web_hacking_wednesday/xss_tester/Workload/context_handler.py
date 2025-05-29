from bs4 import BeautifulSoup


def classify_context(html_text: str, marker: str) -> str:
    """
    Examine html_text around `marker` and return one of:
      "html_data", "attribute", "js_string", "url", "css", or None
    """
    soup = BeautifulSoup(html_text, "html.parser")

    # 1) HTML Data: marker in a tag's text node
    for tag in soup.find_all():
        if tag.string and marker in tag.string:
            return "html_data"

    # 2) Attribute: marker in any attribute value
    for tag in soup.find_all():
        for attr_val in tag.attrs.values():
            vals = attr_val if isinstance(attr_val, (list, tuple)) else [attr_val]
            if any(isinstance(v, str) and marker in v for v in vals):
                return "attribute"

    # 3) JS String Literal: marker in a <script> block
    for script in soup.find_all("script"):
        if script.string and marker in script.string:
            return "js_string"

    # 4) URL context: marker in href or src attributes
    for tag in soup.find_all(href=True):
        if marker in tag["href"]:
            return "url"
    for tag in soup.find_all(src=True):
        if marker in tag["src"]:
            return "url"

    # 5) CSS context: marker in a style attr or inside a <style> block
    for tag in soup.find_all(style=True):
        if marker in tag.get("style", ""):
            return "css"
    for style in soup.find_all("style"):
        if style.string and marker in style.string:
            return "css"

    return None
