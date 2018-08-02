import socket
import datetime
import time
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.sendto('{"id":"10.2.1.211","lat":41.699799,"lng":-86.237534,"alt":562}', ('10.2.1.255', 5002))

sock.sendto('Direct msg to 10.2.1.14', ('10.2.1.14',5002))
while True:
    sock.sendto('BROADCASTED MSG: {"id":"mac99","lat":41.699,"lng":-86.237,"alt":'+str(random.randint(500,801))+',"time":"'+ str(datetime.datetime.utcnow()) +' UTC"}', ('10.2.1.255', 5002))
    time.sleep(0.5)
