import os
import json
import time
import re
from urllib.parse import urlparse, parse_qs, urljoin
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class WebSpider:
    def __init__(self, target_url, use_proxy=True):
        """
        Initialize the WebSpider with a target URL.
        """
        self.target_url = target_url
        self.parsed_target = urlparse(target_url)
        self.domain_folder = os.path.join("requests_responses", self.parsed_target.netloc)
        os.makedirs(self.domain_folder, exist_ok=True)
        self.use_proxy = use_proxy
        self.driver = self._get_driver()

    def _get_driver(self):
        """
        Creates and returns a new Chrome WebDriver instance with options.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        if self.use_proxy:
            # Configure a proxy for Chrome using Selenium Wire
            seleniumwire_options = {
                'proxy': {
                    'http': 'http://127.0.0.1:8080',
                    'https': 'http://127.0.0.1:8080',
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }
            return webdriver.Chrome(options=chrome_options, seleniumwire_options=seleniumwire_options)
        else:
            return webdriver.Chrome(options=chrome_options)

    def _sanitize_filename(self, filename: str):
        """
        Sanitizes filenames by removing invalid characters.
        """
        filename = filename.split('?', 1)[0].split('#', 1)[0]  # Remove query/fragments
        return re.sub(r'[<>:"/\\|?*\s]', '_', filename)

    def _capture_requests(self):
        """
        Saves request/response data for any requests that match the `target_url` domain.
        """
        for request in self.driver.requests:
            if request.response:
                url = request.url
                # Skip common static-file extensions
                if self.target_url in url and not url.endswith(
                    ('.png', '.svg', '.jpg', '.jpeg', '.gif', '.ico', '.webp', '.css', '.js')
                ):
                    parsed_url = urlparse(url)
                    endpoint_path = parsed_url.path or "root"
                    sanitized_path = self._sanitize_filename(endpoint_path)
                    filename = f"{sanitized_path}.json"

                    # Extract URL query parameters
                    query_params = parse_qs(parsed_url.query)
                    response_html = self.driver.page_source

                    # Check for POST data
                    post_body = None
                    post_params = None
                    if request.method.upper() == 'POST' and request.body:
                        try:
                            post_body_str = request.body.decode('utf-8', errors='replace')
                            content_type = request.headers.get('Content-Type', '').lower()
                            if 'application/x-www-form-urlencoded' in content_type:
                                post_params = parse_qs(post_body_str)
                                post_body = post_body_str
                            else:
                                post_body = post_body_str
                        except Exception as e:
                            post_body = f"Failed to decode POST body: {str(e)}"

                    request_response_data = {
                        "URL": url,
                        "Method": request.method,
                        "HTTP Version": request.response.headers.get(':version', 'Unknown'),
                        "Request Headers": dict(request.headers),
                        "Response Headers": dict(request.response.headers),
                        "URL Parameters": query_params,
                        "HTML Content": response_html
                    }
                    if post_body is not None:
                        request_response_data["POST Body"] = post_body
                    if post_params is not None:
                        request_response_data["POST Parameters"] = post_params

                    output_path = os.path.join(self.domain_folder, filename)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(request_response_data, f, indent=4)

    def _interact_with_forms(self):
        """
        Dynamically finds and interacts with forms by selecting dropdowns, filling text fields, and capturing requests.
        """
        forms = self.driver.find_elements(By.TAG_NAME, "form")
        time.sleep(1)

        for form in forms:
            try:
                # Handle Dropdown Selections (if available)
                selects = form.find_elements(By.TAG_NAME, "select")
                for select_element in selects:
                    dropdown = Select(select_element)
                    for index in range(len(dropdown.options)):
                        dropdown.select_by_index(index)
                        selected_value = dropdown.first_selected_option.get_attribute("value")
                        print(f"Selected option: {selected_value}")

                        time.sleep(1)

                        if selected_value.startswith("http") or selected_value.startswith("/"):
                            test_url = urljoin(self.driver.current_url, selected_value)
                            print(f"Manually requesting stock check: {test_url}")

                            self.driver.get(test_url)
                            time.sleep(2)
                            self._capture_requests()

                            self.driver.back()
                            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                # Click Submit Buttons
                submit_buttons = form.find_elements(By.XPATH, ".//button[@type='submit'] | .//input[@type='submit']")
                if submit_buttons:
                    for button in submit_buttons:
                        try:
                            self.driver.execute_script("arguments[0].scrollIntoView();", button)
                            time.sleep(1)

                            try:
                                button.click()
                            except:
                                self.driver.execute_script("arguments[0].click();", button)

                            print("Clicked submit button.")
                            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                            self._capture_requests()

                            self.driver.back()
                            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                        except Exception as e:
                            print(f"Skipping submit button due to error: {str(e)}")
                else:
                    print("No submit button found in form. Trying JavaScript form submission.")
                    self.driver.execute_script("arguments[0].submit();", form)
                    time.sleep(2)
                    self._capture_requests()
                    self.driver.back()
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            except Exception as e:
                print(f"Skipping form due to error: {str(e)}")

    def start_spidering(self, method="GET", url=None, headers=None, post_data=None):
        """
        Starts spidering the target site, capturing requests and responses for each visited URL.
        """
        visited_urls = set()
        links_to_visit = {self.target_url}
        wait = WebDriverWait(self.driver, 10)

        def interceptor(request):
            if headers:
                for key, value in headers.items():
                    request.headers[key] = value
            if method == "POST" and post_data:
                request.body = post_data.encode("utf-8")
                request.headers["Content-Length"] = str(len(post_data.encode("utf-8")))

        self.driver.request_interceptor = interceptor

        try:
            while links_to_visit:
                current_url = links_to_visit.pop()
                if current_url in visited_urls:
                    continue
                visited_urls.add(current_url)

                self.driver.requests.clear()

                if method == "POST" and url == current_url:
                    print(f"📡 Sending POST request to {current_url}")
                    self.driver.get(current_url)
                else:
                    self.driver.get(current_url)

                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                self._capture_requests()

                # Click All Links
                a_tags = self.driver.find_elements(By.TAG_NAME, 'a')
                for link in a_tags:
                    try:
                        href = link.get_attribute('href')
                        if href and self.parsed_target.netloc in urlparse(href).netloc:
                            links_to_visit.add(href)
                    except Exception as e:
                        print(f"Skipping <a> due to error: {str(e)}")

                # Click All Buttons
                buttons = self.driver.find_elements(By.XPATH, "//button | //input[@type='button']")
                for button in buttons:
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView();", button)
                        time.sleep(1)
                        button.click()
                        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                        self._capture_requests()
                        self.driver.back()
                        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    except Exception as e:
                        print(f"Skipping button due to error: {str(e)}")

                self._interact_with_forms()

        finally:
            self.driver.quit()
