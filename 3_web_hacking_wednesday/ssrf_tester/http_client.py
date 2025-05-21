import httpx

class HTTPClient:
    def __init__(self, timeout=10, verify_ssl=True):
        """
        Initializes the HTTP client with a persistent session.
        If verify_ssl is False, it disables SSL verification for all requests.
        """
        self.client = httpx.Client(timeout=timeout, verify=verify_ssl)

    def send_request(self, method, url, headers=None, data=None):
        try:
            # Filter out any non-ASCII characters from header values
            if headers:
                sanitized_headers = {}
                for k, v in headers.items():
                    try:
                        sanitized_headers[k] = v.encode("ascii", errors="ignore").decode("ascii")
                    except Exception:
                        continue  # skip broken headers entirely
            else:
                sanitized_headers = None

            response = self.client.request(method=method, url=url, headers=sanitized_headers, data=data)
            return response
        except httpx.RequestError as e:
            print(f"❌ HTTP request error: {e}")
            return None

    def close(self):
        """
        Closes the HTTP client session.
        """
        self.client.close()