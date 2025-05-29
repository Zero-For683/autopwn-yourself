import asyncio
import httpx
from playwright.async_api import async_playwright
from request_builder import build_request

'''
    This is a high priority file to work on

    We need SOLID, 100% accuracy (or as damn close to 100% as we can get) on whether or not XSS was actually executed

    This will significantly reduce the number of false-positives if we can nail this. 
    '''

async def send_request(client: httpx.AsyncClient,
                       method: str,
                       url: str,
                       headers: dict | None = None,
                       data: dict | None = None,
                       timeout_secs: float = 10.0) -> httpx.Response | None:
    """
    Send a single HTTP request with a timeout and catch read-timeouts.
    Returns the Response, or None on timeout.
    """
    try:
        return await client.request(
            method,
            url,
            headers=headers,
            data=data,
            follow_redirects=True,
            timeout=timeout_secs
        )
    except httpx.ReadTimeout:
        print(f"[warning] Request timed out: {method} {url}")
        return None
    except httpx.HTTPError as e:
        print(f"[warning] HTTP error for {method} {url}: {e}")
        return None


async def test_payloads(req_json, core_payloads, source, param): # This doesnt test in-browser yet!!! THIS NEEDS TO HAPPEN. 
    """
    Fire each payload in core_payloads at the given source/param.
    Return a list of (payload, executed) tuples, but bail out on the first request failure.
    """
    results = []

    for payload in core_payloads:
        # 🔥 super-clear debug of what we're sending and where
        print(f"    [debug] → Testing core payload in {source} param '{param}': {payload!r}")
        method, url, headers, data = build_request(req_json, payload, source, param)

        try:
            resp = await client.request(method, url, headers=headers, data=data)
        except Exception as e:
            # ❌ tell me exactly which payload + param died, then continue
            print(f"    [error] Core payload request FAILED for param '{param}' payload {payload!r}: {e}")
            print(f"    [debug] → Aborting core payload loop for '{param}' and moving on\n")
            continue # before this was break. I dont want to stop testing just because a single one didnt work

        # ✅ we got *some* response — show me the status
        print(f"    [debug] Received HTTP {resp.status_code} for payload {payload!r} on '{param}'")

        # your existing XSS-execution check (whatever it is)
        executed = payload in resp.text  # just a placeholder for now. IT DOES NOT ACTUALLY SEE IF XSS WAS EXECUTED
        print(f"        [verify] {payload!r} → executed={executed}")

        results.append((payload, executed))

    return results



async def verify_in_browser(source, param, payload) -> bool:
    """
    Your Playwright snippet goes here. Returns True if we saw an alert()
    or other execution, False otherwise.
    """
    # ... your existing code ...
    pass

