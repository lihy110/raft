from server.Server import *
from server.Message import *
import threading

class Client:
    """
    客户端类
    """
    def __init__(self):
        #客户端配置
        self.id = 1
        self.port = 6000
        self.host = 'localhost'
        self.leader = None
        
        self.server = Server(self.port)
        self.server.initialise()

        #访问领导者配置
        self.leader = 1
        self.leader_port = 3001
        self.leader_host = 'localhost'

        self.Stop = True
        self.last_append_entry = None  # 添加用来存储最后一次添加的内容

        #启用消息接收线程
        state_handling_thread = threading.Thread(target=self.start_recive)
        state_handling_thread.start()


    def run(self):
        print("欢迎使用Raft协议！")
        print("1. 查询")
        print("2. 添加")
        print("3. 退出")
        while True:
            command = input("请输入指令: ")
            if command == "1":      # 查询
                address = {"port":self.port, "host":self.host}
                Message = ClientRequestMessage(self.id ,address)
                self.server.send(self.leader_port, self.leader_host, Message)
                
            elif command == "2":    # 添加
                message = input("请输入添加的内容: ")
                self.last_append_entry = message
                address = {"port":self.port, "host":self.host}
                Message = ClientAppendEntriesMessage(message, self.id, address)
                self.server.send(self.leader_port, self.leader_host, Message)
                
            elif command == "3":    # 退出
                self.Stop = False
                break

    def start_recive(self):
        """
        启动消息接收
        """
        while True:
            msg = self.server.receive()     # 接收消息
            if msg != None:
                self.handle(msg)            # 处理消息
                print(msg)                  # 输出消息
            elif self.Stop == False:        # 当输入为3时，退出
                return 
            else:
                pass

    def handle(self, msg):##############
        """
        处理消息
        :param msg: 消息
        """
        if isinstance(msg, ClientResponseMessage):
            msg = msg.serialize()
            print(msg)
            print()
        elif isinstance(msg, ClientAppendEntriesResponseMessage):
            msg = msg.serialize()
            print(msg)
            print()
        elif isinstance(msg, ClientRedirectMessage):
            msg = msg.serialize()
            print("发现新领导者，正在重定向...。新领导为：" + str(msg['currentLeader']))
            self.leader = msg['currentLeader']
            self.leader_port = msg['port']
            self.leader_host = msg['host']
            if msg['type'] == "ClientRequestMessage":
                address = {"port":self.port, "host":self.host}
                Message = ClientRequestMessage(self.id ,address)
                self.server.send(self.leader_port, self.leader_host, Message)
            elif msg['type'] == "ClientAppendEntriesMessage":
                address = {"port":self.port, "host":self.host}
                message = self.last_append_entry
                Message = ClientAppendEntriesMessage(message, self.id, address)
                self.server.send(self.leader_port, self.leader_host, Message)
            else:
                assert False, "Unknown redirectMessage type"
        else:
            assert False, "Unknown message type"

if __name__ == '__main__':
    client = Client()
    client.run()