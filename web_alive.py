# web_alive.py
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is running."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
