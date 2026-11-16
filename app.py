from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

import os
import requests
import json

API_KEY = os.getenv("SERPAPI_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
        return render_template("index.html") 

@app.route("/search", methods=["POST"])
def search():
      keyword = request.form.get("keyword")

      if not keyword or not keyword.strip():
            return jsonify({"error": "Chybí klíčové slovo"}), 400

      params = {
            "engine": "google",
            "q": keyword,
            "api_key": API_KEY
      }

      response = requests.get("https://serpapi.com/search", params=params)
      results = response.json()
      organic_results = results.get("organic_results", [])

      with open("results.json", "w", encoding="utf-8") as file:
            json.dump(organic_results, file, ensure_ascii=False, indent=4)
      
      return jsonify(organic_results)

if __name__ == "__main__":
    app.run()