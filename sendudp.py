import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.sendto('A new message Blasting to 10.2.1.255', ('10.2.1.255', 5002))

sock.sendto('Sending directly to 10.2.1.14', ('10.2.1.14',5002))
