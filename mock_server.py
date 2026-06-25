#!/usr/bin/env python3
"""HTTP Mock Server."""
import json
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional

class MockHandler(BaseHTTPRequestHandler):
    routes = []
    request_log = []
    
    def _find_route(self):
        for route in self.routes:
            if (route["method"] == self.command and 
                route["path"] == self.path):
                return route
        return None
    
    def _handle_request(self):
        MockHandler.request_log.append({
            "method": self.command,
            "path": self.path,
        })
        
        route = self._find_route()
        if route:
            status = route.get("status", 200)
            body = route.get("body", {})
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(body).encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "No mock found"}).encode())
    
    def do_GET(self): self._handle_request()
    def do_POST(self): self._handle_request()
    def do_PUT(self): self._handle_request()
    def do_DELETE(self): self._handle_request()
    def log_message(self, format, *args): pass

def start_server(config_path: str, port: int = 8080):
    with open(config_path) as f:
        config = json.load(f)
    MockHandler.routes = config.get("routes", [])
    server = HTTPServer(("0.0.0.0", port), MockHandler)
    print(f"Mock server on port {port} with {len(MockHandler.routes)} routes")
    server.serve_forever()

def main():
    parser = argparse.ArgumentParser(description="HTTP Mock Server")
    parser.add_argument("command", choices=["start"])
    parser.add_argument("--config", required=True)
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    start_server(args.config, args.port)

if __name__ == "__main__":
    main()
