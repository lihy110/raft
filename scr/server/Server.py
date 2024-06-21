import socket
import pickle

class Server (object):
    def __init__(self, port, host='localhost'):
        if port is None:
            raise ValueError("Port is None")
        self.port = port
        self.host = host


    def initialise(self):
        self.accepter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.accepter.setblocking(False)    #设置非阻塞
        self.accepter.bind((self.host, self.port))


    def receive(self):
        """
        接收数据
        :return: data
        """
        try:
            data= self.accepter.recv(1024)
            # print(data.decode())
            data = pickle.loads(data)
            
            return data
        except Exception as e:
            # print(f"Receive error: {e}")
            # return False
            pass

    def send(self, port, addr='localhost', data = None):
        """
        发送数据
        :param port: 端口
        :param addr: 地址
        :param data: 数据，默认为None
        :return: bool
        """
        if data is None:
            print("No data to send.")
            return False
        try:
            data_bytes = pickle.dumps(data)
            self.accepter.sendto(data_bytes, (addr, port))
            return True
        except Exception as e:
            print(f"Send error: {e}")
            return False
        
    def broadcast(self, other_peers, data):
        """
        广播数据
        :param other_peers: 其他节点
        :param data: 数据
        """
        try:
            for node in other_peers:
                data_bytes = pickle.dumps(data)
                self.accepter.sendto(data_bytes , (node["host"], node["port"]))
        except Exception as e:
            # print(f"Broadcast error: {e} {node}")
            # return False
            pass
        
    # def receive(self):
    #     while self.exit_program:
    #         try:
    #             data= self.accepter.recv(1024)
    #             print(data.decode())
                
    #         except Exception as e:
    #             print(f"Receive error: {e}")
    #             break
    