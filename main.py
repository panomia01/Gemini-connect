from flask import Flask, request, jsonify
import google.generativeai as genai
import json
import os
app = Flask(__name__)

# Correct way to initialize Gemini
genai.configure(api_key=os.environ["GOOGLE_API_KEY"]) # Replace with your key

# Create the model instance (use gemini-1.5-flash or gemini-pro if preferred)
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route("/get_ticker", methods=["GET"])
def get_ticker():
    brand_name = request.args.get("brand_name")
    esg_score = request.args.get("esg_score")

    if not brand_name or not esg_score:
        return jsonify({"error": "Missing 'brand_name' or 'esg_score' parameter"}), 400

    prompt = (
        f"The brand '{brand_name}' has an ESG risk score of {esg_score}. "
        f"Suggest 3 alternative companies in the same industry (e.g., sportswear, apparel, or footwear) "
        f"with better ESG performance. For each brand, include:\n"
        f"- Brand Name\n"
        f"- Stock Ticker (if available)\n"
        f"- ESG Risk Score (approximate)\n"
        f"- Homepage URL\n"
        f"Return the response as a JSON array of 3 objects with fields: brand_name, ticker, esg_score, homepage."
    )

    try:
        response = model.generate_content(prompt)
        print(response)
        # Clean up Gemini output in case it includes ```json code block
        raw = response.text.strip().replace("```json", "").replace("```", "")
        parsed = json.loads(raw)
        return jsonify({
            "brand_name": brand_name,
            "alternatives": parsed
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
