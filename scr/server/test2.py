import threading
from Server import Server 

datas = {
    "name": "peer1",
    "port": 8888,
    "status": "leader",
    "type": "election",
    "data": ""
}

def main(host, port):
    server = Server(port, host)
    server.initialise()         #初始化
    receive_thread = threading.Thread(target=server.receive)
    receive_thread.start()
    while True:
        text = input("请输入: ")
        if text == "exit":
            datas["data"] = text
            server.stop_event()
            break
        else: 
            datas["data"] = text
            server.send(8887, host, datas)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8888
    main(host, port)