import json
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import pandas as pd
    import joblib
    import numpy as np
    
    # Load model
    MODEL_PATH = "notebooks/wildfire_risk_model.pkl"
    model = joblib.load(MODEL_PATH)
    MODEL_LOADED = True
except Exception as e:
    MODEL_LOADED = False
    MODEL_ERROR = str(e)

def handler(event, context):
    # Handle different HTTP methods
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    
    # Serve HTML frontend
    if http_method == 'GET' and (path == '/' or path == '/index.html'):
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html; charset=utf-8',
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                },
                'body': html_content
            }
        except FileNotFoundError:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'text/html',
                },
                'body': '<h1>404 - Frontend not found</h1>'
            }
    
    # Handle prediction API
    elif http_method == 'POST' and path == '/predict':
        if not MODEL_LOADED:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': json.dumps({'error': f'Model not loaded: {MODEL_ERROR}'})
            }
        
        try:
            # Parse request body
            body = json.loads(event.get('body', '{}'))
            
            # Calculate derived features
            temperature = float(body['temperature'])
            min_temp = float(body['min_temp'])
            wind_speed = float(body['wind_speed'])
            
            temp_range = temperature - min_temp
            wind_temp_ratio = wind_speed / (temperature + 1)
            
            # Prepare input as DataFrame
            input_data = pd.DataFrame([{
                "temperature": temperature,
                "rainfall": float(body['rainfall']),
                "wind_speed": wind_speed,
                "season": body['season'],
                "MIN_TEMP": min_temp,
                "TEMP_RANGE": temp_range,
                "WIND_TEMP_RATIO": wind_temp_ratio,
                "MONTH": int(body['month']),
                "LAGGED_PRECIPITATION": float(body['lagged_rainfall']),
                "LAGGED_AVG_WIND_SPEED": float(body['lagged_wind']),
                "DAY_OF_YEAR": int(body['day_of_year'])
            }])
            
            # Prediction
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1]
            
            response = {
                "prediction": int(prediction),
                "probability": float(probability)
            }
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps(response)
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'error': str(e)})
            }
    
    # Handle CORS preflight
    elif http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    # Handle 404
    else:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps({'error': 'Endpoint not found'})
        }

# Vercel entrypoint
app = handler
