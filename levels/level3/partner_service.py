"""
:5054 - "trusted" ad-network relay. app.py is only allowed to talk to this
host - but this host will happily 302-redirect to anywhere it's told to,
which is exactly what makes the whitelist in app.py useless.

Usage:
  GET /redirect?to=<any url>  -> 302 Location: <any url>
"""

from flask import Flask, request, redirect

app = Flask(__name__)


@app.route("/redirect")
def do_redirect():
    target = request.args.get("to", "/")
    return redirect(target, code=302)


@app.route("/")
def index():
    return "Trusted ad network relay. Use /redirect?to=<url>"


if __name__ == "__main__":
    print("[*] partner_service.py listening on 127.0.0.1:5054")
    app.run(host="127.0.0.1", port=5054)