from flask import Flask, request, jsonify
import google.generativeai as genai
import yfinance as yf
import os
import json

app = Flask(__name__)

# Initialize Gemini
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

def get_esg_score(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.sustainability
        if info is not None and 'totalEsg' in info:
            return float(info['totalEsg'])
    except Exception as e:
        print(f"[YFinance] Error for {ticker_symbol}: {e}")
    return None

@app.route("/get_ticker", methods=["GET"])
async def get_ticker():
    brand_name = request.args.get("brand_name")
    esg_score = request.args.get("esg_score", type=float)

    if not brand_name or esg_score is None:
        return jsonify({"error": "Missing brand_name or esg_score"}), 400

    prompt = (
        f"The brand '{brand_name}' has an ESG risk score of {esg_score}. "
        f"Suggest 3 companies in the same industry with better ESG performance based on sustainalytics. "
        f"For each, include: brand_name, stock ticker, and homepage URL. "
        f"Return strictly as a JSON array of 3 objects: brand_name, ticker, homepage."
    )

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip().replace("```json", "").replace("```", "")
        print("[Gemini Response Raw]:", raw)

        suggestions = json.loads(raw)

        validated = []
        for item in suggestions:
            ticker = item.get("ticker")
            if not ticker:
                continue
            score = await get_esg_score(ticker)
            if score is not None and score < esg_score:
                validated.append({
                    "brand_name": item.get("brand_name"),
                    "ticker": ticker,
                    "esg_score": score,
                    "homepage": item.get("homepage")
                })

        # Return top 3 valid ones
        return jsonify({
            "brand_name": brand_name,
            "alternatives": validated[:3]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
