#!/usr/bin/env python3
"""
Simple HTTP server to view the results dashboard.
Opens the dashboard in your default browser.
"""
import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    # Check if results file exists
    if not os.path.exists('experiment_results.json'):
        print("❌ Error: experiment_results.json not found!")
        print("   Please run the experiment first: python toon_vs_json_experiment.py")
        return
    
    # Check if dashboard exists
    if not os.path.exists('results_dashboard.html'):
        print("❌ Error: results_dashboard.html not found!")
        return
    
    # Start server
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}/results_dashboard.html"
        print(f"\n🌐 Starting server on http://localhost:{PORT}")
        print(f"📊 Opening dashboard: {url}")
        print(f"   (Press Ctrl+C to stop the server)\n")
        
        # Open browser
        webbrowser.open(url)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped.")

if __name__ == "__main__":
    main()


