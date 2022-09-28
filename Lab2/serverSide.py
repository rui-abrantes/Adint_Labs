from socket import *
import aux_functions
import json 

s =socket(AF_INET,SOCK_DGRAM)
host = '0.0.0.0'
port = 12350
s.bind((host, port))

print(host, port)
while True:
    data, addr = s.recvfrom(512)
    print('recv', addr)
    print(data)
    my_dict = aux_functions.count_digit(str(data))

    json_s = json.dumps(my_dict)

    s.sendto( json_s.encode() , addr)

s.close()