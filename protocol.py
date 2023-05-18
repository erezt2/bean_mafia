import pickle, socket
from information import *


BYTES_LENGTH = 3
TEMP = 1024
test = True


def receive(skt):
    if test:
        temp = skt.recv(TEMP)
        if not temp:
            return None
        return pickle.loads(temp)
    temp = skt.recv(BYTES_LENGTH)
    if not temp:
        return None
    length = int.from_bytes(temp, "big", signed=False)
    temp = skt.recv(length)
    return pickle.loads(temp)


def send(skt, data):
    if test:
        temp = pickle.dumps(data)
        if len(temp) >= 1000:
            print(len(temp))
        skt.sendall(temp)
        return
    temp = pickle.dumps(data)
    temp1 = len(temp).to_bytes(BYTES_LENGTH, "big", signed=False)
    # print(len(temp1+temp))
    skt.sendall(temp1 + temp)
    # if isinstance(data, dict):
    #     for key in data:
    #         data[key].used()
    # elif isinstance(data, SmartDict):
    #     data.used()
    # else:
    #     raise Exception("error, got:" + str(data.__class__))
