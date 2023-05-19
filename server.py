import socket, random, protocol
import threading


class InverseFunc:  # two sided dictionary for convenience
    def __init__(self, class1, class2):
        self.class1 = class1
        self.class2 = class2
        self.one_to_two = {}
        self.two_to_one = {}

    def __contains__(self, item):
        if isinstance(item, self.class1):
            return item in self.one_to_two
        elif isinstance(item, self.class2):
            return item in self.two_to_one
        else:
            raise TypeError

    def __getitem__(self, item):
        if isinstance(item, self.class1):
            return self.one_to_two[item]
        elif isinstance(item, self.class2):
            return self.two_to_one[item]
        else:
            raise TypeError

    def __setitem__(self, key, value):
        if isinstance(key, self.class1):
            self.one_to_two[key] = value
            self.two_to_one[value] = key
        elif isinstance(key, self.class2):
            self.two_to_one[key] = value
            self.one_to_two[value] = key
        else:
            raise TypeError

    def __delitem__(self, key):
        if isinstance(key, self.class1):
            del self.two_to_one[self.one_to_two[key]]
            del self.one_to_two[key]
        elif isinstance(key, self.class2):
            del self.one_to_two[self.two_to_one[key]]
            del self.two_to_one[key]
        else:
            raise TypeError

    def __len__(self):
        return len(self.one_to_two)

    def get_two(self):
        return list(self.two_to_one.keys())

    def get_one(self):
        return list(self.one_to_two.keys())


class Server:
    SERVER_IP = "0.0.0.0"

    def __init__(self):
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        skt.bind((self.SERVER_IP, 0))
        skt.listen()

        self.port = skt.getsockname()[1]
        host = socket.gethostname()
        self.ip = socket.gethostbyname(host)
        self.server = skt
        self.users = InverseFunc(socket.socket, User)
        self.next_id = 1
        self.lock = threading.Lock()
        self.run = True

        with open("settings", "r") as file:
            self.byte_size = int(file.readlines()[3])

    # def run(self):
    #     skt_read, skt_write, _ = select.select([self.server] + self.users.get_one(), self.users.get_one(), [])
    #     for current in skt_read:  # iterate over
    #         if current is self.server:
    #             temp = self.server.accept()
    #             client = temp[0]
    #             self.users[client] = User(self, temp)
    #             self.next_id += 1
    #             temp = self.users[client]
    #             protocol.send(client, (temp.id, temp.name))
    #             print(f"{str(temp.address)} user {temp.name} connected")
    #         else:
    #             data = protocol.receive(current)
    #             user = self.users[current]
    #             if data is None:
    #                 print(f"{str(user.address)} known as {user.name} disconnected")
    #                 self.close(current)
    #                 continue
    #             self.update_client(user, data)
    #     for current in skt_write:
    #         self.send_to(current)

    def run_threads(self):
        while self.run:
            try:
                temp = self.server.accept()
            except OSError:
                break
            with self.lock:
                client = temp[0]
                self.users[client] = User(self, temp)
                self.next_id += 1
                temp = self.users[client]
            protocol.send(client, (temp.id, temp.name))
            print(f"{str(temp.address)} user {temp.name} connected")
            lst = [0, "add_players"]
            for p in self.users.get_two():
                if p == temp:
                    continue
                lst.append([p.id, p.name])
            temp.send(lst)
            temp.broadcast([temp.id, "add_player", temp.name])
            temp.start()


    def close(self):
        self.run = False
        self.server.close()
        for c in self.users.get_two():
            c.connection.close()
            c.running = False
    # def run_client(self, connection):
    #     skt_read, skt_write, _ = select.select([connection], [connection], [])
    #
    #     if skt_read:
    #         pass
        # if skt_write and :
        #     current, = skt_write
        #     self.send_to(current)

    # def send_to(self, connection):
    #     a = time.time()
    #     client = self.users[connection]
    #     protocol.send(connection, client.players_data)
    #     for key in client.players_data:
    #         if key != 0 and client.players_data[key]["+projectiles"]:
    #             print(client.players_data[key]["+projectiles"])
    #         client.players_data[key].used()
    #     if time.time() - a > 2:
    #         print(time.time() - a)
        # client.send
        # for proj in reply[1]:
        #     for player in Connection.conn_list:
        #         if player is self:
        #             continue
        #         player.projectiles.append((self.name, *proj))
        #
        # self.connection.sendall(pickle.dumps((
        #     tuple((x.name, *x.reply) for x in Connection.conn_list if x is not self),
        #     self.copy_proj()
        # )))

    # def update_client(self, user, data):
    #     if data["|test"]:
    #         print("AAAAAAAAAAAAAAA")
    #         sd = SmartDict()
    #         sd += {"=test": True}
    #         user.players_data[0] = sd
    #     data["=user_data"].name = user.name
    #     for usr in self.users.get_two():
    #         if usr == user:
    #             continue
    #         usr.set_data(usr.id, copy.deepcopy(data))
    #
    # def close(self, client):
    #     for usr in self.users.get_two():
    #         usr.set_data("=stopped", True)
    #     del self.users[client]
    #     client.close()

    # def user_from_id(self, _id):
    #     for usr in self.users.get_two():
    #         if usr.id == _id:
    #             return usr
    #     return None

    def get_ids(self):
        return map(lambda x: x.id, self.users.get_two())

    def get_names(self):
        return map(lambda x: x.name, self.users.get_two())

    def reset(self):
        pass


class User:
    name_list = ["liam", "noah", "oliver", "william", "james", "benjamin", "ethan", "alex", "henry", "jacob", "michael",
                 "daniel", "logan", "jackson", "aiden", "samuel", "matthew", "levi", "david", "john", "jeff", "carter",
                 "luke", "theodore", "jayden", "dylan", "leo", "chris", "andrew", "roy", "robert", "nicholas",
                 "emma", "sophia", "isabella", "charlotte", "mia", "evelyn", "abigail", "haley", "emily", "victoria",
                 "madison", "eleanor", "luna", "zoey", "hannah", "lily", "ellie", "violet", "satella", "leah", "bell",
                 "lucy", "ivy", "alice", "sarah", "piper", "jade", "amy", "rose", "mary", "penny", "iris", "taylor", "fuck-face"]

    def __init__(self, server, accept):
        self.connection = accept[0]
        self.address = accept[1]

        # temp_current = [this.name for this in self.__class__.conn_list if this.connected]
        self.name = random.choice([name for name in self.__class__.name_list if name not in server.get_names()])

        # temp_current = [this for this in self.__class__.conn_list if not this.connected]
        # for this in temp_current:
        #     if self.name == this.name:
        #         self.__class__.conn_list.remove(this)
        #         for i in range(len(self.__class__.conn_list)):
        #             self.__class__.conn_list[i].id = i
        #         self.__class__.users = len(self.__class__.conn_list)

        self.id = server.next_id
        self.thread = None
        self.connected = True
        self.lock = threading.Lock()
        self.recv_changed = False
        self.players_data = {}
        self.projectiles = []
        self.running = True
        self.server = server
        self.thread = threading.Thread(target=self.run, args=tuple())

    def start(self):
        self.thread.start()

    # def set_data(self, _id, data):
    #     if _id not in self.players_data:
    #         self.players_data[_id] = data
    #     else:
    #         self.players_data[_id] += data

    def run(self):
        while self.running:
            try:
                data = protocol.receive(self.connection)
            except ConnectionResetError:
                self.close()
                break
            if data is None:
                self.close()
            else:
                self.broadcast([self.id] + data)

    def close(self):
        self.broadcast([self.id, "remove_player"])
        with self.server.lock:
            del self.server.users[self]
        self.connection.close()
        self.running = False

    def broadcast(self, data):
        with self.server.lock:
            lst = self.server.users.get_two()
        for client in lst:
            if client == self:
                continue
            client.send(data)

    def send(self, data):
        with self.lock:
            protocol.send(self.connection, data)

    # def threaded_client(self):
    #     try:
    #         self.connection.send(pickle.dumps([self.id, self.name]))
    #         stop = False
    #         data = 0
    #         while True:
    #             try:
    #                 data = self.connection.recv(Server.byte_size)
    #             except ConnectionResetError:
    #                 stop = True
    #
    #             if stop:
    #                 print(f"{str(self.address)} known as {self.name} disconnected")
    #                 self.connected = False
    #                 self.reply = [None]
    #                 break
    #
    #             reply = pickle.loads(data)
    #             if reply is None:
    #                 print(f"{str(self.address)} known as {self.name} disconnected")
    #                 self.connected = False
    #                 self.reply = [None]
    #                 break
    #
    #             self.reply = reply[0]
    #
    #             for proj in reply[1]:
    #                 for player in Connection.conn_list:
    #                     if player is self:
    #                         continue
    #                     player.projectiles.append((self.name, *proj))
    #
    #             # proj_list = []
    #             # for proj in Projectile.projectile_list:
    #             #     if self.reply[0][0] - 0.75 <= proj.x <= self.reply[0][0] + 0.75 and self.reply[0][1] - 0.75 <= proj.y <= self.reply[0][1] + 0.75:
    #             #         proj_list.append(proj)
    #
    #             # (players_info, projectiles)
    #             self.connection.sendall(pickle.dumps((
    #                                         tuple((x.name, *x.reply) for x in Connection.conn_list if x is not self),
    #                                         self.copy_proj()
    #                                     )))
    #
    #     except OSError as e:
    #         print(f"{str(self.address)} known as {self.name} disconnected")
    #         self.connected = False
    #         self.reply = [None]


def loop(server, stop):
    while not stop.is_set():
        server.run()


def main():
    server = Server()
    print(server.ip, server.port, sep=":")
    server.run_threads()


if __name__ == "__main__":
    main()
