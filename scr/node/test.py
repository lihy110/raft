from Node import * 
from utility import *
node = [
        {'name': 'node1', 'user_ID': 1, 'currentTerm': 0, 'commitIndex': 0, 'lastApplied': 0, 'Entries': []},
        {'name': 'node2', 'user_ID': 2, 'currentTerm': 0, 'commitIndex': 0, 'lastApplied': 0, 'Entries': []},
    ]


def main(file_path):
    config = peer.load_config(file_path)       
    node = Node(config)
    a = node[-1]["name"]
    print(a)


if __name__ == "__main__":
    file_path = "../peer1_config.json"
    main(file_path)