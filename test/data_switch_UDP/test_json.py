import requests


data = {
    "name": "peer1",
    "port": 8887,
    "type": "leader",
    "data": "hello"
}

def main():
    print(data)
    
if __name__ == '__main__':
    main()