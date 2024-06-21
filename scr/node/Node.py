import sys
import threading
sys.path.append("..")
from .State import *
from server.Server import *
from .utility import *

class Node():
    """
    节点类
    """
    def __init__(self, config):
        """
        初始化节点
        Entries的因为由Entry组成的数组，其中Entry格式为
        Entry = {
                "Index": len(self.node.Entries) + 1,
                "Term": self.node.term,
                "Data": data
            }
        :param config: 配置信息
        """
        self.config = None
        self.port = None
        self.host = None
        # self.Server = Server(self.config.port)

        ##节点状态
        self.user_ID = None
        self.name = None
        self.currentTerm = 0
        self.commitIndex = 0
        self.lastApplied = 0
        self.Entries = []
        self.other_peers = []

        #读取配置
        self.configure(config)

        ##节点间通信
        self.server = Server(self.port)
        self.server.initialise()
        state_handling_thread = threading.Thread(target=self.start_state_handling)
        state_handling_thread.start()

        ##计时器
        self.timer = timer()
        state_handling_thread = threading.Thread(target=self.timeout)
        state_handling_thread.start()

        ##节点角色
        self.state = Follower(self)

    def configure(self, config):
        """
        配置节点
        :param config: 配置
        """
        self.config = config
        self.user_ID = config["node_ID"]
        self.name = config["name"]
        self.port = config["port"]
        self.host = config["host"]
        self.other_peers = config["other_peers"]

    def start_state_handling(self):
        """
        启动状态处理循环
        """
        while True:
            msg = self.server.receive()     # 接收消息
            if msg != None:
                print(f"Node {self.user_ID} received message: {msg}")
                self.state.handle(msg)      # 处理消息
            else:
                pass    # 暂时不做处理

    def timeout(self):
        """
        超时处理
        """
        while True:
            if self.timer.timer_function():
                self.state.timeout()
                self.timer.restart_timer()

    def apply_commits(self, commitIndex = None):
        """
        应用提交
        :param commitIndex: 提交索引，默认为None
        """
        while self.commitIndex > self.lastApplied:
            print(f"Apply commit {self.lastApplied}")       #模拟应用提交
            self.lastApplied += 1

    def get_lastLogs_info(self, n = 1):
        """
        获取最后第n个日志的索引和任期
        :param n: 1:返回最后n个日志的索引和任期，默认为1
        :return: lastLogsIndex, lastLogsTerm
        """
        if len(self.Entries) == 0:
            return 0, 0
        else:
            return self.Entries[-n]["Index"], self.Entries[-n]["Term"]
        
    def get_log_term(self, index):
        """
        获取日志的任期，并判断日志是否存在
        :param index: 日志索引
        :return: term
        """
        if index == 0 or index > len(self.Entries) or index != self.Entries[index - 1]["Index"]:
            return False
        else:
            return self.Entries[index - 1]["Term"]
        
    def get_address(self, Id):
        """
        获取其他的地址
        :param Id: 领导者ID
        :return: host, port
        """
        for node in self.other_peers:
            if node["node_ID"] == Id:
                return node["host"], node["port"]
        return False
    
    def get_log_data(self, index):
        """
        获取日志数据
        :param index: 日志索引
        :return: data
        """
        # 如果日志不存在或者日志索引不正确返回False
        if index == 0 or index > len(self.Entries) or index != self.Entries[index - 1]["Index"]:
            return False
        else:
            return self.Entries[index - 1]["Data"]

def main():
    path = "../peer1_config.json"
    config = peer.load_config(path)        
    print("Successfully loaded config!!!")
    n = Node(config)
    n.state.switch_to_candidate()
    n.state.timeout()

if __name__ == '__main__':
    main()