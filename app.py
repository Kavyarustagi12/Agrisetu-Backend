from flask import Flask,jsonify,request
import google.generativeai as genai
app = Flask(__name__)
genai.configure(api_key="AIzaSyDndkudiwiRg4UC0b7Lf6MZ2G_qHZFI-bc")
model=genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content("Write a poem about the sea in 4 lines")
print(response.text)
@app.route('/details', methods=['post'])
def farmer_details():
    data = request.json
    text = data.get("text", "")
    instruction="This text which i have send you. Identify the name of the crop, the quantity, and the amount per quintal. Return a " \
    "json object with the keys 'crop', 'quantity', and 'amount_per_quintal'. If any information is missing, set its value to null. " \
    "Here is the text: " + text
    response = model.generate_content(instruction)
    return jsonify({"response": response.text})
if __name__ == "__main__":
    print("\nRegistered routes:\n", app.url_map, "\n")
    app.run(debug=True)
