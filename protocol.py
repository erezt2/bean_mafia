import pickle


BYTES_LENGTH = 3
TEMP = 1024
test = True


def receive(skt):
    try:
        temp = skt.recv(TEMP)
    except ConnectionAbortedError:
        return None
    except ConnectionResetError:
        return None
    if not temp:
        return None
    return pickle.loads(temp)
    # temp = skt.recv(BYTES_LENGTH)
    # if not temp:
    #     return None
    # length = int.from_bytes(temp, "big", signed=False)
    # temp = skt.recv(length)
    # return pickle.loads(temp)


def send(skt, data):
    temp = pickle.dumps(data)
    if len(temp) >= 1000:
        print(len(temp))
    skt.sendall(temp)
    return
    # temp = pickle.dumps(data)
    # temp1 = len(temp).to_bytes(BYTES_LENGTH, "big", signed=False)
    # skt.sendall(temp1 + temp)
