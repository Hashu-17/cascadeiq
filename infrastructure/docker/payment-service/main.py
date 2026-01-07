import random
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if random.random() < 0.3:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'payment error')
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'payment ok')

def main():
    server = HTTPServer(('0.0.0.0', 9001), Handler)
    server.serve_forever()

if __name__ == '__main__':
    main()
