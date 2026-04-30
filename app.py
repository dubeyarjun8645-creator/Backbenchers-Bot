import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UG Uploader Bot v2.0</title>
    <style>
        body { background-color: #121212; color: #ff4d4d; font-family: monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .container { text-align: center; border: 2px solid #ff4d4d; padding: 20px; border-radius: 10px; }
        .card { text-decoration: none; color: inherit; }
        b { font-size: 1.5em; }
        footer { margin-top: 20px; color: #888; font-size: 0.8em; }
        img { border-radius: 50%; margin: 5px; vertical-align: middle; }
    </style>
</head>
<body>
    <div class="container">
        <a href="#" class="card">
            <pre>
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▄▄▄░█░▄▄▀█▄░▄██░▀██░█▄░▄██
██▄▄▄▀▀█░▀▀░██░███░█░█░██░███
██░▀▀▀░█░██░█▀░▀██░██▄░█▀░▀██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
            </pre>
            <b>v2.0.0 Live</b>
        </a>
    </div>
    <footer>
        <img src="https://tinypic.host/images/2025/04/28/IMG_20250428_085026_585.jpg" width="30" height="30">
        Powered By SAINI & ARJUN
        <p>© 2026 Video Downloader. All rights reserved.</p>
    </footer>
</body>
</html>
"""

if __name__ == "__main__":
    # Render uses 'PORT' environment variable
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
