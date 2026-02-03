from http_client import HTTPClient
from utils import SSRFUtils

def test_url_parameters(json_files, payloads, allowed_host=None, attacker_host=None):
    """
    Tests URL query parameters for SSRF on each JSON file.
    """
    http_client = HTTPClient(verify_ssl=False)
    for file in json_files:
        SSRFUtils.url_param_payloads(
            file=file,
            http_client=http_client,
            payloads=payloads,
            allowed_host=allowed_host,
            evil_host=attacker_host
        )
        
    http_client.close()


def test_post_parameters(json_files, payloads, allowed_host=None, attacker_host=None):
    """
    Tests POST parameters for SSRF on each JSON file.
    """
    http_client = HTTPClient(verify_ssl=False)
    for file in json_files:
        SSRFUtils.post_param_payloads(
            file=file,
            http_client=http_client,
            payloads=payloads,
            allowed_host=allowed_host,
            evil_host=attacker_host
        )
    http_client.close()

def test_header_ssrf(json_files, payloads, allowed_host=None, attacker_host=None):
    http_client = HTTPClient(verify_ssl=False)
    for file in json_files:
        SSRFUtils.header_payloads(
            file=file,
            http_client=http_client,
            payloads=payloads,
            allowed_host=allowed_host,
            evil_host=attacker_host
        )
    http_client.close()