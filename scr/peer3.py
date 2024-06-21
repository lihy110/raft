from node.utility import peer
from node.Node import *
import argparse

parser = argparse.ArgumentParser(description='参数选择')
parser.add_argument('--path','-p',type=str, default = "./peer3_config.json",required=False,help="节点配置路径")

args = parser.parse_args()

def main(file_path):
    config = peer.load_config(file_path)        
    print("Successfully loaded config!!!")
    node = Node(config)


if __name__ == "__main__":
    main(args.path)