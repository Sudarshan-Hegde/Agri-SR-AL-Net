#!/usr/bin/env python3
"""
Simple test server for Geo-Agri Analyst - No dependencies needed!
Run with: python simple_server.py
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse as urlparse

class GeoAgriHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"message": "Geo-Agri Analyst API is running!", "status": "healthy"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/v1/analyze':
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                request_data = json.loads(post_data.decode('utf-8'))
                lat = request_data.get('lat')
                lng = request_data.get('lng')
                
                # Mock response
                response = {
                    "land_class": "Arable Land",
                    "confidence": 0.92,
                    "before_image_b64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
                    "after_image_b64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==",
                    "processing_steps": [
                        "Fetching live satellite imagery...",
                        "Preprocessing satellite data...",
                        "Enhancing image quality with AI...",
                        "Running land classification model...",
                        "Generating final analysis..."
                    ]
                }
                
                print(f"🌍 Analysis request: lat={lat}, lng={lng}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"❌ Error: {e}")
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), GeoAgriHandler)
    print("🚀 Geo-Agri Analyst Test Server starting on http://localhost:8000")
    print("📡 Ready to receive requests from frontend...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.server_close()