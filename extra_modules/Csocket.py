import socket
host = '192.168.59.53'
port = 9879
buffer_size = 1024
text = "Hello, World!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
text = text.encode('utf-8')
s.send(text)
data = s.recv(buffer_size)
s.close()
print("received data:", data)
