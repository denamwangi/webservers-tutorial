import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
x = sock.connect(('localhost', 8888))
y = sock.getsockname()
print x, y
# import ipdb; ipdb.set_trace()
host, port = sock.getsockname()[:2]
print host, port