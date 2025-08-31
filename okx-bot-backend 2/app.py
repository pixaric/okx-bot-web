from flask import Flask, jsonify
from datetime import datetime
import hmac, base64, hashlib, requests

app = Flask(__name__)

# 🔐 Tus credenciales OKX
API_KEY = '60fa6c47-056b-4f63-8850-f8accabd4f54'
SECRET_KEY = '983808B2A9D9792535A57FA724F7F17A'
PASSPHRASE = 'Trading.25'

def get_okx_headers(method, path, body=""):
    timestamp = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
    message = timestamp + method + path + body
    signature = base64.b64encode(
        hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).digest()
    ).decode()
    return {
        "OK-ACCESS-KEY": API_KEY,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

@app.route('/balance')
def balance():
    path = "/api/v5/account/balance"
    url = "https://my.okx.com" + path
    headers = get_okx_headers("GET", path)
    res = requests.get(url, headers=headers)
    return jsonify(res.json())

if __name__ == '__main__':
    app.run(debug=True)