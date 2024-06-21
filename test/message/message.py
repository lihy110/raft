class ElectResponseMessage():
    """
    响应选取结果的消息
    消息格式：
        @follower_host:follower_port@elect 1/0
    """

    def __init__(self, follower, value):
        """
        :param follower 参与选举的follower的node key
        :param value    选举结果0已经选举其他node 1选取
        """
        self.follower = follower
        self.value = value

    def serialize(self, eol=False):
        """
        重载
        """
        data = {
            'follower': self.follower,
            'value': self.value
        }
        return data
    
if __name__ == '__main__':
    """
    测试
    """
    follower = ('localhost', 8080)
    value = 1
    msg = ElectResponseMessage(follower, value)

    print(isinstance(msg, ElectResponseMessage))