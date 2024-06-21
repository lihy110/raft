# 开发日志
## 之前
> 实现了节点之间的p2p交互、节点状态转换、节点配置加载

## 4.30
- 将底层通讯协议改为TCP，并进行select.select模块测试（弃用）

## 5.6
- TCP已弃用
- 完成Message.py信息包的封装
- 完成Server.py消息传递的封装

**待完成:**
- 需要进一步完成消息回复以及消息接受处理
- 还需要完成State.py的110行通讯处理，将通讯和消息处理结合

## 5.7
- 取消Server.py消息接受的循环，将其视为底层，将线程部署放在Node.py
- 完成计时器

**待完成:**
- 需要继续在Node.py中将计时器融入其中


## 5.8
- 完成Node.py中的计时器

**待完成:**
- 完成State.py的超时处理

## 5.9
- 完成State.py中Candidate的on_ElectResponse（选举响应处理）
- 完成State.py中Follower的on_ElectRequest（投票请求处理）

**待完成:**
- 选举功能

## 5.10
- 修改了名称，处理消息响应前为on_，其余取消on_前缀
- 完成了State.py中Candidate的Elect（选举）功能
- Node.py新增get_lastLogs_info()（获取最后第n个日志的索引和任期）功能
- 完成State.py中AppendEntries()（日志追加）

**待完成:**
- State.py中Leader的on_AppendEntries（AppendEntries响应的处理），日志对其、日志追加

## 5.12
- 在Node.py中新增get_address(self, leaderId)用于获取对应ID的地址
- 完成State.py中的Candidate类里on_AppendEntries()（日志追加处理）
- 在State.py的Candidate类里增加on_ElectRequest()（选举响应处理）
- 修改State.py的Candidate类里的switch_to_Follower()方法，增加转变类时包含voteFor

**待完成**
- 完成State.py中的AppendEntriesResponseMessage（日志追加响应消息）的响应处理    (完成)
- 完成State.py中Leader类里的on_AppendEntriesResponse()（日志追加响应处理）  （完成）

## 5.15
- 在Message.py中的AppendEntriesResponseMessage类里增加node_ID属性（node_ID属性用于Leader辨识Follower身份）
- 修改State.py中Follower类的on_AppendEntries()方法，使其一次添加一条（**可以优化**），修改如下

    ``` python
            # 追加新的日志条目
            for entry in msg["entries"]:
                self.node.Entries.append(entry)
            #修改为
            # 追加新的日志条目
            self.node.Entries.append(entry)
    ```
- 在Node.py的Node类中添加def get_log_data(self, index)方法用于获取数据

**待完成**
- 完善State.py中Leader类里的on_AppendEntriesResponse()（日志追加响应处理）添加nextIndex[]和matchIndex[]的处理 （完成）

## 5.16 
- 在Message.py中的AppendEntriesResponseMessage()类中添加lastLogIndex成员变量
- 在State.py中的Follower类中的on_AppendEntries()（日志追加处理）方法中增加直接返回prevLogIndex的判断，如下
    ```python
            if prevLogIndex > 0 and prevLogIndex > len(self.node.Entries):          #如果prevLogIndex大于日志长度，则直接返回lastLogIndex
                response = AppendEntriesResponseMessage(self.node.termcurrentTerm, False, self.node.user_ID, len(self.node.Entries))
                self.node.server.send(port, host, response)
                return False
    ```
- 在State.py中的Follower类中的on_AppendEntries()（日志追加处理）方法中增加对于AppendEntriesResponseMessage()消息的lastLogIndex变量处理，将删除不匹配日志放入判断，以便于Leader更新nextIndex
    ```python
            elif prevLogIndex > 0 and self.node.get_log_term(prevLogIndex) != prevLogTerm:
                # 如果不匹配，发送不成功的响应，删除prevLogIndex及其之后的日志
                self.node.Entries = self.node.Entries[:prevLogIndex - 1]    #增加
                response = AppendEntriesResponseMessage(self.node.termcurrentTerm, False, self.node.user_ID, len(self.node.Entries))
                
                self.node.server.send(port, host, response)
                return False
    ```

- 在State.py中的Follower类中增加judge_commitIndex()方法用于查询日志同步是否大于1/2节点，有则同步
- 在State.py中的Leader类中的on_AppendEntriesResponse()（日志追加响应处理）中增加lastLogIndex变量处理，以修改及nextIndex和matchIndex变量的变更（判断msg["lastLogIndex"]是否小于len(self.node.Entries)有则说明还在日志同步中，反之则最新追加完成并检测是否进行提交）
- 增加状态转换时，输出XXX switch to XXX

**待完成**
- 完成心跳消息触发日志同步  （完成）
- 检测其他的nextIndex和matchIndex的值修改       （完成）
- 再次检查on_AppendEntriesResponse()的逻辑      （完成）
- 完成代码调试

## 5.20
- 在State.py中的Leader类中的on_AppendEntriesResponse()（日志追加响应处理）增加心跳消息的日志对齐触发
- 在State.py中的Leader类中的on_AppendEntriesResponse()（日志追加响应处理）增加对于日志消息，当Leader的prevLogIndex < len(Entries)的处理方法，即删除Entries中prevLogIndex后内容
- 解决了5.18的错误调试

**待完成**
- 在Leader中增加当收到消息的term和最新日志大于自己时，变为Follower。
    > 问题：如果存在一个较新节点反复发送心跳信息，那Leader会频繁变为Follower。

## 5.28
- 在scr文件夹中增加client.py客户端，并完成初始化、信息发送部分
- 在peer.py文件中增加argparse来指定读取文件参数路径

**待完成**
- 在client.py文件夹中完成消息处理handle()函数

## 6.17
- 在Message.py文件中，增加客户端消息类型,并完成了部分客户端的消息处理

**待完成**
- 在client.py文件夹中完成消息处理handle()函数以及State.py中各角色的客户端消息处理

## 6.18
- 在State.py中的Follower和Candidate角色中增加leaderId成员变量
- 在Message.py文件中的ClientRequestMessage类中增加clientAddress成员变量，并增加相应的处理
- 在State.py中的Leader类的timeout()方法中增加超时触发心跳

**待完成**
- 完成Follower()、Candidate()和Leader类中的on_ClientRequest()和on_ClientAppendEntries()方法    （完成）

## 6.19 
- 修改State.py中的Candidate类的on_ElectRequest()方法，增加变为Follower后立即投票，防止多次变为Candidate
    ```python
    ###修改前:
    msg = msg.serialize()
    if self.node.currentTerm < msg["term"]:         #如果请求的任期大于当前任期
        self.node.currentTerm = msg["term"]
        self.switch_to_Follower(msg["candidateId"])
    ```

- 对State.py中的Followers类的on_AppendEntries()（日志追加处理）方法进行了重构，将旧的Term消息全部抛弃，并且对有效消息实现计时器重置；且对于领导者和任期更新也提前了

## 6.20
- 在State.py中的Leader类中增加on_ElectRequest()方法，以处理收到Candidate的投票，防止其一直是Leader
- 在State.py中的Candidate类中on_AppendEntries()方法增加了`node.currentTerm <= msg["term"]`，将之前的<改为<=，**防止在选出有效领导者时，重新进行选举**。
```python
if self.node.currentTerm <= msg["term"]:         #如果请求的任期大于当前任期
    self.node.currentTerm = msg["term"]
    self.switch_to_Follower(msg["leaderId"], msg["leaderId"])
```
- 将角色状态转变时计时器的重置放到角色初始化处
- 增加一些成功运行输出

# 错误调试
## 5.18
- 运行scr中的peer1.py文件报错`Receive error: [WinError 10035] 无法立即完成一个非阻止性套接字操作。`
    > **原因**：非阻塞的recvform系统调用调用之后，进程并没有被阻塞，内核马上返回给进程，如果数据还没准备好，此时会返回一个error。进程在返回之后，可以干点别的事情，然后再发起recvform系统调用。重复上面的过程，循环往复的进行recvform系统调用。这个过程通常被称之为轮询。轮询检查内核数据，直到数据准备好，再拷贝数据到进程，进行数据处理。需要注意，拷贝数据整个过程，进程仍然是属于阻塞的状态。<br>
    > **解决方法**：抛出异常pass

## 6.18
- 运行多个节点时，一直处于选举阶段，未能选出领导者
- 运行时发现出现错误`AttributeError: 'ElectRequestMessage' object has no attribute 'encode'`
    > **原因**：因为 data 是一个 ElectRequestMessage 对象，而不是一个字符串。<br>
    > **解决方法**：使用python中的pickle模块进行序列号对象，修改如下
    ```python
    ###发送方
    data_bytes = pickle.dumps(data)
    self.accepter.sendto(data_bytes, (addr, port))

    ###接收方
    data= self.accepter.recv(1024)
    data = pickle.loads(data)
    ```

- 修改Follower类中的on_ElectRequest()方法之前：
    ```python
    def on_ElectRequest(self, msg):
        msg = msg.serialize()
        candidateId = None
        for peer in self.node.other_peers:
            if peer["node_ID"] == msg["candidateId"]:
                candidateId = peer["node_ID"]
                host = peer["host"]
                port = peer["port"]
        if candidateId is not None:                                  #如果请求投票的节点在节点列表中
            _, lastLogsTerm = self.node.get_lastLogs_info()          #获取最后一个日志的索引和任期
            if self.voteFor != None:                                 #如果已经投过票
                return False
            
            elif self.node.currentTerm < msg["term"]:                 #如果请求的任期大于当前任期
                self.node.currentTerm = msg["term"]                   #更新当前任期，直接等于请求的任期，不然追不上
                if lastLogsTerm <= msg["lastLogIndex"]:               #如果请求的日志索引大于等于本地日志索引
                    self.voteFor = msg["candidateId"]
                    msg_response = ElectResponseMessage(self.node.user_ID, True)
                    self.node.server.send(port, host, msg_response)   #发送响应
                    self.node.timer.restart_timer(2000, 3000)         #重置计时器????，防止竞争
                    return True
                return False
            else:                                                     #如果请求的任期小于当前任期
                return False
    ```

## 6.19
- 运行时发现`if peer["node_ID"] == candidateId`未能进行匹配
    > **原因**：因为 在配置文件中`"node_ID": "1",`设置为了字符串。<br>
    > **解决方法**：修改为int类型`node_ID": 1`

- 之前运行时，收到选票报错
    > **原因**：一些名称设置错误。<br>
    ```cmd
    #——————————————————————————————————1——————————————————————————————————#
    Node 1 received message: <server.Message.ElectResponseMessage object at 0x0000013328CD9FD0> 
    Exception in thread Thread-1 (start_state_handling):
    Traceback (most recent call last):
    File "D:\Program Files\anaconda3\Lib\threading.py", line 1045, in _bootstrap_inner        
        self.run()
    File "D:\Program Files\anaconda3\Lib\threading.py", line 982, in run
        self._target(*self._args, **self._kwargs)
    File "D:\87128\Programme\py_run\raft\scr\node\Node.py", line 72, in start_state_handling  
        self.state.handle(msg)      # 处理消息
        ^^^^^^^^^^^^^^^^^^^^^^
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 26, in handle
        self.on_ElectResponse(msg)
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 293, in on_ElectResponse    
        seg = AppendEntriesMessage(self.node.user_ID, self.node.term, Index, Term, self.node.commitIndex)
                                                
        ^^^^^^^^^^^^^^
    AttributeError: 'Node' object has no attribute 'term'

    #——————————————————————————————————2——————————————————————————————————#
    #——————节点1-Leader——————#
    Node 1 received message: <server.Message.ElectResponseMessage object at 0x000001A91C648E50>
    Candidate成为Leader!!!
    Node 1 received message: <server.Message.ElectResponseMessage object at 0x000001A91C37C490> 
    Time out
    Exception in thread Thread-2 (timeout):       
    Traceback (most recent call last):
    File "D:\Program Files\anaconda3\Lib\threading.py", line 1045, in _bootstrap_inner        
        self.run()
    File "D:\Program Files\anaconda3\Lib\threading.py", line 982, in run
        self._target(*self._args, **self._kwargs) 
    File "D:\87128\Programme\py_run\raft\scr\node\Node.py", line 82, in timeout
        self.state.timeout()
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 388, in timeout
        self.AppendEntries()        #发送心跳检测 
        ^^^^^^^^^^^^^^^^^^^^
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 445, in AppendEntries       
        seg = AppendEntriesMessage(self.node.user_ID, self.node.term, Index, Term, self.node.commitIndex)
                                                
        ^^^^^^^^^^^^^^
    AttributeError: 'Node' object has no attribute 'term'

    #——————节点2-Follower——————#
    Node 2 received message: <server.Message.ElectRequestMessage object at 0x00000203E74AA010>
    Candidate switch to Follower!!!
    Voted for 1 by 2
    Node 2 received message: <server.Message.AppendEntriesMessage object at 0x00000203E6FEAE50>         #收到心跳
    Exception in thread Thread-1 (start_state_handling):
    Traceback (most recent call last):
    File "D:\Program Files\anaconda3\Lib\threading.py", line 1045, in _bootstrap_inner        
        self.run()
    File "D:\Program Files\anaconda3\Lib\threading.py", line 982, in run
        self._target(*self._args, **self._kwargs)
    File "D:\87128\Programme\py_run\raft\scr\node\Node.py", line 72, in start_state_handling  
        self.state.handle(msg)      # 处理消息
        ^^^^^^^^^^^^^^^^^^^^^^
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 28, in handle
        self.on_AppendEntries(msg)
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 134, in on_AppendEntries    
        msg = msg.serialize()
            ^^^^^^^^^^^^^^^
    File "D:\87128\Programme\py_run\raft\scr\server\Message.py", line 74, in serialize        
        'leader': self.leader,
                ^^^^^^^^^^^
    AttributeError: 'AppendEntriesMessage' object has no attribute 'leader'. Did you mean: 'leaderId'?

    #——————————————————————————————————3——————————————————————————————————#
    #——————节点2-Follower——————#
    Node 2 received message: <server.Message.ElectRequestMessage object at 0x0000018B9ADD9FD0>
    Candidate switch to Follower!!!
    Voted for 1 by 2
    Node 2 received message: <server.Message.AppendEntriesMessage object at 0x0000018B9ADD9FD0> 
    Exception in thread Thread-1 (start_state_handling):
    Traceback (most recent call last):
    File "D:\Program Files\anaconda3\Lib\threading.py", line 1045, in _bootstrap_inner        
        self.run()
    File "D:\Program Files\anaconda3\Lib\threading.py", line 982, in run
        self._target(*self._args, **self._kwargs)
    File "D:\87128\Programme\py_run\raft\scr\node\Node.py", line 72, in start_state_handling  
        self.state.handle(msg)      # 处理消息
        ^^^^^^^^^^^^^^^^^^^^^^
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 28, in handle
        self.on_AppendEntries(msg)
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 135, in on_AppendEntries    
        if msg["data"] == None:                         #心跳检测
        ~~~^^^^^^^^
    KeyError: 'data'
    ```
- 发现同时两个Follower同时成为Candidate后，另一个节点都给两个节点进行投票了
    > **原因**：在Follower和Candidate类的on_ElectRequest()方法中，Term对象获取错误😓<br>
    ```python
    ###修改前
    def on_ElectRequest(self, msg):
        #……
        lastLogIndex = msg['lastLogIndex']
        _, lastLogsTerm = self.node.get_lastLogs_info()
        
        # 仅在未投票或收到更高任期的请求时考虑投票
        if (self.voteFor is None or self.node.currentTerm < term) and lastLogsTerm <= lastLogIndex:
        #……

    ###修改后
    def on_ElectRequest(self, msg):
        #……
        lastLogTerm = msg['lastLogTerm']

        # 假设你有方法 get_lastLogs_info() 来获取当前的最后日志信息
        _, lastLogsTerm = self.node.get_lastLogs_info()

        # 仅在未投票或收到更高任期的请求时考虑投票
        if (self.voteFor is None or self.node.currentTerm < term) and lastLogsTerm <= lastLogTerm:
            #……
    ```
- 运行client.py，再添加节点时报错
    ```cmd
    Node 2 received message: <server.Message.ClientAppendEntriesMessage object at 0x000002DBFEB8A110>  
    Exception in thread Thread-1 (start_state_handling):
    Traceback (most recent call last):
    File "D:\Program Files\anaconda3\Lib\threading.py", line 1045, in _bootstrap_inner
        self.run()
    File "D:\Program Files\anaconda3\Lib\threading.py", line 982, in run
        self._target(*self._args, **self._kwargs)
    File "D:\87128\Programme\py_run\raft\scr\node\Node.py", line 72, in start_state_handling
        self.state.handle(msg)      # 处理消息
        ^^^^^^^^^^^^^^^^^^^^^^
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 34, in handle
        self.on_ClientAppendEntries(msg)
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 217, in on_ClientAppendEntries     
        if self.node.leader is not None:     #如果有Leader，则重定向  
        ^^^^^^^^^^^^^^^^
    AttributeError: 'Node' object has no attribute 'leader'
    ```

## 6.20
- 在客户端向Leader发送ClientAppendEntriesMessage来添加信息时，报错
    ```cmd
    Node 2 received message: <server.Message.ClientAppendEntriesMessage object at 0x000001C6C2BEE350>  
    Exception in thread Thread-1 (start_state_handling):
    Traceback (most recent call last):
    File "D:\Program Files\anaconda3\Lib\threading.py", line 1045, in _bootstrap_inner
        self.run()
    File "D:\Program Files\anaconda3\Lib\threading.py", line 982, in run
        self._target(*self._args, **self._kwargs)
    File "D:\87128\Programme\py_run\raft\scr\node\Node.py", line 74, in start_state_handling
        self.state.handle(msg)      # 处理消息
        ^^^^^^^^^^^^^^^^^^^^^^       
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 34, in handle
        self.on_ClientAppendEntries(msg)
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 540, in on_ClientAppendEntries     
        data = msg["ClientResponseMessage"]
            ~~~^^^^^^^^^^^^^^^^^^^^^^^^^
    KeyError: 'ClientResponseMessage'
    ```
    > **原因**：在Leader类的on_ClientAppendEntries()方法中，msg字典对象获取错误😓`data = msg["ClientResponseMessage"]`<br>
    > **解决方法**：修改为`data = msg["entries"]`
    
    <br>
    
    ```cmd
        Node 2 received message: <server.Message.ClientAppendEntriesMessage object at 0x000001EA6D46E350>  
    Exception in thread Thread-1 (start_state_handling):
    Traceback (most recent call last):
    File "D:\Program Files\anaconda3\Lib\threading.py", line 1045, in _bootstrap_inner
        self.run()
    File "D:\Program Files\anaconda3\Lib\threading.py", line 982, in run
        self._target(*self._args, **self._kwargs)
    File "D:\87128\Programme\py_run\raft\scr\node\Node.py", line 74, in start_state_handling
        self.state.handle(msg)      # 处理消息
        ^^^^^^^^^^^^^^^^^^^^^^
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 34, in handle
        self.on_ClientAppendEntries(msg)
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 542, in on_ClientAppendEntries     
        isAddend = self.AppendEntries(data)
                ^^^^^^^^^^^^^^^^^^^^^^^^
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 457, in AppendEntries
        Index, Term = self.node.get_lastLogs_info(2)        #获取紧邻 新日志之前的日志索引和任期       
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "D:\87128\Programme\py_run\raft\scr\node\Node.py", line 105, in get_lastLogs_info
        return self.Entries[-n]["Index"], self.Entries[-n]["Term"]    
            ~~~~~~~~~~~~^^^^      
    IndexError: list index out of range
    ```

    > **原因**：`self.node.Entries.append(Entry)``Index,Term = self.node.get_lastLogs_info(2)`先进性了日志添加，再进行查找倒数第二个以达到查找添加之前的最后一个log文件的目的。以至于在没有log文件的情况下进行会发现，添加后查询倒数第二个文件不存在。</br>
    > **解决方法**：更换顺序，如下
    ```python
    Index, Term = self.node.get_lastLogs_info()        #获取最新日志的索引和任期，没有则返回(0,0)
    self.node.Entries.append(Entry)
    ```
    <br>
    
    ```cmd
    Node 2 received message: <server.Message.ClientAppendEntriesMessage object at 0x000002AC296BE390>  
    Exception in thread Thread-1 (start_state_handling):
    Traceback (most recent call last):
    File "D:\Program Files\anaconda3\Lib\threading.py", line 1045, in _bootstrap_inner
        self.run()
    File "D:\Program Files\anaconda3\Lib\threading.py", line 982, in run
        self._target(*self._args, **self._kwargs)
    File "D:\87128\Programme\py_run\raft\scr\node\Node.py", line 74, in start_state_handling
        self.state.handle(msg)      # 处理消息
        ^^^^^^^^^^^^^^^^^^^^^^
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 34, in handle
        self.on_ClientAppendEntries(msg)
    File "D:\87128\Programme\py_run\raft\scr\node\State.py", line 224, in on_ClientAppendEntries     
        leaderPort, leaderHost = self.node.get_address(self.leader)   
                                                    ^^^^^^^^^^^    
    AttributeError: 'Follower' object has no attribute 'leader'. Did you mean: 'leaderId'?
    ```
    > **原因**：出现如上一些命名调用错误</br>
    > **解决方法**：进行名称更改

# 可以改进之处
1. 客户端处使用recvfrom()函数替代recv()函数，就不需要在数据段中增加发送方的地址字段
2. 使用TCP协议，保证消息的顺序收发

# 开发进度
## 投票
空行分为三阶段：发送、相应、处理
|成员        |   功能      |         完成  |
|:----------:| :---------- | :----------:  |
|Candidate   |   Elect()   |      完成     |
|            |                  |          |
|Cancidate   |on_ElectRequest() |  完成    |
|Follower    |on_ElectRequest() |  完成    |
|Leader      |on_ElectRequest() |  完成    |
|            |                  |          |
|Candidata   |on_ElectResponse()|  完成    |

## 消息追加
空行分为三阶段：发送、相应、处理
|成员        |     功能                 |   完成   |
|:----------:|   :----------            | :-------:|
|Leader      | AppendEntries()          |  完成    |
|            |                          |          |             
|Cancidate   |on_AppendEntries()        |  完成    |
|Follower    |on_AppendEntries()        |  完成    |
|            |                          |          |
|Leader      |on_AppendEntriesResponse()|  完成    |

## 成员变更
|成员        |     功能                 |   完成   |
|:----------:|   :----------            | :-------:|

## 客户端
|成员        |     功能                 |   完成    |
|:----------:|   :----------            | :-------:|
|Follower    |on_ClientRequest()        |   完成   |   
|Follower    |on_ClientAppendEntries()  |   完成   |   
|            |                          |          |
|Candidate   |on_ClientRequest()        |   完成   |   
|Candidate   |on_ClientAppendEntries()  |   完成   |   
|            |                          |          |
|Leader      |on_ClientRequest()        |   完成   |   
|Leader      |on_ClientAppendEntries()  |   完成   |   


