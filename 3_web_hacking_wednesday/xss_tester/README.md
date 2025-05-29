XSS scanner, right now it uses the output of burpsuite pro spidering to pull all the requests on a site

The XSS scanner methodically goes through each request and tests the xss payload. This is a particularly laborious scanner because it requires you to verify the vulnerability in-browser to see if JavaScript was executed or not. 


** TODO **

So, we generate a very small, dumb list. Even if a site is vulnerable to XSS we are never going to find it with out current extremely basic payload list. We need to make our payload generator smarter by:
- Better identifying the context of our XSS payload being injected into (escaping via payloads like >'<script>alert(1)</script>)
- Throwing our core payloads into some basic encodings to bypass that as well
- After this, then we go into phase 2 / matrix scanning

Then, we need to incorporate in-browser testing for different events (like mousover if possible) since we cant do a lot of the portswigger labs without it




---

# **Basic flow of program:**

1. Detect injection points & insert your unique marker for the request:
    - Send a unique string (ie. z0f863)
2. Fetch & find the unique string in the response (via beautifulsoup).
3. Classify the sink into one of the contexts (find the unique string and how it relates to its surroundings)
    - Explained more in depth below
4. Select/generate only those payload templates that make sense for that context:
    - Core payloads
    - Secondary payloads
    - Full matrix payloads
5. Because there are potentiall tens of thousands of payloads, we'll do "phased-based" escalation
    - Try variants of core-payloads only
    - If core payloads are reflected, we will test secondary payloads
    - Full-matrix combos only as a last resort (Only for payloads that didnt execute but mightve reflected secondary payloads)
6. Encode each variant and fire them off.
7. Continue to the next request


# **ROADMAP**

Tier 1: Core contexts

Make sure the engine reliably handles the five “classic” injection contexts:

1. HTML Data (breaking out of a tag body)
2. Attribute (quoted & unquoted)
3. JS string literal
4. URL (href/src + javascript:/data:)
5. CSS (inline styles + <style> blocks)

Once those consistently produce valid payloads and execution evidence, it'll already catch the vast majority of reflected, stored, and many DOM XSS flaws.

---

Tier 2: Common bypass techniques

When I'm ready to level up, I'll add a small “bypass” toolkit that sits between the raw templates and encoders. For example:
1. Unicode/hex/UTF-7 escapes (turn alert into \u0061\u006cert)
2. Overlong UTF-8 sequences
3. Double- or triple-URL-encoding
4. Simple polyglots (payloads that work in HTML, JS, CSS simultaneously)

These are just extra transformation passes on the strings it'll already be generating.

I'll also need to "upgrade" how smart the thing is and NOT spray & pray. It needs to have the payload list as short as possible

---


Tier 3: Advanced contexts & trickery

If I get to this point I'll plugin more exotic classes as separate modules:
1. Obfuscation tricks (e.g. injecting <svg><script> inside weird XML namespaces)
2. Client-side template injection (mustache/Handlebars payloads)
3. Scriptless attacks (e.g. <meta http-equiv>, CSS animations with onanimationend)
4. WAF-bypass global objects (e.g. abusing window.onerror, location properties)

These often require special skeletons or completely different grammars, hence the "advanced" contexts and trickery.