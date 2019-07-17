import socket
import StringIO
import sys


class WSGIServer(object):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self, server_address):
        self.listening_socket = listen_socket = socket.socket(
            self.address_family,
            self.socket_type,
        )

        # why are we reassigning things so liberally?
        # why is this not just self.listen_socket??
        listen_socket.bind(server_address)
        listen_socket.listen(self.request_queue_size)

        print('getting the sock name yields: ', listen_socket.getsockname())
        host, port = self.listening_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.headers_set = []
        print('server name and port are ', self.server_name, self.server_port)


    def set_app(self, application):
        self.application = application

    
    def serve_forever(self):
        listen_socket = self.listening_socket
        while True:
            self.client_connection, client_address = listen_socket.accept()
            print('client address is ', client_address)
            self.handle_one_request()
    
    def handle_one_request(self):
        self.request_data = request_data = self.client_connection.recv(1024)
        print "request data is ", request_data
        print(''.join(
            '< {line}\n'.format(line=line)
            for line in request_data.splitlines()
        ))
        print('Now going to parse the request data')
        # pull out the request method, path, and version
        self.parse_request(request_data)

        env = self.get_environ()
        result = self.application(env, self.start_response)

        self.finish_response(result)

    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date', 'Tue, 10 June 2019 5:55:55 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        print 'headers look as so ', response_headers, server_headers
        self.headers_set = [status, response_headers + server_headers]
    
    def finish_response(self, result):
        print 'result is ', result
        
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data
            print(''.join(
                '> {line}\n'.format(line=line)
                for line in response.splitlines()
            ))
            self.client_connection.sendall(response)
        finally:
            self.client_connection.close()  



    def get_environ(self):
        env = {}
        env['wsgi.version'] = (1,0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = StringIO.StringIO(self.request_data)
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        env['REQUEST_METHOD'] = self.request_method
        env['PATH_INFO'] = self.path
        env['SERVER_NAME'] = self.server_name
        env['SERVER_PORT'] = str(self.server_port)
        return env
    
        
    
    def parse_request(self, text):
        print('going to split this up',text )
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        print('now looks like thisss ', request_line)
        (
            self.request_method, 
            self.path, 
            self.request_version
        ) = request_line.split()

SERVER_ADDRESS = (HOST, PORT) = '', 8889

    
def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Nooopes. Please provide a WSGI object as module:callable')
    app_path = sys.argv[1]
    print "app path is ", app_path

    module, application = app_path.split(':')
    print " so module is ", module
    print "and applicatio is ", application

    module = __import__(module)
    application = getattr(module, application)
    print('wtf is this thing now?')
    print('new module is ', module)
    print('and new application is ', application)

    httpd = make_server(SERVER_ADDRESS, application)
    print('WSGIServer: Serving HTTP on port {port} ...\n'.format(port=PORT))
    httpd.serve_forever()