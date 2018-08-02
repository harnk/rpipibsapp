import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.sendto('{"id":"10.2.1.99","lat":41.699799,"lng":-86.237534,"alt":562,"intent":"going somewhere fast"}', ('10.2.1.255', 5002))

sock.sendto('Sending right to 10.2.1.14', ('10.2.1.14',5002))
