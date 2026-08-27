from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # This is the "real" internal notification backend. It should only ever
    # be reachable from inside the network, never from app.py:5050 directly.
    return (
        '{"status": "internal notification service", '
        '"flag": "FLAG{dns_rebinding_toctou_bypass}"}',
        200,
        {"Content-Type": "application/json"},
    )


if __name__ == "__main__":
    print("[*] internal_target.py listening on 127.0.0.1:5051")
    app.run(host="127.0.0.1", port=5051)
