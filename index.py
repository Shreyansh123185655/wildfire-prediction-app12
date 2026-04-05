import json
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize model variables
model = None
MODEL_LOADED = False
MODEL_ERROR = ""

try:
    import pandas as pd
    import joblib
    import numpy as np
    
    # Load model
    MODEL_PATH = "notebooks/wildfire_risk_model.pkl"
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        MODEL_LOADED = True
        MODEL_ERROR = ""
    else:
        MODEL_ERROR = f"Model file not found at {MODEL_PATH}"
except Exception as e:
    MODEL_LOADED = False
    MODEL_ERROR = str(e)

def handler(event, context):
    try:
        # Handle different HTTP methods
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        
        # Debug logging
        print(f"Request: {http_method} {path}")
        print(f"Model loaded: {MODEL_LOADED}")
        
        # Serve HTML frontend
        if http_method == 'GET' and (path == '/' or path == '/index.html'):
            try:
                html_file = 'index.html'
                if os.path.exists(html_file):
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    return {
                        'statusCode': 200,
                        'headers': {
                            'Content-Type': 'text/html; charset=utf-8',
                            'Cache-Control': 'no-cache, no-store, must-revalidate',
                        },
                        'body': html_content
                    }
                else:
                    error_body = '<h1>404 - Frontend not found</h1>'
                    return {
                        'statusCode': 404,
                        'headers': {
                            'Content-Type': 'text/html',
                        },
                        'body': error_body
                    }
            except Exception as e:
                print(f"Error serving HTML: {str(e)}")
                error_body = f'<h1>500 - Server Error: {str(e)}</h1>'
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'text/html',
                    },
                    'body': error_body
                }
        
        # Handle prediction API
        elif http_method == 'POST' and path == '/predict':
            try:
                if not MODEL_LOADED:
                    error_response = json.dumps({'error': f'Model not loaded: {MODEL_ERROR}'})
                    return {
                        'statusCode': 500,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*',
                        },
                        'body': error_response
                    }
                
                # Parse request body
                body_str = event.get('body', '{}')
                if not body_str:
                    error_response = json.dumps({'error': 'Empty request body'})
                    return {
                        'statusCode': 400,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*',
                        },
                        'body': error_response
                    }
                
                body = json.loads(body_str)
                
                # Validate required fields
                required_fields = ['temperature', 'min_temp', 'rainfall', 'wind_speed', 'month', 'day_of_year', 'lagged_rainfall', 'lagged_wind', 'season']
                for field in required_fields:
                    if field not in body:
                        error_response = json.dumps({'error': f'Missing required field: {field}'})
                        return {
                            'statusCode': 400,
                            'headers': {
                                'Content-Type': 'application/json',
                                'Access-Control-Allow-Origin': '*',
                            },
                            'body': error_response
                        }
                
                # Calculate derived features
                temperature = float(body['temperature'])
                min_temp = float(body['min_temp'])
                wind_speed = float(body['wind_speed'])
                
                temp_range = temperature - min_temp
                wind_temp_ratio = wind_speed / (temperature + 1) if temperature != -1 else 0
                
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
                
                response_data = {
                    "prediction": int(prediction),
                    "probability": float(probability)
                }
                
                response_body = json.dumps(response_data)
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'POST, OPTIONS',
                        'Access-Control-Allow-Headers': 'Content-Type',
                    },
                    'body': response_body
                }
                
            except Exception as e:
                print(f"Prediction error: {str(e)}")
                error_response = json.dumps({'error': f'Prediction failed: {str(e)}'})
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                    },
                    'body': error_response
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
            error_response = json.dumps({'error': f'Endpoint not found: {http_method} {path}'})
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': error_response
            }
            
    except Exception as e:
        print(f"Handler error: {str(e)}")
        error_response = json.dumps({'error': f'Handler failed: {str(e)}'})
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': error_response
        }

# Vercel entrypoint
app = handler
