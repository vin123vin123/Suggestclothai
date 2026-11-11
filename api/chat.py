from http.server import BaseHTTPRequestHandler
import json
import os
import requests

# --- CONFIGURATION ---
API_URL = "https://suggestonlineshops.onrender.com/chat"
# Safely pulls the key from Vercel's server environment, falling back to the default string if missing
API_SECRET_TOKEN = os.getenv("API_SECRET_TOKEN", "Mycux2erkec6")
# ---------------------

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            request_data = json.loads(post_data.decode('utf-8'))
            prompt = request_data.get("prompt", "")

            headers = {
                "Content-Type": "application/json",
                "X-API-Key": API_SECRET_TOKEN
            }
            payload = {"userPrompt": prompt}

            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            self.send_response(response.status_code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            if response.status_code == 200:
                self.wfile.write(json.dumps(response.json()).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({"error": f"Downstream error: {response.text}"}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
