import socket, sys, os

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    sock.connect('tmp')
except socket.error, msg:
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    exit(1)

count = 0
import time
dt = time.time()

while 1:
    data_ori = os.urandom(180*320*3)
    data = str(data_ori)
    while data:
        sock.send(data[:1024])
        data = data[1024:]

    data_recv = ""
    while len(data_recv) < 180*320*3:
        temp = sock.recv(min(1024, 180*320*3-len(data_recv)))
        data_recv += temp

    print data_ori == data_recv

    count += 1
    print "%.1f" % (float(count) / (time.time() - dt))
sock.close()
