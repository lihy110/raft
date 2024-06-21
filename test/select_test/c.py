# coding: utf-8
import socket

messages = ['This is the message ', 'It will be sent ', 'in parts ']

server_address = ('localhost', 8090)

# Create TCP/IP sockets
socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET,  socket.SOCK_STREAM)]

# Connect the sockets to the port where the server is listening
print ('connecting to %s port %s' % server_address)

for s in socks:
    s.connect(server_address)

for index, message in enumerate(messages):
    # Send messages on both sockets
    for s in socks:
        print('%s: sending "%s"' % (s.getsockname(), message + str(index)))
        # 发送消息时直接使用字符串的encode方法将其转换为字节流
        s.send((message + str(index)).encode('utf-8'))
    # Read responses on both sockets

for s in socks:
    data = s.recv(1024)
    print('%s: received "%s"' % (s.getsockname(), data))
    if data != b"":
        print ('closing socket', s.getsockname())
        s.close()
