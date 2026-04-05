import os
import json

def handler(request):
    # Simple HTML response for testing
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
        .status { background: #e3f2fd; padding: 15px; border-radius: 5px; text-align: center; margin: 20px 0; }
        .error { background: #ffebee; color: #c62828; padding: 15px; border-radius: 5px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 Wildfire Risk Prediction App</h1>
        <div class="status">
            <h3>✅ Serverless Function is Working!</h3>
            <p>The API endpoint is live and responding correctly.</p>
            <p>Model loading and prediction features will be added next.</p>
            <p><small>Updated: 2025-04-05 16:48 UTC</small></p>
        </div>
        <div style="text-align: center; margin: 20px 0;">
            <h3>🚀 Deployment Status: SUCCESS</h3>
            <p>Your Vercel deployment is working correctly!</p>
        </div>
    </div>
</body>
</html>
    """
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html_content
    }

# Vercel entrypoint
app = handler
