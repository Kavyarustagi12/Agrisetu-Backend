from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai
import json
import re

app = Flask(__name__)
CORS(app)  # allow all origins

genai.configure(api_key="AIzaSyCr6NV2w1PMUNq4mb2QIa7Ubjt0YG_aOYA")
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route('/details', methods=['POST'])
def farmer_details():
    data = request.json
    text = data.get("text", "")

    instruction = f"""
You are a JSON generator. 
Extract the crop name, quantity, and amount_per_quintal from this text: "{text}".
Return ONLY valid JSON, with no explanations, markdown, or extra text.
Example output format:
{{
  "crop": "Mango",
  "quantity": "50",
  "amount_per_quintal": "1200"
}}
"""

    try:
        # Call Gemini API
        response = model.generate_content(instruction)
        raw_text = response.text.strip()

        # Remove ```json ... ``` or ``` ... ``` wrappers if present
        cleaned_text = re.sub(r"^```(?:json)?|```$", "", raw_text).strip()

        # Parse JSON safely
        json_data = json.loads(cleaned_text)

    except Exception as e:
        # Always return JSON, even on error
        json_data = {
            "error": "Failed to parse Gemini response",
            "raw_text": raw_text,
            "exception": str(e)
        }

    return jsonify(json_data)

if __name__ == "__main__":
    app.run(debug=True)
