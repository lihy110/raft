class State(object):
    """
    节点状态类
    不同状态有不同的表现
    """

    def __init__(self, node):
        self.node = node

class Follower(State):
    def __init__(self, node):
        super(Follower, self).__init__(node)
        self.voteFor = None

    def on_timeout(self):
        pass

    def on_switch_to_candidate(self):
        self.node.state = Candidate(self.node)

class Candidate(State):
    def __init__(self, node):
        super(Candidate, self).__init__(node)
        self.voteFor = None

    def on_timeout(self):
        print('timeout')
    
    def on_switch_to_leader(self):
        self.node.state = Leader(self.node)

    def switch_to_follower(self):
        self.node.state = Follower(self.node)
        self.voteFor = 1

class Leader(State):
    def __init__(self, node):
        super(Leader, self).__init__(node)

    def on_timeout(self):
        pass

    def on_switch_to_candidate(self):
        self.node.state = Candidate(self.node)
        

class Node():
    def __init__(self):
        self.config = 1
        self.state = Follower(self)
        self.term = 0
        self.log = []
        self.commitIndex = 0

    def start(self):
        pass

    def dispatch(self, server, client, request):
        pass

    def on_term(self):
        self.term += 1

def main():
    n = Node()
    n.state.on_switch_to_candidate()
    print(n.state)
    n.state.switch_to_follower()
    print(n.state.voteFor)

if __name__ == '__main__':
    main()