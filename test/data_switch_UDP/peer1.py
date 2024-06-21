#导入模块
import socket
import threading
import json

#定义实例
sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#定义链接的服务器
send_ip_port = ("127.0.0.1", 8888)

#定义自己的IP地址
my_ip_port = ("127.0.0.1", 8887)
sk.bind(my_ip_port)

datas = {
    "name": "peer1",
    "port": 8887,
    "status": "leader",
    "type": "election",
    "data": "hello"
}

exit_program = False

def receive_message():
    global exit_program
    while not exit_program:
        try:
            data = sk.recv(1024)
            print(data.decode())
            if data == b'exit':
                exit_program = True
                break
            json_data = json.loads(data)        #str转换为dict
            if json_data["type"] == "election":     #接收到投票信息
                print("Received election message")
                reply = {
                    "name": "peer1",
                    "port": 8887,
                    "type": "reply",
                    "data": "true"
                }
                sk.sendto(json.dumps(reply).encode(), send_ip_port)
        except KeyboardInterrupt:
            exit_program = True
            # 发送退出消息给服务器
            sk.sendto("exit".encode(), send_ip_port)
            break

def send_message():
    global exit_program
    while not exit_program:
        try:
            msg_input = input("请输入发送的消息:")

            if msg_input == "2":        #输入2发送data信息
                print("Sending heartbeat")
                sk.sendto(json.dumps(datas).encode(), send_ip_port)
            else:
                sk.sendto(msg_input.encode(), send_ip_port)
        except KeyboardInterrupt:
            exit_program = True
            sk.sendto("exit".encode(), send_ip_port)
            break


def main():
    global exit_program
    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()
    send_message()
    
    receive_thread.join()


if __name__ == '__main__':
    main()
    