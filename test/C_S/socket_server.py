#导入模块
import socket
import threading

#创建实例
sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#定义ip地址
ip_port = ("127.0.0.1",8888)
#绑定监听
sk.bind(ip_port)
#不断循环接收数据

#定义发送数据
send_ip_port = ("127.0.0.1", 8887)

def receive_message():
    while True:
        data = sk.recv(1024)    #sk.recvfrom(1024)返回数据和地址

        print(data)

def send_message():
    while True:
        #接收数据
        #如果接收到数据则发送数据
        msg_input = input("请输入发送的消息:")
        if msg_input == "exit":
            break

        sk.sendto(msg_input.encode(),send_ip_port)

def main():
    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()
    send_message()

if __name__ == '__main__':
    main()
