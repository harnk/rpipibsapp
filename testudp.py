import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

address = ('',5002)
sock.bind(address)

while True:
    data,addr = sock.recvfrom(1024)
    print data
    print addr

