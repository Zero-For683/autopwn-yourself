import os, json, asyncio, httpx
from datetime          import datetime
from context_handler   import classify_context
from payload_generator import generate_core_payloads
from verifier          import test_payloads
from request_builder   import build_request

'''
    Right now this is the file that strings everything together and handles the bare-bones logic. 

    It needs to be segmented and separated for readability, efficiency, and bloat.

    The only thing this file should be doing is passing the marker to our functions to handle. But as it's built, it'll be hard to re-work everything.
    '''


def find_injection_points(req_json: dict) -> dict: # Finds any parameters to inject into and puts them into a dict
    pts = {}
    if req_json.get("URL Parameters"):
        pts["url"] = list(req_json["URL Parameters"].keys())
    if req_json.get("POST Parameters"):
        pts["post"] = list(req_json["POST Parameters"].keys())
    return pts

def scan_requests(dirpath: str, marker: str): # dirpath is given from main.py
    """
    Entry point called by main.py.
    Kicks off the asyncio loop.
    """
    print(f"[+] Testing XSS injection (marker={marker}) on all requests in '{dirpath}'")
    asyncio.run(_async_scan(dirpath, marker))

async def _async_scan(dirpath: str, marker: str):
    files = sorted(f for f in os.listdir(dirpath) if f.endswith(".json")) # gets all of our .json files we exported
    if not files:
        print(f"[!] No JSON requests found in {dirpath}")
        return

    limits = httpx.Limits(max_connections=5, max_keepalive_connections=2)
    async with httpx.AsyncClient(http2=True, limits=limits, follow_redirects=True) as client:
        for fname in files: # Begin looping over all .json files outputted
            path = os.path.join(dirpath, fname)
            with open(path, encoding="utf-8") as f:
                req_json = json.load(f)

            pts = find_injection_points(req_json) # Finding all the places we can inject our marker into
            if not pts:
                print(f"[+] {fname} has no injectable parameters, skipping")
                continue

            print(f"[→] Scanning {fname}:")

            for source, params in pts.items(): # Looping over all possible inject spots
                for param in params: # Now looping over each parameter for markers
                    print(f"    [debug] → Probing marker in parameter: '{param}'")
                    method, url, headers, data = build_request(req_json, marker, source, param) # rebuilding the request and storing easy variables. 
                    try:
                        resp = await client.request(method, url, headers=headers, data=data) # Testing our marker
                    except Exception as e:
                        print(f"    [debug] Request for marker in '{param}' failed: {e}")
                        continue

                    print(f"    [debug] Received {resp.status_code} for marker probe on '{param}'")
                    present = (marker in resp.text)
                    print(f"    [debug] Marker {'FOUND' if present else 'not found'} in response body for '{param}'")


                    if not present and source == "post": # Different logic needed if it's a post request
                        view_url = headers.get("referer") or req_json["URL"] # Possibly dangerous to not include this with GET requests (GETs have redirects too)
                        try:
                            view_resp = await client.get(view_url, headers=headers)
                            present = (marker in view_resp.text) # Checks to see if our marker is in the original spot (incase we get redirected)
                            print(f"    [debug] Marker {'FOUND' if present else 'not found'} in view page for '{param}'")
                        except Exception as e:
                            print(f"    [debug] View-page check failed for '{param}': {e}")

                    # now your existing reflection logic...
                    if not present: # Checks for marker. If none then it moves onto the next parameter/json file
                        print(f"    [debug] → No reflection for '{param}', moving on")
                        continue

                    print(f"    [debug] !!! Marker reflected in '{param}' – firing core payloads") # This function is getting really long. It might be best to return something here and fire off another function in main.py


                    # 2) Reflection check (also same)
                    reflected_html = resp.text
                    reflected = (marker in reflected_html)
                    if not reflected and source == "post": # Second if statement to check for post redirects. Not sure why we need two here? Unecessary bloat if un-needed
                        view_url = headers.get("referer") or req_json["URL"]
                        try:
                            view_resp = await client.get(view_url, headers=headers)
                            reflected_html = view_resp.text
                            reflected = (marker in reflected_html)
                        except Exception:
                            pass

                    if not reflected and "location" in resp.headers: # Not sure what this bit of logic is for...
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
                    # Again, I think we should pass this point off to main.py and have the logic run in a separate function. I think this one is just getting so bloated
                    ctx = classify_context(reflected_html, marker)
                    print(f"    [!] Marker reflected in {source} param '{param}' → context={ctx}")
                    extra = {}
                    # ... your existing context‐specific extra gathering here ...
                    core_payloads = generate_core_payloads(ctx, marker=marker, **extra)

                    # bail as soon as any core payload request fails
                    for p in core_payloads:
                        try:
                            m2, u2, h2, d2 = build_request(req_json, p, source, param) # m2 = method, u2 = url, h2 = headers, d2 = data (just like the first time we called build_request)
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




