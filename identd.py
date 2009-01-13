
import socket

host = ''
port = 113

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

conn, addr = s.accept()
print 'somebodys here %s %s' % (str(conn), str(addr))
print conn.recv(1024)
conn.close()


