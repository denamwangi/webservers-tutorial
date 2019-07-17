import socket
import time


HOST = ''
PORT = 8888
SERVER_ADDRESS = (HOST, PORT)
REQUEST_QUEUE_SIZE = 5


def handle_request(client_connection):
    request = client_connection.recv(1024)
    http_response = b"""
HTTP/1.1 200 OK

iterative server: suuuuuup
    """
    client_connection.sendall(http_response)
    time.sleep(10)

def serve_forever():
    # set up le socket
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print "serving HTTP goodness on port %s..." % PORT

    while True:
        client_connection, client_address = listen_socket.accept()
        handle_request(client_connection)
        dir(client_connection)
        print("all done")
        client_connection.close()


if __name__ == "__main__":
    serve_forever()