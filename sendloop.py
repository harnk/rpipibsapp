import socket
import datetime
import time
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# sock.sendto('{"id":"10.2.1.211","lat":41.699799,"lng":-86.237534,"alt":562}', ('10.2.1.255', 5002))

# sock.sendto('Direct msg to 10.2.1.3', ('10.2.1.14',5002))
while True:
    # sock.sendto('BROADCASTED MSG: {"id":"mac99","lat":41.699,"lng":-86.237,"alt":'+str(random.randint(500,801))+',"time":"'+ str(datetime.datetime.utcnow()) +' UTC"}', ('10.2.1.255', 5002))
    sock.sendto(
        '{"pibs_payload":{"source_id":"RPI.11","uav_class":"???","current_position":[41.6,-86.2,562],"generation_time":' + str(
            time.time()) + ',"heading":[[41.7,-87.1,500],[41.8,-87.3,500]],"resolution_advisory_flag":false,"emergency_flag":false}}',
        ('10.2.1.255', 5002))
    time.sleep(3)

