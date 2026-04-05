import os
import json
import pandas as pd
import joblib
import numpy as np
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Load model
MODEL_PATH = "notebooks/wildfire_risk_model.pkl"
model = joblib.load(MODEL_PATH)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve the web interface
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 Wildfire Risk Prediction</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #ff6b35; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .row { display: flex; gap: 15px; }
        .row .form-group { flex: 1; }
        button { background: #ff6b35; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; }
        button:hover { background: #e55a2b; }
        .result { margin-top: 20px; padding: 15px; border-radius: 5px; text-align: center; font-weight: bold; }
        .high-risk { background: #ffebee; color: #c62828; border: 1px solid #ef5350; }
        .low-risk { background: #e8f5e8; color: #2e7d32; border: 1px solid #66bb6a; }
        .loading { display: none; text-align: center; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 Wildfire Risk Prediction App</h1>
        <p>Enter environmental details to predict wildfire risk:</p>
        
        <form id="predictionForm">
            <div class="row">
                <div class="form-group">
                    <label for="temperature">🌡️ Temperature (°F)</label>
                    <input type="number" id="temperature" name="temperature" min="-50" max="150" value="85" required>
                </div>
                <div class="form-group">
                    <label for="min_temp">❄️ Minimum Temperature (°F)</label>
                    <input type="number" id="min_temp" name="min_temp" min="-50" max="150" value="65" required>
                </div>
            </div>
            
            <div class="row">
                <div class="form-group">
                    <label for="rainfall">🌧️ Rainfall (mm)</label>
                    <input type="number" id="rainfall" name="rainfall" min="0" max="500" value="0" step="0.1" required>
                </div>
                <div class="form-group">
                    <label for="wind_speed">💨 Wind Speed (km/h)</label>
                    <input type="number" id="wind_speed" name="wind_speed" min="0" max="200" value="18" step="0.1" required>
                </div>
            </div>
            
            <div class="row">
                <div class="form-group">
                    <label for="month">📅 Month</label>
                    <input type="number" id="month" name="month" min="1" max="12" value="6" required>
                </div>
                <div class="form-group">
                    <label for="day_of_year">📆 Day of Year</label>
                    <input type="number" id="day_of_year" name="day_of_year" min="1" max="365" value="180" required>
                </div>
            </div>
            
            <div class="row">
                <div class="form-group">
                    <label for="lagged_rainfall">🌧️ Previous Day Rainfall (mm)</label>
                    <input type="number" id="lagged_rainfall" name="lagged_rainfall" min="0" max="500" value="0" step="0.1" required>
                </div>
                <div class="form-group">
                    <label for="lagged_wind">💨 Previous Day Wind Speed (km/h)</label>
                    <input type="number" id="lagged_wind" name="lagged_wind" min="0" max="200" value="15" step="0.1" required>
                </div>
            </div>
            
            <div class="form-group">
                <label for="season">🗓️ Season</label>
                <select id="season" name="season" required>
                    <option value="Winter">Winter</option>
                    <option value="Spring">Spring</option>
                    <option value="Summer" selected>Summer</option>
                    <option value="Autumn">Autumn</option>
                </select>
            </div>
            
            <button type="submit">🚀 Predict Wildfire Risk</button>
        </form>
        
        <div class="loading" id="loading">
            <p>🔄 Processing prediction...</p>
        </div>
        
        <div id="result"></div>
    </div>

    <script>
        document.getElementById('predictionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            
            loading.style.display = 'block';
            result.innerHTML = '';
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const prediction = await response.json();
                
                loading.style.display = 'none';
                
                if (prediction.error) {
                    result.innerHTML = `<div class="result high-risk">❌ Error: ${prediction.error}</div>`;
                } else {
                    const riskClass = prediction.prediction === 1 ? 'high-risk' : 'low-risk';
                    const riskText = prediction.prediction === 1 ? 'High Wildfire Risk' : 'Low Wildfire Risk';
                    const emoji = prediction.prediction === 1 ? '⚠️' : '✅';
                    
                    result.innerHTML = `
                        <div class="result ${riskClass}">
                            <h3>${emoji} ${riskText}</h3>
                            <p>Probability: ${(prediction.probability * 100).toFixed(2)}%</p>
                        </div>
                    `;
                }
            } catch (error) {
                loading.style.display = 'none';
                result.innerHTML = `<div class="result high-risk">❌ Network error: ${error.message}</div>`;
            }
        });
    </script>
</body>
</html>
            """
            
            self.wfile.write(html_content.encode())
            return
        
        # Handle prediction endpoint
        elif self.path == '/predict':
            self.do_POST()
            return
        
        # Handle 404
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'404 Not Found')
    
    def do_POST(self):
        if self.path != '/predict':
            self.send_response(404)
            self.end_headers()
            return
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            # Calculate derived features
            temperature = float(data['temperature'])
            min_temp = float(data['min_temp'])
            wind_speed = float(data['wind_speed'])
            
            temp_range = temperature - min_temp
            wind_temp_ratio = wind_speed / (temperature + 1)
            
            # Prepare input as DataFrame
            input_data = pd.DataFrame([{
                "temperature": temperature,
                "rainfall": float(data['rainfall']),
                "wind_speed": wind_speed,
                "season": data['season'],
                "MIN_TEMP": min_temp,
                "TEMP_RANGE": temp_range,
                "WIND_TEMP_RATIO": wind_temp_ratio,
                "MONTH": int(data['month']),
                "LAGGED_PRECIPITATION": float(data['lagged_rainfall']),
                "LAGGED_AVG_WIND_SPEED": float(data['lagged_wind']),
                "DAY_OF_YEAR": int(data['day_of_year'])
            }])
            
            # Prediction
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1]
            
            response = {
                "prediction": int(prediction),
                "probability": float(probability)
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {"error": str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())
