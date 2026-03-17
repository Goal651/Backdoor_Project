#!/usr/bin/env python3
"""
Local Server for Backdoor Snake Game
Place in: backdoor-snake-game/server/server.py
Run first: python server.py
"""

import http.server
import socketserver
import os
import json
import urllib.parse
from pathlib import Path

PORT = 8080
DEPENDENCIES_DIR = "dependencies"

class DependencyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the path
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Handle root path
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
            <html>
                <head>
                    <title>Backdoor Snake Game Server</title>
                    <style>
                        body { font-family: Arial; margin: 40px; background: #f0f0f0; }
                        h1 { color: #333; }
                        h2 { color: #666; }
                        ul { list-style-type: none; padding: 0; }
                        li { margin: 10px 0; }
                        a { background: #fff; padding: 10px; border-radius: 5px; 
                           text-decoration: none; color: #0066cc; display: inline-block; width: 400px; }
                        a:hover { background: #e6e6e6; }
                        .small { font-size: 0.9em; color: #666; }
                    </style>
                </head>
                <body>
                    <h1>Backdoor Snake Game Dependency Server</h1>
                    <p>Server is running. Available endpoints:</p>
                    <ul>
                        <li><a href="/check-deps">/check-deps</a> <span class="small">- Check required dependencies</span></li>
                        <li><a href="/list-deps">/list-deps</a> <span class="small">- List available dependencies</span></li>
                        <li><a href="/dependencies/">/dependencies/</a> <span class="small">- Download dependencies</span></li>
                    </ul>
                    <h2>Available Dependencies:</h2>
                    <ul>
            """)
            
            # List available files in dependencies directory
            if os.path.exists(DEPENDENCIES_DIR):
                for file in os.listdir(DEPENDENCIES_DIR):
                    if file.endswith(('.whl', '.exe', '.msi', '.txt')):
                        file_path = os.path.join(DEPENDENCIES_DIR, file)
                        if os.path.isfile(file_path):
                            file_size = os.path.getsize(file_path)
                            size_mb = file_size / (1024 * 1024)
                            self.wfile.write(f'<li><a href="/dependencies/{file}">{file}</a> <span class="small">({size_mb:.2f} MB)</span></li>\n'.encode())
            
            self.wfile.write(b"""
                    </ul>
                    <p><small>Server running on port 8080</small></p>
                </body>
            </html>
            """)
            return
        
        # Handle check-deps endpoint
        elif path == '/check-deps':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Get Python version to suggest correct pygame wheel
            import sys
            py_version = f"{sys.version_info.major}{sys.version_info.minor}"
            
            deps = {
                "required": ["pygame", "requests"],
                "versions": {
                    "pygame": "2.6.1",
                    "requests": "2.31.0"
                },
                "urls": {
                    "pygame": f"http://localhost:{PORT}/dependencies/pygame-2.6.1-cp{py_version}-cp{py_version}-win_amd64.whl",
                    "requests": f"http://localhost:{PORT}/dependencies/requests-2.32.5-py3-none-any.whl"
                },
                "alternate_urls": {
                    "pygame": [
                        f"http://localhost:{PORT}/dependencies/pygame-2.6.1-cp{py_version}-cp{py_version}-win32.whl",
                        f"http://localhost:{PORT}/dependencies/pygame-2.6.1-cp39-cp39-win_amd64.whl",
                        f"http://localhost:{PORT}/dependencies/pygame-2.6.1-cp310-cp310-win_amd64.whl",
                        f"http://localhost:{PORT}/dependencies/pygame-2.6.1-cp311-cp311-win_amd64.whl",
                        f"http://localhost:{PORT}/dependencies/pygame-2.6.1-cp312-cp312-win_amd64.whl"
                    ]
                }
            }
            self.wfile.write(json.dumps(deps, indent=2).encode())
            return
        
        # Handle list-deps endpoint
        elif path == '/list-deps':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            files = []
            if os.path.exists(DEPENDENCIES_DIR):
                for file in os.listdir(DEPENDENCIES_DIR):
                    file_path = os.path.join(DEPENDENCIES_DIR, file)
                    if os.path.isfile(file_path):
                        files.append({
                            "name": file,
                            "size": os.path.getsize(file_path),
                            "url": f"/dependencies/{file}"
                        })
            
            self.wfile.write(json.dumps({"files": files}, indent=2).encode())
            return
        
        # Handle file downloads
        elif path.startswith('/dependencies/'):
            filename = path.replace('/dependencies/', '')
            
            # Prevent directory traversal attacks
            filename = os.path.basename(filename)
            if not filename:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Bad Request")
                return
            
            filepath = os.path.join(DEPENDENCIES_DIR, filename)
            
            # Check if file exists and is a file (not a directory)
            if os.path.exists(filepath) and os.path.isfile(filepath):
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.send_header('Content-Length', str(os.path.getsize(filepath)))
                self.end_headers()
                
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                # Create error page
                error_html = f"""
                <html>
                    <head><title>404 Not Found</title></head>
                    <body>
                        <h1>404 - File Not Found</h1>
                        <p>The file <strong>{filename}</strong> was not found in the dependencies directory.</p>
                        <p>Available files:</p>
                        <ul>
                """
                
                self.wfile.write(error_html.encode())
                
                # List available files
                if os.path.exists(DEPENDENCIES_DIR):
                    for f in os.listdir(DEPENDENCIES_DIR):
                        f_path = os.path.join(DEPENDENCIES_DIR, f)
                        if os.path.isfile(f_path):
                            self.wfile.write(f'<li><a href="/dependencies/{f}">{f}</a></li>'.encode())
                
                self.wfile.write(b"""
                        </ul>
                        <p><a href="/">Back to home</a></p>
                    </body>
                </html>
                """)
                return
        
        # Handle favicon.ico
        elif path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return
        
        # Default response for other paths
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>404 Not Found</h1><p>The requested path was not found.</p><p><a href='/'>Go to home</a></p>")

def setup_dependencies():
    """Create dependencies directory and files"""
    Path(DEPENDENCIES_DIR).mkdir(exist_ok=True)
    
    # Create requirements.txt
    req_path = os.path.join(DEPENDENCIES_DIR, 'requirements.txt')
    with open(req_path, 'w') as f:
        f.write("pygame==2.6.1\nrequests==2.32.5\n")
    
    print("=" * 60)
    print("BACKDOOR SNAKE GAME - DEPENDENCY SERVER")
    print("=" * 60)
    print()
    print(f"Dependencies directory: {os.path.abspath(DEPENDENCIES_DIR)}")
    print()
    print("REQUIRED FILES - Download and place in the directory above:")
    print()
    print("1. PYGAME (choose one for your Python version):")
    print("   - Python 3.9:  pygame-2.6.1-cp39-cp39-win_amd64.whl")
    print("   - Python 3.10: pygame-2.6.1-cp310-cp310-win_amd64.whl")
    print("   - Python 3.11: pygame-2.6.1-cp311-cp311-win_amd64.whl")
    print("   - Python 3.12: pygame-2.6.1-cp312-cp312-win_amd64.whl")
    print()
    print("   Download from: https://pypi.org/project/pygame/#files")
    print()
    print("2. REQUESTS (any Python 3 version):")
    print("   -requests-2.32.5-py3-none-any.whl")
    print()
    print("   Download from: https://pypi.org/project/requests/#files")
    print()
    print("To check your Python version: python --version")
    print()
    print("Server URLs:")
    print("  - Home:         http://localhost:8080")
    print("  - Check deps:   http://localhost:8080/check-deps")
    print("  - List files:   http://localhost:8080/list-deps")
    print("  - Dependencies: http://localhost:8080/dependencies/")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)

def run_server():
    """Run the HTTP server"""
    handler = DependencyHandler
    
    # Allow reuse of address
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"\nServer started at http://localhost:{PORT}")
        print(f"Serving dependencies from: {os.path.abspath(DEPENDENCIES_DIR)}")
        
        # Show available files
        if os.path.exists(DEPENDENCIES_DIR):
            files = [f for f in os.listdir(DEPENDENCIES_DIR) 
                    if os.path.isfile(os.path.join(DEPENDENCIES_DIR, f))]
            if files:
                print("\nAvailable files:")
                for f in files:
                    size = os.path.getsize(os.path.join(DEPENDENCIES_DIR, f))
                    print(f"  - {f} ({size/1024/1024:.2f} MB)")
            else:
                print("\nWARNING: No files found in dependencies directory!")
                print("Please download the required wheel files.")
        
        print("\nWaiting for connections...\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == "__main__":
    setup_dependencies()
    run_server()