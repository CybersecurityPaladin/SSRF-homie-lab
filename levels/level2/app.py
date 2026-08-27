import time
import struct
import socket
import ipaddress
import requests
from urllib.parse import urlparse
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Custom DNS resolver - talks to rebind_dns.py on :5053
# ---------------------------------------------------------------------------
DNS_SERVER = ("127.0.0.1", 5053)
REBIND_DOMAIN = "hooks.notifyservice.lab"


def dns_query_custom(hostname, timeout=2):
    """Send a raw A-record query to our lab DNS server and return the answer IP."""
    txid = int(time.time() * 1000) % 65535
    header = struct.pack(">HHHHHH", txid, 0x0100, 1, 0, 0, 0)
    qname = b"".join(bytes([len(l)]) + l.encode() for l in hostname.split(".")) + b"\x00"
    question = qname + struct.pack(">HH", 1, 1)  # type=A, class=IN
    packet = header + question

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        sock.sendto(packet, DNS_SERVER)
        data, _ = sock.recvfrom(512)
    finally:
        sock.close()
    return socket.inet_ntoa(data[-4:])


# Monkeypatch socket resolution ONLY for our lab domain, so that when
# `requests` later opens a real connection to that host, it goes through
# the same custom resolver as the save-time check did.
_orig_getaddrinfo = socket.getaddrinfo


def _patched_getaddrinfo(host, *args, **kwargs):
    if host == REBIND_DOMAIN:
        ip = dns_query_custom(host)
        return _orig_getaddrinfo(ip, *args, **kwargs)
    return _orig_getaddrinfo(host, *args, **kwargs)


socket.getaddrinfo = _patched_getaddrinfo

# ---------------------------------------------------------------------------
# In-memory "storage" for the saved webhook (single global slot - demo only)
# ---------------------------------------------------------------------------
STATE = {"webhook_url": None}


def is_safe_url(url):
    parsed = urlparse(url)
    host = parsed.hostname
    if not host:
        return False
    try:
        ip = dns_query_custom(host) if host == REBIND_DOMAIN else socket.gethostbyname(host)
        ip_obj = ipaddress.ip_address(ip)
        return not (ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved)
    except Exception:
        return False


@app.route("/level2", methods=["GET"])
def level2_page():
    return render_template("index.html", saved_url=STATE["webhook_url"])


@app.route("/level2/save", methods=["POST"])
def level2_save():
    url = request.form.get("url", "").strip()
    if not url:
        return jsonify(error="URL is empty"), 400

    if not is_safe_url(url):
        return jsonify(error="URL blocked: resolves to a private/internal address"), 400

    STATE["webhook_url"] = url
    return jsonify(status="saved", url=url)


@app.route("/level2/trigger", methods=["POST"])
def level2_trigger():
    url = STATE["webhook_url"]
    if not url:
        return jsonify(error="No webhook saved yet"), 400

    try:
        r = requests.post(url, json={"event": "order.status", "status": "shipped"}, timeout=5)
        body = r.text[:2000]
        return jsonify(status="delivered", http_status=r.status_code, body=body)
    except requests.exceptions.RequestException as e:
        return jsonify(error=f"Delivery failed: {e}"), 502


if __name__ == "__main__":
    print("[*] app.py listening on 127.0.0.1:5050")
    app.run(host="127.0.0.1", port=5050, debug=False)
