import json

def handler(event, context):
    # Simple HTML response
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Wildfire Prediction</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #ff6b35; text-align: center; }
        .status { background: #e3f2fd; padding: 15px; border-radius: 5px; text-align: center; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 Wildfire Risk Prediction App</h1>
        <div class="status">
            <h3>✅ Serverless Function Working!</h3>
            <p>Basic deployment successful. ML features will be added next.</p>
        </div>
    </div>
</body>
</html>"""
    
    response_body = html_content
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': response_body
    }

app = handler
