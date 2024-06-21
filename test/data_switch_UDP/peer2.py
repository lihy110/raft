#导入模块
import socket
import threading
import json

#创建实例
sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#定义ip地址
ip_port = ("127.0.0.1",8888)
#绑定监听
sk.bind(ip_port)
#不断循环接收数据

#定义发送数据
send_ip_port = ("127.0.0.1", 8887)

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
            data = sk.recv(1024)       #接受信息
            print(data.decode())       #打印信息
            if data == b'exit':        #接收到exit退出
                exit_program = True
                break
            json_data = json.loads(data)       #str转换为dict
            if json_data["type"] == "election":         #接收到投票信息
                print("Received election message")
                reply = {
                    "name": "peer1",
                    "port": 8887,
                    "type": "reply",
                    "data": "true"
                }
                sk.sendto(json.dumps(reply).encode(), send_ip_port)
            elif json_data["type"] == "reply":      #接收到回复信息
                print("Received reply message")
                
        except KeyboardInterrupt:       #抛出异常
            exit_program = True
            # 发送退出消息给服务器
            sk.sendto("exit".encode(), send_ip_port)
            break

def send_message():
    global exit_program
    while not exit_program:
        try:                            
            msg_input = input("请输入发送的消息:")
            
            if msg_input == "2":      #输入2发送data信息
                print("Sending heartbeat")
                sk.sendto(json.dumps(datas).encode(), send_ip_port)
            else:
                sk.sendto(msg_input.encode(), send_ip_port)
        except KeyboardInterrupt:       #抛出异常
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