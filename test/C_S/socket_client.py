#导入模块
import socket
import threading

#定义实例
sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#定义链接的服务器
send_ip_port = ("127.0.0.1", 8888)

#定义自己的IP地址
my_ip_port = ("127.0.0.1", 8887)
sk.bind(my_ip_port)


def receive_message():
    while True:
        data = sk.recv(1024)
        print(data)

def send_message():
    while True:
        msg_input = input("请输入发送的消息:")
        if msg_input == "exit":
            return

        sk.sendto(msg_input.encode(),send_ip_port)

    sk.close()

#循环数据的输入
# while True:
#     #输入发送的信息
#     msg_input = input("请输入发送的消息:")
#     if msg_input == "exit":
#         break

#     sk.sendto(msg_input.encode(),ip_port)

#     #如果发送数据则接收数据
#     if msg_input:
#         #接收数据
#         data = sk.recv(1024)
#         print(data)

def main():
    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()
    send_message()


if __name__ == '__main__':
    main()