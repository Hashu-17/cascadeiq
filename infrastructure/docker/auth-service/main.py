import random
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if random.random() < 0.25:
            self.send_response(503)
            self.end_headers()
            self.wfile.write(b'auth degraded')
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'auth ok')

def main():
    server = HTTPServer(('0.0.0.0', 9002), Handler)
    server.serve_forever()

if __name__ == '__main__':
    main()
