import json
import re
from difflib import SequenceMatcher
from urllib.parse import urlparse, urlencode, parse_qs
from datetime import datetime
import os

from http_client import HTTPClient  # Not strictly used here, but you might need it
                                    # if you want to create an HTTPClient instance inside

class SSRFUtils:
    """
    A utility class containing functions for SSRF testing and related operations.
    All methods are static for convenience, so you can call them directly on the class.
    """

    @staticmethod
    def url_param_payloads(file, http_client, payloads, allowed_host=None, evil_host=None):
        """
        Reads a JSON file containing request/response data, attempts SSRF payloads
        in the URL query parameters, and reports potential SSRF detections.
        """
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        url = data.get("URL")
        headers = data.get("Request Headers", {})
        method = data.get("Method", "GET").upper()
        original_html = data.get("HTML Content", "")
        post_params = data.get("POST Parameters", {})
        content_type = headers.get("content-type", "").lower()

        if not url:
            return

        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)

        for param, value_list in query_params.items():
            param_value_str = value_list[0] if value_list else ""

            if not SSRFUtils.is_potential_ssrf(param, param_value_str):
                continue

            counter = 0
            for payload in payloads:
                modified_payload = SSRFUtils.substitute_payload(payload, allowed_host, evil_host)
                if modified_payload is None:
                    continue

                temp_params = query_params.copy()
                temp_params[param] = [modified_payload]
                modified_query = urlencode(temp_params, doseq=True)
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{modified_query}"

                # For GET requests, we typically don’t need to send POST data,
                # but we *could* do so if the original was expecting it and had
                # a certain content type:
                encoded_params = None
                if "application/x-www-form-urlencoded" in content_type:
                    encoded_params = urlencode(post_params, doseq=True)
                elif "application/json" in content_type:
                    encoded_params = json.dumps(post_params)

                try:
                    timestamp = datetime.utcnow().isoformat()
                    SSRFUtils.log_payload_fire(timestamp, url, param, method, modified_payload, file)

                    response = http_client.send_request(method, test_url, headers)
                    if response and response.status_code == 200:
                        counter += 1
                        similarity_ratio = SSRFUtils.compare_html(original_html, response.text)
                        if similarity_ratio < 0.95:
                            print(f"🔥 SSRF detected on {url} | Param: {param} | Payload: {modified_payload}")
                        if counter > 3:
                            print(f"📌 3+ successful SSRF-like responses for '{param}', moving on.")
                            break
                except Exception as e:
                    print(f"❌ Error during request: {str(e)}")

    @staticmethod
    def post_param_payloads(file, http_client, payloads, allowed_host=None, evil_host=None):
        """
        Reads a JSON file containing request/response data, attempts SSRF payloads
        in the POST body, and reports potential SSRF detections.
        """
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        url = data.get("URL")
        headers = data.get("Request Headers", {})
        method = data.get("Method", "POST").upper()
        post_params = data.get("POST Parameters", {})
        original_html = data.get("HTML Content", "")
        content_type = headers.get("content-type", "").lower()

        if not url:
            return 

        if not post_params:
            return 

        if "content-length" in headers:
            del headers["content-length"]

        for param, value_list in post_params.items():
            param_value_str = value_list[0] if isinstance(value_list, list) and value_list else value_list

            if not SSRFUtils.is_potential_ssrf(param, param_value_str):
                continue

            counter = 0
            for payload in payloads:
                modified_payload = SSRFUtils.substitute_payload(payload, allowed_host, evil_host)
                if modified_payload is None:
                    continue 

                temp_params = post_params.copy()
                temp_params[param] = [modified_payload]

                if "application/x-www-form-urlencoded" in content_type:
                    encoded_params = urlencode(temp_params, doseq=True)
                elif "application/json" in content_type:
                    encoded_params = json.dumps(temp_params)
                else:
                    encoded_params = None

                if not encoded_params:
                    continue

                try:
                    timestamp = datetime.utcnow().isoformat()
                    SSRFUtils.log_payload_fire(timestamp, url, param, method, modified_payload, file)
                    response = http_client.send_request(method, url, headers, data=encoded_params)

                    if response and response.status_code == 200:
                        counter += 1
                        similarity_ratio = SSRFUtils.compare_html(original_html, response.text)
                        if similarity_ratio < 0.95:
                            print(f"🔥 SSRF detected on {url} | Param: {param} | Payload: {modified_payload}")
                        if counter > 3:
                            print(f"📌 3+ successful SSRF-like responses for '{param}', moving on.")
                            break
                except Exception as e:
                    print(f"❌ Error during request: {str(e)}")

    def header_payloads(file, http_client, payloads, allowed_host=None, evil_host=None):
        """
        Injects SSRF payloads into sensitive HTTP headers like Referer, User-Agent, etc.
        """
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        url = data.get("URL")
        headers = data.get("Request Headers", {}).copy()
        method = data.get("Method", "GET").upper()
        original_html = data.get("HTML Content", "")
        content_type = headers.get("content-type", "").lower()
        post_params = data.get("POST Parameters", {})

        if not url:
            return

        vulnerable_headers = ["referer", "user-agent", "x-forwarded-host", "host"]

        for header in vulnerable_headers:
            if header not in headers:
                continue

            for payload in payloads:
                modified_payload = SSRFUtils.substitute_payload(payload, allowed_host, evil_host)
                if modified_payload is None:
                    continue

                temp_headers = headers.copy()
                temp_headers[header] = modified_payload

                encoded_params = None
                if method == "POST":
                    if "application/x-www-form-urlencoded" in content_type:
                        encoded_params = urlencode(post_params, doseq=True)
                    elif "application/json" in content_type:
                        encoded_params = json.dumps(post_params)

                try:
                    timestamp = datetime.utcnow().isoformat()
                    SSRFUtils.log_payload_fire(timestamp, url, f"header: {header}", method, modified_payload, file)

                    response = http_client.send_request(method, url, headers=temp_headers, data=encoded_params)

                except Exception as e:
                    print(f"❌ Error testing header SSRF for '{header}': {str(e)}")

    # --------------------------------------------------------------------------
    # SSRF Helper Methods
    # --------------------------------------------------------------------------
    @staticmethod
    def is_potential_ssrf(param_name, param_value):
        """
        Checks if a parameter is likely to be vulnerable to SSRF by looking
        for certain keywords or a recognized URL scheme.
        """
        SSRF_KEYWORDS = [
            "url", "endpoint", "callback", "webhook", "stockApi",
            "imageUrl", "feed", "host", "dest", "uri", "path", "redir"
        ]
        URL_PATTERN = re.compile(r"(https?|ftp|file|dict|gopher|smb)://", re.IGNORECASE)

        # Check parameter name for known SSRF keywords
        if any(keyword.lower() in param_name.lower() for keyword in SSRF_KEYWORDS):
            return True

        # If the param value looks like a URL (scheme://)
        if URL_PATTERN.search(str(param_value)):
            return True
        


        return False

    @staticmethod
    def substitute_payload(payload, allowed_host=None, evil_host=None):
        requires_allowed = "{allowed.com}" in payload
        requires_evil = "{evil.com}" in payload

        # Rule 1: --allowed is set, --attacker is not → skip if {evil.com} appears
        if allowed_host and not evil_host and requires_evil:
            return None

        # Rule 2: --attacker is set, --allowed is not → skip if {allowed.com} appears
        if evil_host and not allowed_host and requires_allowed:
            return None

        # Rule 3: neither set → skip all payloads requiring replacement
        if not allowed_host and not evil_host and (requires_allowed or requires_evil):
            return None

        if requires_allowed and allowed_host:
            payload = payload.replace("{allowed.com}", allowed_host)
        if requires_evil and evil_host:
            payload = payload.replace("{evil.com}", evil_host)

        return payload

    @staticmethod
    def compare_html(original_html, new_html):
        """
        Compares two HTML pages (strings) and returns a similarity ratio.
        A lower ratio may indicate a different response, suggesting SSRF success.
        """
        if not original_html or not new_html:
            return 0

        ratio = SequenceMatcher(None, original_html, new_html).ratio()
        return ratio
    
    @staticmethod
    def log_payload_fire(timestamp, original_url, param, method, payload, json_file):
        parsed = urlparse(original_url)
        domain = parsed.netloc
        log_dir = os.path.join("requests_responses", domain)
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "log.txt")

        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{timestamp}] method={method} param='{param}' → {payload} || FILENAME: {json_file} \n")

