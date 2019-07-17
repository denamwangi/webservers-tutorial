import BaseHTTPServer

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''handle incoming requests by returning a static page'''
    page = '''\
        <html>
            <body>
                <h1>Suuuuuuup Yo!</h1>
            </body>
        </html>
    '''

    # Handle GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(self.page)))
        # adds whitespace that says hey headers are done
        self.end_headers()
        self.wfile.write(self.page)

if __name__ == "__main__":
    server_address = ('', 8080)
    server = BaseHTTPServer.HTTPServer(server_address, RequestHandler)
    print('Server: Running on port {}'.format(server.server_port))
    server.serve_forever()

