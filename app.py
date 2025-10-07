from flask import Flask,jsonify,request
from flask_cors import CORS
import google.generativeai as genai
app = Flask(__name__)
CORS(app)  # allow all origins
genai.configure(api_key="AIzaSyDndkudiwiRg4UC0b7Lf6MZ2G_qHZFI-bc")
model=genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content("Write a poem about the sea in 4 lines")
print(response.text)
@app.route('/details', methods=['post'])
def farmer_details():
    data = request.json
    text = data.get("text", "")
    instruction = f"""
You are a JSON generator. 
Extract the crop name, quantity, and amount_per_quintal from this text: "{text}".
Return ONLY valid JSON, with no explanations, markdown, or extra text.
Example output format:
{"{"}
  "crop": "Mango",
  "quantity": "50",
  "amount_per_quintal": "1200"
{"}"}
"""
    response = model.generate_content(instruction)
    print(jsonify(response.text))
    return jsonify(response.text)
if __name__ == "__main__":
    print("\nRegistered routes:\n", app.url_map, "\n")
    app.run(debug=True)
