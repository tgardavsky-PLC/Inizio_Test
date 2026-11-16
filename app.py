from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

API_KEY = os.getenv("SERPAPI_API_KEY")

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword", "").strip()

    if not keyword:
        return jsonify({"error": "Chybí klíčové slovo"}), 400

    if not API_KEY:
        return jsonify({"error": "Chybí API klíč"}), 500

    params = {
        "engine": "google",
        "q": keyword,
        "api_key": API_KEY
    }

    try:
        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=30
        )
        response.raise_for_status()

        results = response.json()
        organic_results = results.get("organic_results", [])

        with open("results.json", "w", encoding="utf-8") as file:
            json.dump(
                organic_results,
                file,
                ensure_ascii=False,
                indent=4
            )

        return jsonify(organic_results)

    except requests.RequestException:
        return jsonify({"error": "Chyba při komunikaci se SerpAPI"}), 502


if __name__ == "__main__":
    app.run()
