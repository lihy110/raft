# raft
&emsp;&emsp;Raft是一种共识算法，旨在解决分布式系统中节点之间达成一致的问题。它通过领导者选举、日志复制和安全性保障等机制来确保系统的一致性和可用性。

&emsp;&emsp;Raft算法的核心是一种强一致性的日志复制机制，其中包括三种角色：领导者、跟随者和候选者。在Raft中，领导者负责接收客户端请求，并将其复制到其他节点的日志中。跟随者则遵循领导者的指令来维护一致性，并在必要时成为候选者参与选举。选举过程确保了系统中的唯一领导者，从而有效地管理日志的复制和一致性。
## 项目结构

- raft
  - img   //存放展示图片
    - 实例  //运行结果
    - 流程图  
  - log   //日志记录
    - log.md    //开发日志
  - scr     //主程序
    -node
      - Node.py     //节点
      - State.py    //状态
      - utility.py  //工具类
      - test.py     //测试
    - server
      - Message.py    //消息封装
      - Server.py   //通讯封装
      - Channel.py  //已弃用，用于连接消息和节点
    - peer1.py    //节点
    - peer2.py    //节点
    - peer1_config.json     //配置信息
    - peer2_config.json     //配置信息
  - test    //测试
    - C_S      //两节点进行交互测试
      - socket_client.py  //客户端
      - socket_server.py  //服务端
    - data_switch_UDP    //data的json数据在两节点进行交互
      - peer1.py
      - peer2.py
      - test_json.py
    - reading_config       //配置读取测试
      - read_config.py
      - peer_config.json
    - parameter_test    //argument参数传递测试
      - test.py   
    - message   //消息识别
      - message.py  
    - select_test     //TCP测试
      - c.py
      - c2.py
      - s.py    //服务器端
    -Timeout    //超时计时器测试
      - timer.py
    - switch_type.py       //状态转换测试
  - PlantUML      //PlantUML流程图代码

## 功能
&emsp;&emsp;实现了选举、日志追加、对齐和心跳、以及客户端对于消息的查询和添加。
*成员管理功能还未完成*

## 运行
**节点**：在raft/scr中运行python peer?.py(?为节点号，目前只有三个，可自行增加)。<br>
配置类型为 json，默认为当前目录的./peer?_config.json文件
```cmd
python ./peer1.py -p="配置文件路径"       
```
配置信息说明
```json
{
    "name": "peer01",                 #节点名称
    "node_ID": 1,                     #节点ID
    "host": "localhost",              #节点host
    "port": 3000,                     #节点端口号
    "other_peers":[                   #其他节点信息
        {
            "node_ID":2,
            "host": "localhost",
            "port": 3001
        },
        {
            "node_ID":3,
            "host": "localhost",
            "port": 3002
        }
    ]
    
}
```

**客户端**：在raft/scr中运行python client.py。其中有功能1.查询；2.添加日志；3.退出；
## 开发工具

- python 3.11.8
- socket 
- threading