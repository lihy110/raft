# coding: utf-8
import json
import socket

server_address = ('localhost', 8090)

# Create TCP/IP sockets
socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the sockets to the port where the server is listening
print ('connecting to %s port %s' % server_address)

data = {
    "name": "peer1",
    "port": socket.SOCK_STREAM,
    "type": "leader",
    "data": "hello"
}


socks.connect(server_address)

while 1:
    try:                            
        msg_input = input("请输入发送的消息:")
        
        if msg_input == "2":      #输入2发送data信息
            print("Sending heartbeat")
            socks.send(json.dumps(data).encode())
        else:
            socks.send(msg_input.encode())
    except KeyboardInterrupt:       #抛出异常
        exit_program = True
        socks.close()
        break

for s in socks:
    data = socks.recv(1024)
    print('%s: received "%s"' % (s.getsockname(), data))
    if data != b"":
        print ('closing socket', s.getsockname())
        s.close()