import os
from flask import Flask, redirect, request, jsonify
import requests

app = Flask(__name__)

# ✅ Carica le variabili d’ambiente
CLIENT_ID = os.environ.get("CANVA_CLIENT_ID")
CLIENT_SECRET = os.environ.get("CANVA_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("CANVA_REDIRECT_URI")
RETURN_URI = os.environ.get("CANVA_RETURN_URI")

@app.route("/")
def home():
    auth_url = (
        f"https://www.canva.com/oauth/authorize?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code"
    )
    return redirect(auth_url)

@app.route("/oauth/redirect")
def oauth_redirect():
    code = request.args.get("code")
    if not code:
        return "❌ Codice OAuth non fornito", 400

    token_url = "https://api.canva.com/auth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code != 200:
        return f"❌ Errore durante lo scambio token:\n{response.text}", 500

    return jsonify(response.json())

@app.route("/return-nav")
def return_nav():
    return "🔁 Navigazione di ritorno da Canva completata! L’utente è tornato al tuo sistema."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001)
