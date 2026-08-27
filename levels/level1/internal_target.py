from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <html>
    <head>
        <meta property="og:title" content="Server Name" />
    </head>
    </html>
    """

@app.route("/admin")
def admin():
    return """
    <html>
    <head>
        <meta property="og:title" content="⚙️ Admin Panel" />
        <meta property="og:description" content="FLAG{admin_panel_via_og}" />
    </head>
    <body style="font-family: monospace; background:#1a1a2e; color:#e0e0e0; padding:2em;">
        <h1>Access denied!</h1>
        <p></p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5051)