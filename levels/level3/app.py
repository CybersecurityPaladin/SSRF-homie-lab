import requests
from urllib.parse import urlparse, quote
from flask import Flask, request, render_template

app = Flask(__name__)

ALLOWED_AD_HOST = "127.0.0.1:5054"


def is_trusted_ad_domain(url):
    # Whitelist check: only allow requests whose HOST is our trusted ad
    # network. This is the entire "security control" for this level - it
    # only looks at the URL the banner points to, never at where that host
    # might redirect the request to afterwards.
    parsed = urlparse(url)
    if not parsed.hostname:
        return False
    host_port = f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname
    return host_port == ALLOWED_AD_HOST


@app.route("/level3", methods=["GET"])
def level3_page():
    # The banner links to our trusted ad network, which then relays the
    # click to the real advertiser.
    inner = "http://127.0.0.1:5054/redirect?to=https://example.com/"
    banner_href = "/level3/go?url=" + quote(inner, safe="")
    return render_template("index.html", banner_href=banner_href)


@app.route("/level3/go", methods=["GET"])
def level3_go():
    url = request.args.get("url", "")
    if not url:
        return "Missing url parameter", 400

    if not is_trusted_ad_domain(url):
        return "Blocked: destination is not a trusted ad network domain", 403

    # UNCOMMENT the following block to mitigate: stop following redirects
    # blindly. This is the simplest fix - the ad network can still redirect
    # you, but the browser (not the server) will be the one following it,
    # so the whitelist check applies again on the next hop.
    # try:
    #     r = requests.get(url, timeout=5, allow_redirects=False)
    # except requests.exceptions.RequestException as e:
    #     return f"Ad delivery failed: {e}", 502
    # if r.is_redirect and "Location" in r.headers:
    #     return "", 302, {"Location": r.headers["Location"]}
    # return r.text, r.status_code, {"Content-Type": r.headers.get("Content-Type", "text/html")}

    # UNCOMMENT the following block INSTEAD, for a stronger fix: follow
    # redirects manually server-side, re-validating the destination host
    # after every single hop instead of trusting the very first check.
    # current_url = url
    # for _ in range(5):
    #     if not is_trusted_ad_domain(current_url):
    #         return "Blocked: redirect chain left the trusted ad network", 403
    #     try:
    #         r = requests.get(current_url, timeout=5, allow_redirects=False)
    #     except requests.exceptions.RequestException as e:
    #         return f"Ad delivery failed: {e}", 502
    #     if r.is_redirect and "Location" in r.headers:
    #         current_url = r.headers["Location"]
    #         continue
    #     return r.text, r.status_code, {"Content-Type": r.headers.get("Content-Type", "text/html")}
    # return "Too many redirects", 502

    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        return r.text, r.status_code, {"Content-Type": r.headers.get("Content-Type", "text/html")}
    except requests.exceptions.RequestException as e:
        return f"Ad delivery failed: {e}", 502


if __name__ == "__main__":
    print("[*] app.py listening on 127.0.0.1:5050")
    app.run(host="127.0.0.1", port=5050, debug=False)