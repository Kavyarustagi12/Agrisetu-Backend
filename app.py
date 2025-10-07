from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai
import json

app = Flask(__name__)
CORS(app)  # allow all origins

genai.configure(api_key="AIzaSyDndkudiwiRg4UC0b7Lf6MZ2G_qHZFI-bc")
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

    # Call Gemini API
    response = model.generate_content(instruction)
    raw_text = response.text.strip()  # remove extra spaces/newlines

    try:
        # Parse the string into JSON
        json_data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        # If Gemini returns invalid JSON, return an error
        return jsonify({"error": "Invalid JSON returned by API", "raw_text": raw_text}), 500

    return jsonify(json_data)

if __name__ == "__main__":
    print("\nRegistered routes:\n", app.url_map, "\n")
    app.run(debug=True)
