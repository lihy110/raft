import sys
sys.path.append("..")
from server.Message import *

class State(object):
    """
    节点状态类
    不同状态有不同的表现
    """

    def __init__(self, node):
        self.node = node
        # self.config = _config
        # self.name = self.config['name']
        # self.user_ID = self.config['user_ID']
        # self.port = self.config['port']
        # self.other_peers = self.config['other_peers']

    def handle(self, msg):
        """
        消息处理
        """
        if isinstance(msg, ElectRequestMessage):              #选举请求
            self.on_ElectRequest(msg)
        elif isinstance(msg, ElectResponseMessage):           #选举请求响应
            self.on_ElectResponse(msg)
        elif isinstance(msg, AppendEntriesMessage):           #日志追加
            self.on_AppendEntries(msg)
        elif isinstance(msg, AppendEntriesResponseMessage):   #日志追加响应
            self.on_AppendEntriesResponse(msg)
        elif isinstance(msg, ClientRequestMessage):           #客户端请求
            self.on_ClientRequest(msg)
        elif isinstance(msg, ClientAppendEntriesMessage):     #客户端日志追加  
            self.on_ClientAppendEntries(msg)
        else:
            assert False, "State: Unknown message type"

    def timeout(self):
        """
        超时处理
        """
        pass
    
    def on_ElectRequest(self, msg):
        """
        选举请求处理
        """
        pass

    def on_ElectResponse(self, msg):
        """
        选举响应处理（Candidate状态下的处理）
        """
        pass

    def on_AppendEntries(self, msg):
        """
        日志追加处理(当日志为空时，被用作心跳检测)
        """
        pass

    def on_AppendEntriesResponse(self, msg):
        """
        日志追加响应处理()
        """
        pass

    def on_ClientRequest(self, msg):
        """
        客户端请求处理
        """
        pass

    def on_ClientAppendEntries(self, msg):
        """
        客户端日志追加处理
        """
        pass


class Follower(State):
    def __init__(self, node, voteFor = None, leaderId = None):
        super(Follower, self).__init__(node)
        self.leaderId = leaderId
        self.voteFor = voteFor
        
        self.node.timer.restart_timer(2000, 3000)

    def timeout(self):
        self.switch_to_candidate(self.leaderId)
        print('[Follower：' + str(self.node.user_ID) + '。超时!!! 变为Candidate!!!]')

    def switch_to_candidate(self, leaderId):
        # self.node.timer.restart_timer(3000, 4000)
        self.node.state = Candidate(self.node, leaderId)
        print("[Follower switch to Candidate!!!]")

    def on_ElectRequest(self, msg):
        """
        请求投票处理
        :param msg:收到的消息
        :return:
        """
        msg = msg.serialize()  
        candidateId = msg['candidateId']
        term = msg['term']
        lastLogTerm = msg['lastLogTerm']
        
        # 假设你有方法 get_lastLogs_info() 来获取当前的最后日志信息
        _, lastLogsTerm = self.node.get_lastLogs_info()
        
        # 仅在未投票或收到更高任期的请求时考虑投票
        if (self.voteFor is None or self.node.currentTerm < term) and lastLogsTerm <= lastLogTerm:
            self.node.currentTerm = term  # 更新当前任期
            self.voteFor = candidateId
            msg_response = ElectResponseMessage(self.node.user_ID, True)
            # msg_response = msg_response.serialize()  # 也要序列化响应消息
            
            # 找到候选人信息发送响应
            for peer in self.node.other_peers:
                if peer["node_ID"] == candidateId:
                    self.node.server.send(peer["port"], peer["host"], msg_response)
                    break
                    
            self.node.timer.restart_timer(2000, 3000)
            print(f"[节点{self.node.user_ID}投票给{candidateId}，任期为{term}]")
            return True
        return False
            
    def on_AppendEntries(self, msg):
        """
        日志追加处理
        :param msg:收到的消息，当data(entries)为空时，用作心跳检测
        :return:
        """
        msg = msg.serialize()
        if msg["term"] < self.node.currentTerm:            #如果请求的任期小于当前任期，拒绝请求
            return False

        self.node.timer.restart_timer()                    #对每个有效信息，进行重置计时器

        if self.node.currentTerm < msg["term"]:
            self.node.currentTerm = msg["term"]
            
        if self.leaderId != msg["leaderId"]:           #如果请求的LeaderID不是本地LeaderID，更新LeaderID
            self.leaderId = msg["leaderId"]


        if msg["entries"] == None:                         #心跳检测
            print("[Follower：" + str(self.node.user_ID) + "。接收到心跳检测!!!]")
            # 如果请求的prevLogIndex大于本地日志长度，或者最新日志不匹配，返回lastLogIndex
            if msg["prevLogIndex"] > 0 and (msg["prevLogIndex"] > len(self.node.Entries) or self.node.get_log_term(msg["prevLogIndex"]) != msg["prevLogTerm"]):
                response = AppendEntriesResponseMessage(self.node.currentTerm, False, self.node.user_ID, len(self.node.Entries))
                host, port = self.node.get_address(self.leaderId)                              #获取Leader地址
                self.node.server.send(port, host, response)                             
                return True
            else:
                # self.node.timer.restart_timer()
                return True
        else:                                              #####日志追加
        
            prevLogIndex = msg["prevLogIndex"]
            prevLogTerm = msg["prevLogTerm"]
            host, port = self.node.get_address(self.leaderId)                                   #获取Leader地址

            if prevLogIndex > 0 and prevLogIndex > len(self.node.Entries):                      #如果prevLogIndex大于日志长度，则直接返回lastLogIndex
                response = AppendEntriesResponseMessage(self.node.currentTerm, False, self.node.user_ID, len(self.node.Entries))
                self.node.server.send(port, host, response)
                return False
            elif prevLogIndex > 0 and self.node.get_log_term(prevLogIndex) != prevLogTerm:      #可与上一个if合并
                # 如果不匹配，发送不成功的响应，删除prevLogIndex及其之后的日志
                self.node.Entries = self.node.Entries[:prevLogIndex - 1]
                response = AppendEntriesResponseMessage(self.node.currentTerm, False, self.node.user_ID, len(self.node.Entries))
                
                self.node.server.send(port, host, response)
                return False
            elif prevLogIndex > 0 and self.node.get_log_term(prevLogIndex) == prevLogTerm:      #如果匹配，则删除Follower中Leader日志之后的日志
                self.node.Entries = self.node.Entries[:prevLogIndex]
            
            # # 删除不匹配的日志条目（如果有的话）
            # if prevLogIndex < len(self.node.Entries) and self.node.get_log_term(prevLogIndex) == prevLogTerm:
            #     self.node.Entries = self.node.Entries[:prevLogIndex]
            
            # 追加新的日志条目
            # for entry in msg["entries"]:
            #     self.node.Entries.append(entry)
            Entry = {
                "Index": len(self.node.Entries) + 1,
                "Term": self.node.currentTerm,
                "Data": msg["entries"]
            }
            self.node.Entries.append(Entry)
            print(f"[Follower{self.node.user_ID}添加日志成功，其Index为{Entry['Index']}")
            
            # 如果Leader的commitIndex比本地的大，则更新commitIndex，但不超过已应用到状态机的最大索引
            if(msg["leaderCommit"] > self.node.commitIndex):
                commitIndex = min(msg["leaderCommit"], len(self.node.Entries) - 1)
                self.node.commitIndex = commitIndex
                self.node.apply_commits()           #应用提交

            # 发送成功响应
            response = AppendEntriesResponseMessage(self.node.currentTerm, True, self.node.user_ID, len(self.node.Entries))
            self.node.server.send(port, host, response)
            return True
        
    def on_ClientRequest(self, msg):
        """
        客户端请求处理，返回现在的LeaderID
        :param msg:收到的消息
        :return:
        """
        msg = msg.serialize()
        print("leaderId:", self.leaderId)
        if self.leaderId is not None:     #如果有Leader，则重定向
            leaderHost, leaderPort = self.node.get_address(self.leaderId)
            port, host = msg['clientAddress']['port'], msg['clientAddress']['host']
            print(f"重定向到{leaderPort}，{leaderHost}，{port}，{host}")
            response = ClientRedirectMessage("ClientRequestMessage", self.leaderId, leaderPort, leaderHost)
            self.node.server.send(port, host, response)
        else:
            pass

    def on_ClientAppendEntries(self, msg):
        """
        客户端日志追加处理，返回现在的LeaderID
        :param msg:收到的消息
        :return:
        """
        msg = msg.serialize()
        if self.leaderId is not None:     #如果有Leader，则重定向
            leaderHost, leaderPort = self.node.get_address(self.leaderId)
            port, host = msg['clientAddress']['port'], msg['clientAddress']['host']
            response = ClientRedirectMessage("ClientAppendEntriesMessage", self.leaderId, leaderPort, leaderHost)
            self.node.server.send(port, host, response)
        else:
            pass
        

class Candidate(State):
    def __init__(self, node, leaderId):
        super(Candidate, self).__init__(node)
        self.votes = 0          #选票数
        self.voteFor = None     #投票对象
        self.leaderId = leaderId

        self.node.timer.restart_timer(3000, 4000)

    def timeout(self):
        """
        超时处理,重置计时器,重新开始选举
        """
        self.node.timer.restart_timer(3000, 4000)   #重置计时器
        #####################################开始选举
        self.Elect()                             #重新开始选举
        print('[候选者' + str(self.node.user_ID) + '开始选举!!!]')
    
    def switch_to_leader(self):
        """
        切换到Leader状态
        """
        self.node.state = Leader(self.node)
        print("[Candidate成为Leader!!!]")

    def switch_to_Follower(self, voteFor = None, leaderId = None):
        """
        切换到Follower状态,重置计时器
        """
        # self.node.timer.restart_timer(2000, 3000)
        self.node.state = Follower(self.node, voteFor, leaderId)
        print("[Candidate switch to Follower!!!]")

    def Elect(self):
        """
        选举
        """
        #给自己投票
        self.node.currentTerm += 1          #????不确定什么时候加1
        self.voteFor = self.node.user_ID
        self.votes = 1          #重置选票数量

        Index, Term = self.node.get_lastLogs_info()         #获取最后一个日志的索引和任期
        seg = ElectRequestMessage(self.node.user_ID, self.node.currentTerm, Index, Term)
        self.node.server.broadcast(self.node.other_peers, seg)      #广播消息

    def on_ElectResponse(self, msg):
        """
        选举响应处理
        :param msg:收到的消息
        :return:
        """
        msg = msg.serialize()
        if msg["voteGranted"] == True:     #如果投票通过
            self.votes += 1

        # 如果获得了大多数的选票，切换到Leader状态
        if self.votes > len(self.node.other_peers) / 2:
            ##广播消息
            Index, Term = self.node.get_lastLogs_info()         #获取最后一个日志的索引和任期
            seg = AppendEntriesMessage(self.node.user_ID, self.node.currentTerm, Index, Term, self.node.commitIndex)
            self.node.server.broadcast(self.node.other_peers, seg)      #广播消息
            self.switch_to_leader()
            # for node in self.node.other_peers:
            #     self.node.server.send(node["port"], node["host"], seg)
    
    def on_AppendEntries(self, msg):
        """
        日志（心跳）处理，如果请求的任期大于等于当前任期，则切换到Follower状态
        :param msg:收到的消息
        :return: bool
        """
        msg = msg.serialize()
        if self.node.currentTerm <= msg["term"]:         #如果请求的任期大于等于当前任期
            self.node.currentTerm = msg["term"]
            self.switch_to_Follower(msg["leaderId"], msg["leaderId"])
            return True
        else:
            return False

    def on_ElectRequest(self, msg):
        """
        选举请求处理
        :param msg:收到的消息
        :return: bool
        """
        msg = msg.serialize()
        # if self.node.currentTerm < msg["term"]:         #如果请求的任期大于当前任期
        #     self.node.currentTerm = msg["term"]
        #     self.switch_to_Follower(msg["candidateId"])
            #######################增加投票
        candidateId = msg['candidateId']
        term = msg['term']
        lastLogTerm = msg['lastLogTerm']
        
        # 假设你有方法 get_lastLogs_info() 来获取当前的最后日志信息
        _, lastLogsTerm = self.node.get_lastLogs_info()
        
        # 仅在未投票或收到更高任期的请求时考虑投票
        if self.node.currentTerm < term and lastLogsTerm <= lastLogTerm:
            self.switch_to_Follower(candidateId)
            self.node.currentTerm = term  # 更新当前任期
            msg_response = ElectResponseMessage(self.node.user_ID, True)
            # msg_response = msg_response.serialize()  # 也要序列化响应消息
            
            # 找到候选人信息发送响应
            for peer in self.node.other_peers:
                if peer["node_ID"] == candidateId:
                    self.node.server.send(peer["port"], peer["host"], msg_response)
                    print(f"[{self.node.user_ID}投票给{candidateId}，其任期为{term}]")
                    break
                    
            return True
        else:
            return False
        
    def on_ClientRequest(self, msg):
        """
        客户端请求处理，返回现在的LeaderID。同理Follower，保证不存在无信息返回
        :param msg:收到的消息
        :return:
        """
        msg = msg.serialize()
        if self.leaderId is not None:     #如果有Leader，则重定向
            leaderHost, leaderPort = self.node.get_address(self.leaderId)
            port, host = msg['clientAddress']['port'], msg['clientAddress']['host']
            response = ClientRedirectMessage("ClientRequestMessage", self.leaderId, leaderPort, leaderHost)
            self.node.server.send(port, host, response)
        else:
            pass

    def on_ClientAppendEntries(self, msg):
        """
        客户端日志追加处理，返回现在的LeaderID。同理Follower，保证不存在无信息返回
        :param msg:收到的消息
        :return:
        """
        msg = msg.serialize()
        if self.leaderId is not None:     #如果有Leader，则重定向
            leaderHost, leaderPort = self.node.get_address(self.leaderId)
            port, host = msg['clientAddress']['port'], msg['clientAddress']['host']
            response = ClientRedirectMessage("ClientAppendEntriesMessage", self.leaderId, leaderPort, leaderHost)
            self.node.server.send(port, host, response)
        else:
            pass

class Leader(State):
    def __init__(self, node):
        super(Leader, self).__init__(node)
        next_Index = len(self.node.Entries) + 1
        self.nextIndex = [{"node_ID": i["node_ID"], "Index": next_Index} for i in self.node.other_peers]
        self.matchIndex = [{"node_ID": i["node_ID"], "Index": 0} for i in self.node.other_peers]

        self.node.timer.restart_timer(1000, 1000)

    def timeout(self):
        self.node.timer.restart_timer(1000, 1000)
        self.AppendEntries()        #发送心跳检测
        
    def find_nextIndex(self, node_ID, Index = None):
        """
        查找、修改日志的索引。如果有Index参数时，修改；
        无Index参数时，查找
        """
        for i in self.nextIndex:
            if i["node_ID"] == node_ID:
                if Index is not None:
                    i["Index"] = Index
                return i["Index"]
        print("[Error: Can't find the nextIndex]")
        return False
    
    def find_matchIndex(self, node_ID, Index = None):
        """
        查找、修改匹配的日志索引
        """
        for i in self.matchIndex:
            if i["node_ID"] == node_ID:
                if Index is not None:
                    i["Index"] = Index
                return i["Index"]
        print("[Error: Can't find the matchIndex]")
        return False

    def switch_to_Follower(self, candidateId = None):
        """
        切换到Follower状态,重置计时器
        """
        # self.node.timer.restart_timer(2000, 3000)
        self.node.state = Follower(self.node, candidateId)
        print("[Switch to Follower!!!]")

    def judge_commitIndex(self):
        """
        判断是否有1/2节点同步，有则进行应用提交
        """
        for i in range(self.node.commitIndex, len(self.node.Entries) + 1):      #从commitIndex开始遍历，表示第i个日志
            count = 1
            for j in self.matchIndex:
                if j["Index"] >= i:
                    count += 1
            if count > len(self.node.other_peers) / 2:
                self.node.commitIndex = i
                self.node.apply_commits()           #应用提交
            else:
                break

    def AppendEntries(self, data = None):
        """
        日志追加,心跳检测
        :param data: 数据，默认为None
        """
        if data is None:            #如果数据为空，用作心跳检测
            Index, Term = self.node.get_lastLogs_info()         #获取最后一个日志的索引和任期
            seg = AppendEntriesMessage(self.node.user_ID, self.node.currentTerm, Index, Term, self.node.commitIndex)
            self.node.server.broadcast(self.node.other_peers, seg)      #广播消息
            print("[领导者" + str(self.node.user_ID) + "。发送心跳检测!!!]")
        else :
            # data = data.encode()
            Entry = {
                "Index": len(self.node.Entries) + 1,
                "Term": self.node.currentTerm,
                "Data": data
            }
            Index, Term = self.node.get_lastLogs_info()        #获取最新日志的索引和任期，没有则返回(0,0)
            self.node.Entries.append(Entry)
            seg = AppendEntriesMessage(self.node.user_ID, self.node.currentTerm, Index, Term, self.node.commitIndex, data)
            self.node.server.broadcast(self.node.other_peers, seg)
            return True

    def on_AppendEntriesResponse(self, msg):       
        """
        日志追加响应处理，如果追加失败，则
        :param msg:收到的消息
        """
        msg = msg.serialize()
        if msg["success"] == False:     #如果追加失败，返回Index - 1的日志
            Index = self.find_nextIndex(msg["node_ID"], msg["lastLogIndex"] + 1) - 1      #更新nextIndex
            Term = self.node.get_log_term(Index)
            data = self.node.get_log_data(Index)
            seg = AppendEntriesMessage(self.node.user_ID, self.node.currentTerm, Index - 1, Term, self.node.commitIndex, data)
            host, port = self.node.get_address(msg["node_ID"])
            self.node.server.send(port, host, seg)
        else:                           #如果追加成功,更新nextIndex和matchIndex
            self.find_matchIndex(msg["node_ID"], msg["lastLogIndex"])           #更新matchIndex
            self.find_nextIndex(msg["node_ID"], msg["lastLogIndex"] + 1)        #更新nextIndex
            if msg["lastLogIndex"] < len(self.node.Entries):
                host, port = self.node.get_address(msg["node_ID"])
                Index = self.find_nextIndex(msg["node_ID"]) - 1                 #查询nextIndex
                Term = self.node.get_log_term(Index)
                data = self.node.get_log_data(Index)
                seg = AppendEntriesMessage(self.node.user_ID, self.node.currentTerm, Index, Term, self.node.commitIndex, data)
                self.node.server.send(port, host, seg)
            else:    #如果追加最新消息成功，则判断是否有1/2节点同步，有则进行日志追加，并更新nextIndex和matchIndex
                self.judge_commitIndex()

    def on_ElectRequest(self, msg):
        """
        选举响应处理，如果请求的任期大于当前任期，则切换到Follower状态；并且日志比它要新的话，给他投票
        :param msg:收到的消息
        """
        msg = msg.serialize()
        if self.node.currentTerm < msg["term"]:         #如果请求的任期大于当前任期
            self.node.currentTerm = msg["term"]
            

            last_log_term, last_log_index = self.node.get_lastLogs_info()
            if (msg["lastLogTerm"] > last_log_term) or (msg["lastLogTerm"] == last_log_term and msg["lastLogIndex"] >= last_log_index):         #如果请求的日志比本地的新，则切换到Follower状态，并给他投票


                term = msg['term']
                candidateId = msg['candidateId']
                self.switch_to_Follower(candidateId)

                msg_response = ElectResponseMessage(self.node.user_ID, True)

                # 找到候选人信息发送响应
                for peer in self.node.other_peers:
                    if peer["node_ID"] == candidateId:
                        self.node.server.send(peer["port"], peer["host"], msg_response)
                        print(f"[{self.node.user_ID}投票给{candidateId}，其任期为{term}]")
                        break
                return True
            
            self.switch_to_Follower()
            return False
        else:
            return False

    def on_ClientRequest(self, msg):
        """
        客户端请求处理，返回消息
        :param msg:收到的消息
        :return:
        """
        msg = msg.serialize()
        port, host = msg['clientAddress']["port"], msg['clientAddress']["host"]
        response = ClientResponseMessage("succeed", self.node.user_ID, self.node.Entries)

        self.node.server.send(port, host, response)
        
    
    def on_ClientAppendEntries(self, msg):
        """
        客户端日志追加处理，返回消息
        :param msg:收到的消息
        :return:
        """
        msg = msg.serialize()
        data = msg["entries"]
        isAddend = self.AppendEntries(data)
        if isAddend:
            port, host = msg['clientAddress']["port"], msg['clientAddress']["host"]
            data = self.node.Entries[-1]
            response = ClientAppendEntriesResponseMessage("succeed", data)

            self.node.server.send(port, host, response)
        else:
            pass