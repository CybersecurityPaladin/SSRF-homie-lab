import re
import requests
from urllib.parse import urlparse
from flask import Flask, request, render_template, jsonify

# UNCOMMENT the next two lines to enable SSRF protection
# import ipaddress
# import socket

app = Flask(__name__)

def extract_url(text):
    url_pattern = r'https?://[^\s]+'
    match = re.search(url_pattern, text)
    return match.group(0) if match else None

def parse_og_and_title(html):
    og = {}
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if title_match:
        og['title'] = title_match.group(1).strip()
    meta_pattern = r'<meta\s+property="og:([^"]+)"\s+content="([^"]+)"'
    for match in re.finditer(meta_pattern, html, re.IGNORECASE):
        prop = match.group(1)
        content = match.group(2).strip()
        og[prop] = content
    return og

# UNCOMMENT this function to validate the target URL
# def is_safe_url(url):
#     parsed = urlparse(url)
#     host = parsed.hostname
#     if not host:
#         return False
#     try:
#         ip = socket.gethostbyname(host)
#         ip_obj = ipaddress.ip_address(ip)
#         return not (ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local)
#     except:
#         return False

@app.route("/level1", methods=["GET"])
def level1_page():
    return render_template("index.html")

@app.route("/level1/check", methods=["POST"])
def level1_check():
    text = request.form.get("text", "")
    if not text:
        return jsonify(error="Post text is empty"), 400

    url = extract_url(text)
    og_data = {}
    domain = ""

    if url:
        # UNCOMMENT the following block to perform URL safety check
        # if not is_safe_url(url):
        #     return jsonify(error="URL blocked due to security policy"), 400

        try:
            # UNCOMMENT next line (redirects disabled)
            # r = requests.get(url, timeout=5, allow_redirects=False, stream=True)
            # COMMENT OUT next line (original request with redirects allowed)
            r = requests.get(url, timeout=5, allow_redirects=True, stream=True)
            raw = bytearray()
            for chunk in r.iter_content(chunk_size=2048):
                raw.extend(chunk)
                if len(raw) >= 10000:
                    break
            r.close()
            html = raw.decode(r.encoding or "utf-8", errors="ignore")
            og_data = parse_og_and_title(html)
            domain = urlparse(url).hostname or ""
        except requests.exceptions.RequestException as e:
            domain = urlparse(url).hostname or ""
            og_data = {'title': 'Link', 'description': ''}

    if not url:
        return jsonify(text=text, og=None)

    if not og_data:
        og_data = {'title': domain or 'Link', 'description': ''}
    elif 'title' not in og_data:
        og_data['title'] = domain or 'Link'

    og_data['domain'] = domain
    response = jsonify(text=text, og=og_data)
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == "__main__":
    print("[*] app.py listening on 127.0.0.1:5050")
    app.run(host="127.0.0.1", port=5050, debug=False)