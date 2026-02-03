from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def build_request(req_json: dict, injection_value: str, source: str, param: str):
    """
    Given a Burp-exported request JSON and a single injection_value,
    return a tuple (method, url, headers, data) ready for httpx.

    Only the specified source/param is replaced with injection_value,
    all other parameters are preserved exactly as-is.
    """
    method   = req_json.get("Method", "GET").upper()
    orig_url = req_json.get("URL", "")
    # copy headers so we don't mutate the original
    # copy headers so we don't mutate the original, drop content-length to let httpx set it correctly
    headers  = {k:v for k,v in req_json.get("Request Headers", {}).items() if k.lower() != "content-length"}
    data     = None

    if source == "url":
        # GET: replace one query parameter
        parsed = urlparse(orig_url)
        qs     = parse_qs(parsed.query, keep_blank_values=True)
        # override the one parameter
        qs[param] = [injection_value]
        new_qs = urlencode(qs, doseq=True)
        url    = urlunparse(parsed._replace(query=new_qs))

    elif source == "post":
        # POST: copy original form params to avoid in-place mutation
        body = {k: v.copy() for k, v in req_json.get("POST Parameters", {}).items()}
        # override only the target parameter
        body[param] = [injection_value]
        data = urlencode(body, doseq=True)
        headers["content-type"] = "application/x-www-form-urlencoded"
        url = orig_url

    else:
        raise ValueError(f"Unknown source {source}; expected 'url' or 'post'.")

    return method, url, headers, data
