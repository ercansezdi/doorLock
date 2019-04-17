import socket
host = "192.168.59.53"
port = 9879
buffer_size = 1024
text = "160711004,Ercan Sezdi,12 34 65 87"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
text = text.encode('utf-8')
s.send(text)
#data = s.recv(buffer_size) #alinan veri
s.close()
