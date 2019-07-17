import socket
import os
import time


HOST = ''
PORT = 8888
SERVER_ADDRESS = (HOST, PORT)
QUEUE_SIZE = 1


def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(
        'Child PID: {pid}. Parent PID {ppid}'.format(
            pid=os.getpid(),
            ppid=os.getppid(),
        )
    )
    print(request.decode())
    http_response = """
HTTP/1.1 200 OK

yo - we bout to handle alllll the requests...or at least 5
    """
    client_connection.sendall(http_response)
    time.sleep(10)

def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(QUEUE_SIZE)
    print("Servin up HTTP goodnes at %s..." % PORT)
    print("Parent PID (PPID): %s \n" % os.getpid())
    
    while True:
        print "hi"
        client_connection, client_address = listen_socket.accept()
        print "client address is", client_address
        pid = os.fork()
        print "pid is ", pid

        if pid == 0:
            print "pid is 0 here"
            listen_socket.close()
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)
        else:
            
            print "pid is not 0 here", pid
            client_connection.close()

if __name__ == "__main__":
    serve_forever()

