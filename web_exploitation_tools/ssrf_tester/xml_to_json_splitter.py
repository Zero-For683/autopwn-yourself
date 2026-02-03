import os
import json
import base64
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs

def decode_base64_if_needed(value, is_base64):
    if is_base64 == "true":
        return base64.b64decode(value).decode("utf-8", errors="replace")
    return value

def parse_headers(header_text):
    headers = {}
    for line in header_text.strip().splitlines():
        if ": " in line:
            key, val = line.split(": ", 1)
            headers[key.lower()] = val
    return headers

def burp_to_json(json_folder, xml_path):
    output_dir = json_folder
    os.makedirs(output_dir, exist_ok=True)

    tree = ET.parse(xml_path)
    root = tree.getroot()

    seen = set()
    file_counter = 1

    for idx, item in enumerate(root.findall(".//item")):
        try:
            url = item.findtext("url")
            method = item.findtext("method", default="GET")
            request_base64 = item.find("request").text.strip()
            request_is_base64 = item.find("request").attrib.get("base64", "false")
            request = decode_base64_if_needed(request_base64, request_is_base64)

            # Extract headers
            request_headers = {}
            if "\n" in request:
                request_lines = request.splitlines()
                request_line = request_lines[0]
                header_lines = request_lines[1:]
                request_headers = parse_headers("\n".join(header_lines))
            else:
                request_line = ""

            post_body = ""
            post_params = {}

            # Extract POST body if content-type is form-urlencoded
            if method == "POST":
                header_lines = request.splitlines()
                if "" in header_lines:
                    split_index = header_lines.index("")
                    post_body = "\n".join(header_lines[split_index + 1:]).strip()

                    content_type = request_headers.get("content-type", "").lower()
                    if "application/x-www-form-urlencoded" in content_type:
                        post_params = parse_qs(post_body)

            # Deduplication key: method + normalized path
            parsed_url = urlparse(url)

            static_exts = (".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".css", ".js", ".woff", ".ttf")
            if parsed_url.path.lower().endswith(static_exts):
                continue

            dedup_key = f"{method}:{parsed_url.path}"
            if dedup_key in seen:
                continue
            seen.add(dedup_key)

            # Parse response
            response = ""
            html_content = ""
            response_elem = item.find("response")
            if response_elem is not None:
                response_base64 = response_elem.text or ""
                response_is_base64 = response_elem.attrib.get("base64", "false")
                response = decode_base64_if_needed(response_base64, response_is_base64)
                html_content = response.split("\r\n\r\n", 1)[-1] if "\r\n\r\n" in response else ""

            # URL params
            url_params = parse_qs(parsed_url.query)

            response_headers = {}
            if "\n" in response:
                response_lines = response.splitlines()
                response_header_lines = response_lines[1:]  # skip status line
                response_headers = parse_headers("\n".join(response_header_lines))

            output = {
                "URL": url,
                "Method": method,
                "HTTP Version": "Unknown",
                "Request Headers": request_headers,
                "Response Headers": response_headers,
                "URL Parameters": url_params,
                "HTML Content": html_content.strip(),
                "POST Body": post_body,
                "POST Parameters": post_params
            }

            output_path = os.path.join(output_dir, f"request_{file_counter}.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=4)

            file_counter += 1

        except Exception as e:
            print(f"[!] Failed to process item {idx+1}: {e}")
