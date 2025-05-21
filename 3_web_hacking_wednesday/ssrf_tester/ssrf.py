import os
import glob
import argparse
from urllib.parse import urlparse

# Core SSRF modules
from payloads import loopback_payloads
from http_client import HTTPClient
from spidering import WebSpider

# Specialized vulnerabilities
from specific_vulns import SpecificVulnsTester, open_redirect_payloads
from basic_checks import test_url_parameters, test_post_parameters, test_header_ssrf  
from payloads import loopback_payloads, fake_relative_url_payloads, domain_allow_list_bypass_payloads
from xml_to_json_splitter import burp_to_json



def get_args():

    parser = argparse.ArgumentParser(description="SSRF Testing Script")

    parser.add_argument("--url", required=True, help="Target URL to test")
    parser.add_argument("--allowed", required=False, help="Allowed domain to use in payloads")
    parser.add_argument("--attacker", required=False, help="Attacker domain to use in payloads")
    parser.add_argument("--spider", action="store_true", help="Enable spidering the target URL")
    parser.add_argument("--redirect", action="store_true", help="Enable open redirect tests")
    parser.add_argument("--shellshock", action="store_true", help="Enable Shellshock vulnerability tests")
    parser.add_argument("--insecure", action="store_true", help="Skip SSL certificate verification (e.g., for Burp)")
    parser.add_argument("--burp", action="store_true", help="Convert Burp XML files to JSON")


    return parser.parse_args()


class SSRFTester:
    """
    A class that orchestrates SSRF testing:
    """

    def __init__(self, target_url, allowed_host=None, attacker_host=None,
                 do_spider=False, do_redirect=False, do_shellshock=False, skip_ssl_verification=False):
        self.target_url = target_url
        self.allowed_host = allowed_host
        self.attacker_host = attacker_host

        self.do_spider = do_spider
        self.do_redirect = do_redirect
        self.do_shellshock = do_shellshock
        self.skip_ssl_verification = skip_ssl_verification

        self.domain = urlparse(self.target_url).netloc
        self.json_folder = os.path.join("requests_responses", self.domain)
        self.json_files = glob.glob(os.path.join(self.json_folder, "*.json"))

    # ---------------------------
    # Core SSRF Testing
    # ---------------------------
    def spider_site(self):
        """Spider the site to capture requests/responses."""
        spider = WebSpider(self.target_url)
        spider.start_spidering()

    def test_url_parameters(self, payloads):
        test_url_parameters(self.json_files, payloads, self.allowed_host, self.attacker_host)

    def test_post_parameters(self, payloads):
        test_post_parameters(self.json_files, payloads, self.allowed_host, self.attacker_host)

    def test_header_parameters(self, payloads):
        test_header_ssrf(self.json_files, payloads, self.allowed_host, self.attacker_host)
    


    # ---------------------------
    # Optional: run everything
    # ---------------------------
    def run(self, payloads=None, allowed_host=None, attacker_host=None):
        # 1) Possibly spider
        if self.do_spider:
            self.spider_site()
            self.json_files = glob.glob(os.path.join(self.json_folder, "*.json"))

        # 2) Print info
        print(f"🔍 Testing URL: {self.target_url}")
        print(f"✅ Allowed Host: {self.allowed_host or 'Not provided'}")
        print(f"⚠️  Attacker Host: {self.attacker_host or 'Not provided'}")


        payloads = domain_allow_list_bypass_payloads + loopback_payloads

        # 3) Standard SSRF tests
        if payloads is None:
            payloads = loopback_payloads

        self.test_url_parameters(payloads)
        self.test_post_parameters(payloads)
        self.test_header_parameters(payloads)

        # 4) Optionally test open redirect
        if self.do_redirect:
            print("\n🔀 Checking for Open Redirect vulnerabilities...")
            vuln_tester = SpecificVulnsTester()  
            http_client = HTTPClient()
            open_redirects_found = vuln_tester.detect_open_redirect(
                self.json_files,
                open_redirect_payloads,
                http_client
            )
            http_client.close()
    
            if open_redirects_found:
                vuln_tester.test_ssrf(
                    self.json_files,
                    open_redirects_found,
                    loopback_payloads,
                    allowed_host,
                    attacker_host
                )

        # 5) Optionally test shellshock
        if self.do_shellshock:
            print("💥 Checking for Shellshock vulnerabilities...")
            vuln_tester = SpecificVulnsTester()
            http_client = HTTPClient(verify_ssl=not self.skip_ssl_verification)
            for file_path in self.json_files:
                vuln_tester.shellshock(
                    file_path, http_client,
                    evil_domain=self.attacker_host
                )
            http_client.close()

def main():
    args = get_args()

    domain = urlparse(args.url).netloc
    json_folder = os.path.join("requests_responses", domain)



    if args.burp:
        desktop_path = "C:/Users/Gabe/Desktop/Burp-Temp/"
        xml_files = glob.glob(os.path.join(desktop_path, "*.xml"))

        for xml_file in xml_files:
            try:
                print(f"🔄 Converting: {xml_file}")
                burp_to_json(json_folder, xml_file)
            except Exception as e:
                print(f"[!] Failed to convert {xml_file}: {e}")

        for xml_file in xml_files:
            try:
                os.remove(xml_file)
                print(f"🧹 Deleted: {xml_file}")
            except Exception as e:
                print(f"[!] Could not delete {xml_file}: {e}")

    tester = SSRFTester(
        target_url=args.url,
        allowed_host=args.allowed,
        attacker_host=args.attacker,
        do_spider=args.spider,
        do_redirect=args.redirect,
        do_shellshock=args.shellshock,
        skip_ssl_verification=args.insecure
    )

    # Call the 'run' method on 'tester'
    tester.run()


if __name__ == "__main__":
    main()