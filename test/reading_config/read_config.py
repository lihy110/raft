import json

def load_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

def main():
    # 读取对等节点配置信息
    peer_config = load_config('peer_config.json')
            ##节点状态
    user_ID = peer_config["node_ID"]
    name = peer_config["name"]
    host = peer_config["host"]
    port = peer_config["port"]    
    other_peers = peer_config["other_peers"]
    currentTerm = 0
    commitIndex = 0
    lastApplied = 0
    Entries = []
    node = 2
    node_exists = any(peer["node_ID"] == node for peer in other_peers)
    if node_exists:
        print("yes")



if __name__ == "__main__":
    main()