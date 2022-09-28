import json
from socket import *
s =socket(AF_INET,SOCK_DGRAM)
host = '0.0.0.0'
port = 12351
s.bind((host, port))

s_addr = ('127.0.0.1', 12350)

s.sendto(b'1234', s_addr)

data = s.recv(512)
json_r = json.loads(data)
print (data)
s.close