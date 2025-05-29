import os
import json
import asyncio
import httpx
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from context_handler import classify_context
from payload_generator import generate_core_payloads
from encoding import base64_encode
from verifier import test_payloads
from request_builder import build_request

def find_injection_points(req_json: dict) -> dict:
    pts = {}
    if req_json.get("URL Parameters"):
        pts["url"] = list(req_json["URL Parameters"].keys())
    if req_json.get("POST Parameters"):
        pts["post"] = list(req_json["POST Parameters"].keys())
    return pts

def scan_requests(dirpath: str, marker: str):
    """
    Entry point called by main.py.
    Kicks off the asyncio loop.
    """
    print(f"[+] Testing XSS injection (marker={marker}) on all requests in '{dirpath}'")
    asyncio.run(_async_scan(dirpath, marker))

async def _async_scan(dirpath: str, marker: str):
    files = sorted(f for f in os.listdir(dirpath) if f.endswith(".json"))
    if not files:
        print(f"[!] No JSON requests found in {dirpath}")
        return

    limits = httpx.Limits(max_connections=5, max_keepalive_connections=2)
    async with httpx.AsyncClient(http2=True, limits=limits, follow_redirects=True) as client:
        for fname in files:
            path = os.path.join(dirpath, fname)
            with open(path, encoding="utf-8") as f:
                req_json = json.load(f)

            pts = find_injection_points(req_json)
            if not pts:
                print(f"[+] {fname} has no injectable parameters, skipping")
                continue

            print(f"[→] Scanning {fname}:")



            for source, params in pts.items():
                for param in params:
                    # 1) Marker probe (same as before)
                    print(f"    [debug] → Probing marker in {source} param '{param}'")
                    method, url, headers, data = build_request(req_json, marker, source, param)
                    try:
                        resp = await client.request(method, url, headers=headers, data=data)
                    except Exception as e:
                        print(f"    [debug] Request for marker in '{param}' failed: {e}")
                        continue

                    print(f"    [debug] Received {resp.status_code} for marker probe on '{param}'")
                    present = (marker in resp.text)
                    print(f"    [debug] Marker {'FOUND' if present else 'not found'} in response body for '{param}'")


                    if not present and source == "post":
                        view_url = headers.get("referer") or req_json["URL"]
                        print(f"    [debug] Checking referer view page {view_url} for '{param}'")
                        try:
                            view_resp = await client.get(view_url, headers=headers)
                            present = (marker in view_resp.text)
                            print(f"    [debug] Marker {'FOUND' if present else 'not found'} in view page for '{param}'")
                        except Exception as e:
                            print(f"    [debug] View-page check failed for '{param}': {e}")

                    # now your existing reflection logic...
                    if not present:
                        print(f"    [debug] → No reflection for '{param}', skipping core payloads")
                        continue

                    print(f"    [debug] !!! Marker reflected in '{param}' – firing core payloads")



##############

                    # 2) Reflection check (also same)
                    reflected_html = resp.text
                    reflected = (marker in reflected_html)
                    if not reflected and source == "post":
                        view_url = headers.get("referer") or req_json["URL"]
                        try:
                            view_resp = await client.get(view_url, headers=headers)
                            reflected_html = view_resp.text
                            reflected = (marker in reflected_html)
                        except Exception:
                            pass

                    if not reflected and "location" in resp.headers:
                        loc = resp.headers["location"]
                        if marker in loc:
                            next_url = httpx.URL(resp.url).join(loc)
                            try:
                                loc_resp = await client.get(str(next_url), headers=headers)
                                reflected_html = loc_resp.text
                                reflected = (marker in reflected_html)
                            except Exception:
                                pass

                    if not reflected:
                        # no marker => move on
                        continue

                    # 3) Generate & fire core payloads
                    ctx = classify_context(reflected_html, marker)
                    print(f"    [!] Marker reflected in {source} param '{param}' → context={ctx}")
                    extra = {}
                    # ... your existing context‐specific extra gathering here ...
                    core_payloads = generate_core_payloads(ctx, marker=marker, **extra)

                    # bail as soon as any core payload request fails
                    for p in core_payloads:
                        try:
                            m2, u2, h2, d2 = build_request(req_json, p, source, param)
                            _ = await client.request(m2, u2, headers=h2, data=d2)
                        except Exception as e:
                            print(f"        [!] Core payload request failed: {e}")
                            # skip verify_in_browser and go to next param
                            break
                    else:
                        # 4) Only if all core payloads sent successfully, verify in-browser
                        results = await test_payloads(req_json, core_payloads, source, param)
                        for payload, executed in results:
                            if not executed:
                                continue
                            ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                            print(f"{ts}  [XSS] {req_json['URL']}  → param='{param}'  payload={payload!r}")
                    # Done with this param
                    continue




