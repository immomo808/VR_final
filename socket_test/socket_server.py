import socket, sys, os

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    os.remove("tmp")
except OSError:
    pass

sock.bind('tmp')
sock.listen(1)

(conn, adr) = sock.accept()
while 1:
    data = ""
    while len(data) < 180*320*3:
        msg = conn.recv(min(1024, 180*320*3-len(data)))
        data += msg

    while data:
        conn.send(data[:1024])
        data = data[1024:]
conn.close()
