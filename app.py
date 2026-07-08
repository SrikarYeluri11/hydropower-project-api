# app1.py (Uploaded to GitHub)
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
API_KEY = "HYDROPOWER_CLIENT_2026"

model = joblib.load('model.pkl')
print('model loaded\n')

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'HydroPower Prediction API is Running'
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "Healthy"
    })

@app.route('/predict', methods=['POST'])
def predict():
    client_api_key = request.headers.get('x-api-key')

    if client_api_key != API_KEY:
        return jsonify({
            'status': 'error',
            'message': 'Invalid api key'
        }), 401
    
    try:
        data = request.get_json()
        water_inflow = data.get('Water_Inflow')

        # --- DATA QUALITY GUARDRAILS ---
        if water_inflow is None or str(water_inflow).strip() == "":
            return jsonify({"status": "error", "message": "The Google Sheet cell is empty."})
        
        try:
            water_inflow = float(water_inflow)
        except ValueError:
            return jsonify({"status": "error", "message": "Text was entered instead of a number."})
            
        if water_inflow < 0:
            return jsonify({"status": "error", "message": "Water inflow cannot be negative."})
            
        if water_inflow > 2000:
            return jsonify({"status": "error", "message": "Water inflow is unrealistically high."})
        # -------------------------------

        input_data = pd.DataFrame({
            'Water_Inflow': [water_inflow]
        })

        prediction = model.predict(input_data)

        # Notice the 'status': 'success' 
        return jsonify({
            'status': 'success',
            'Water_Inflow': water_inflow,
            'Predicted_Power_Generated': round(float(prediction[0]), 2) 
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
    
if __name__ == '__main__':
    app.run(debug=True)