class Message (object):
    def __init__(self):
        pass

class ElectResponseMessage (Message):
    """
    选举响应消息
    """
    def __init__(self, term, voteGranted):
        """
        :param term: 任期
        :param voteGranted: 投票
        :return:
        """
        self.term = term
        self.voteGranted = voteGranted

    def serialize(self):
        data = {
            'term': self.term,
            'voteGranted': self.voteGranted
        }
        return data
    
class ElectRequestMessage (Message):
    """
    选举请求消息
    """
    def __init__(self, candidateId, term, lastLogIndex, lastLogTerm):
        """
        :param candidateId: 候选人ID
        :param term: 任期
        :param lastLogIndex: 最后一个日志的索引
        :param lastLogTerm: 最后一个日志的任期
        :return:
        """
        self.candidateId = candidateId
        self.term = term
        self.lastLogIndex = lastLogIndex
        self.lastLogTerm = lastLogTerm

    def serialize(self):
        data = {
            'candidateId': self.candidateId,
            'term': self.term,
            'lastLogIndex': self.lastLogIndex,
            'lastLogTerm': self.lastLogTerm
        }
        return data
    
class AppendEntriesMessage (Message):
    """
    日志追加消息
    """
    def __init__(self, leaderId, term, prevLogIndex, prevLogTerm, leaderCommit, entries = None ):
        """
        :param leaderId: 领导者ID
        :param term: 任期
        :param prevLogIndex: 前一个日志的索引
        :param prevLogTerm: 前一个日志的任期
        :param leaderCommit: 领导者已知提交最高的日志的索引
        :param entries: 日志条目，即数据
        :return:
        """
        self.leaderId = leaderId
        self.term = term
        self.prevLogIndex = prevLogIndex
        self.prevLogTerm = prevLogTerm
        self.entries = entries
        self.leaderCommit = leaderCommit

    def serialize(self):
        data = {
            'leaderId': self.leaderId,
            'term': self.term,
            'prevLogIndex': self.prevLogIndex,
            'prevLogTerm': self.prevLogTerm,
            'entries': self.entries,
            'leaderCommit': self.leaderCommit
        }
        return data
    
class AppendEntriesResponseMessage (Message):
    """
    日志追加响应消息，由于使用UDP协议因此需要返回node_ID，以便Leader知道是哪个节点的响应
    或使用recvfrom()方法获取响应的地址也可以
    """
    def __init__(self, term, success, node_ID, lastLogIndex):
        """
        :param term: 任期
        :param success: 成功
        :param node_ID: 节点ID
        :param lastLogIndex: 最后一个日志的索引
        :return:
        """
        self.term = term
        self.success = success
        self.node_ID = node_ID
        self.lastLogIndex = lastLogIndex

    def serialize(self):
        data = {
            'term': self.term,
            'success': self.success,
            'node_ID': self.node_ID,
            'lastLogIndex': self.lastLogIndex
        }
        return data
    

#####################客户端消息#####################
class ClientRequestMessage (Message):
    """
    客户端请求消息
    """
    def __init__(self, clientID, clientAddress, command = None):
        """
        :param clientID: 客户ID
        :param clientAddress: 客户地址
        :param command: 命令，默认为None。保留接口，以便扩展
        :return:
        """
        self.clientID = clientID
        self.clientAddress = clientAddress
        self.command = command

    def serialize(self):
        data = {
            'clientID': self.clientID,
            'clientAddress': self.clientAddress,
            'command': self.command
        }
        return data
    
class ClientResponseMessage (Message):
    """
    客户端响应消息
    """
    def __init__(self, state, currentLeader, entries):
        """
        :param state: 获取状态
        :param data: 数据
        :return:
        """
        self.state = state
        self.currentLeader = currentLeader
        self.entries = entries

    def serialize(self):
        data = {
            'state': self.state,
            'currentLeader': self.currentLeader,
            'data': self.entries
        }
        return data
    
class ClientAppendEntriesMessage (Message):
    """
    客户端日志追加消息
    """
    def __init__(self, entries, clientID, clientAddress):
        """
        :param entries: 日志条目，即数据
        :param clientID: 客户ID
        :param clientAddress: 客户地址
        :return:
        """
        self.entries = entries
        self.clientID = clientID
        self.clientAddress = clientAddress


    def serialize(self):
        data = {
            'entries': self.entries,
            'clientID': self.clientID,
            'clientAddress': self.clientAddress
        }
        return data
    
class ClientAppendEntriesResponseMessage (Message):
    """
    客户端日志追加响应消息
    """
    def __init__(self, state, lastLogIndex):
        """
        :param state: 追加状态
        :param lastLogIndex: 最后一个日志的索引
        :return:
        """
        self.state = state
        self.lastLogIndex = lastLogIndex

    def serialize(self):
        data = {
            'state': self.state,
            'lastLogIndex': self.lastLogIndex
        }
        return data
    
class ClientRedirectMessage (Message):
    """
    客户端重定向消息
    """
    def __init__(self, type, currentLeader, port, host):
        """
        :param type: 之前发送消息的类型
        :param currentLeader: 当前领导者
        :param port: 领导者端口
        :param host: 领导者地址
        :return:
        """
        self.type = type
        self.currentLeader = currentLeader
        self.port = port
        self.host = host

    def serialize(self):
        data = {
            'type': self.type,
            'currentLeader': self.currentLeader,
            'port': self.port,
            'host': self.host
        }
        return data