import http.server
import socketserver
import os
import sys

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, api_port=5000, **kwargs):
        self.api_port = api_port
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            # Read the index.html file
            with open("index.html", "r") as f:
                content = f.read()
            
            # Inject API_PORT into the HTML
            content = content.replace(
                "const API_PORT = window.API_PORT || 5000;",
                f"const API_PORT = {self.api_port};"
            )
            
            # Send response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode())
        else:
            super().do_GET()

def serve_frontend(port, api_port):
    """
    Serve the frontend static files on the specified port.
    """
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    os.chdir(static_dir)

    retries = 3
    while retries > 0:
        try:
            handler = lambda *args, **kwargs: CustomHandler(*args, api_port=api_port, **kwargs)
            with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
                print(f"Serving frontend at http://0.0.0.0:{port} (API port: {api_port})")
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\nShutting down frontend server...")
                    httpd.shutdown()
            break
        except OSError as e:
            if e.errno == 98:  # Address already in use
                print(f"Port {port} is in use, waiting for it to be available...")
                retries -= 1
                if retries == 0:
                    raise
                import time
                time.sleep(2)
            else:
                raise

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    api_port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    serve_frontend(port, api_port)
