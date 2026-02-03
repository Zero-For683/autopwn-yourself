def url_param_payloads(file, http_client, payloads):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    url = data["URL"]
    headers = data["Request Headers"]
    method = data["Method"].upper()
    # Defining our url/headers/method for the request

    parsed = urlparse(url) # Breaks into 6 attributes
    query_params = parse_qs(parsed.query) # Breaks parameters into dictionary

    for param, value in query_params.items(): # Looping over the new dict
        for payload in payloads: # Injecting all payloads in our list
            temp_params = query_params.copy() # When we loop, we reset by copying the original dict
            temp_params[param] = [payload] # Access the key and change the value
            modified_query = urlencode(temp_params, doseq=True) # Smush the params back into URL format
            test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{modified_query}" # Build the URL

            print(f"Testing {payload} against {test_url}")
            http_client.send_request(method, test_url, headers)