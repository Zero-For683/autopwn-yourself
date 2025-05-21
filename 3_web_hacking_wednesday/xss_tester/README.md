XSS scanner, right now it uses the output of burpsuite pro spidering to pull all the requests on a site

The XSS scanner methodically goes through each request and tests the xss payload. This is a particularly laborious scanner because it requires you to verify the vulnerability in-browser to see if JavaScript was executed or not. 


Basic flow of program:
- Detect injection points & insert your unique marker for the request:
    1. Send a unique string (ie. z0f863)
- Fetch & find the unique string in the response (via beautifulsoup).
- Classify the sink into one of the contexts (find the unique string and how it relates to its surroundings): 
    1. HTML Data "<example>z0f863</example>"
    2. Attribute (quotted and unquotted)
    3. JS String Literal
    4. URL (href)
    5. CSS
- Select/generate only those payload templates that make sense for that context.
- Encode each variant and fire them off.
- Continue to the next request

--------------------------------------------------

TODO list for this tool:
- Payload generator
- Threading (so you can run more than one thread when scan is running)
- Selenium browser verification
- Front-page with all the help options