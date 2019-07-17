import socket

HOST, PORT = '', 8889

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

print 'Serving HTTP on port %s ...' % PORT


while True:
    client_connection, client_address = listen_socket.accept()
    print 'COnnected to',  client_address
    request = client_connection.recv(1024)
    print 'request is '
    print "*" * 5
    print request
    print '*' * 5
    http_response = """\
HTTP/1.1 200 OK

Suuuuup Yo!
"""
    client_connection.sendall(http_response)
    
    client_connection.close()

# why you no work?

# # echo client program
# listen_socket.connect((HOST, PORT))
# listen_socket.sendall('Hello, world')
# data = listen_socket.recv(1024)
# s.close()
# print 'Received', repr(data)