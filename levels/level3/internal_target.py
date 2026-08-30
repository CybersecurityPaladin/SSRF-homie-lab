from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <html><body style="font-family: sans-serif; background:#1a1a2e; color:#e0e0e0; padding:2em;">
    <h1>Internal Partner Dashboard</h1>
    <p>If you accessed the internal server directly, the flag is invalid. If you accessed it through the SSRF vulnerability, here is your valid flag:</p>
    <p>FLAG{ssrf_via_redirect_bypass}</p>
    </body></html>
    """


if __name__ == "__main__":
    print("[*] internal_target.py listening on 127.0.0.1:5051")
    app.run(host="127.0.0.1", port=5051)