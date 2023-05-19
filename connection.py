import socket, threading, protocol
from visuals.text import Text
from visuals.click import Click
from classes.selfPlayer import SelfPlayer
from classes.projectile import Projectile


def none(a=None):
    pass


def menu_delete_status(self=None):
    Text.get_key("status").text = ""


class Connection:

    def __init__(self, screen, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.address = (self.ip, self.port)

        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        skt.connect((ip, port))
        self.client = skt
        self.stored = []
        self.cache = []
        self.running = True
        self.lock = threading.Lock()

        v = screen.variables
        self.screen = screen
        v.conn = self

        hs = protocol.receive(skt)
        if hs is None:
            Click.get_key("start").enabled = True
            Text.get_key("status").text = "connection failed"
            self.screen.Process(none, menu_delete_status, frames=100, dict_key="delete_status")
            screen.variables.conn = None
        else:
            self.id, self.name = hs
            self.thread = threading.Thread(target=self.run, args=tuple())
            screen.change_screen("game")
            self.screen.Text((self.name, "Arial", 1 / 35, (255, 255, 255)), (0.5, 0.5 - 1j / 20), (0.5, 0.65), "self_player",
                                f"player_{self.id}", stick_to_camera=True, z_index=2)
            v.player = SelfPlayer(screen)
            v.conn.send(["update_player_pos", v.player.get_player_desc()])
            self.thread.start()

    def send(self, data):
        protocol.send(self.client, data)

    def run(self):
        while self.running:
            data = protocol.receive(self.client)
            with self.lock:
                self.stored.append(data)

    def get_stored(self):
        with self.lock:
            stored = list(self.stored)
            self.stored.clear()
        return stored

    def quit(self):
        print(1234)
        v = self.screen.variables
        Projectile.projectile_list.clear()
        self.running = False
        self.client.close()
        v.ip_inserted = ""
        v.conn = None
        if v.server is not None:
            v.server.close()
            v.stop_event.set()
            v.server = None
            v.stop_event = None
        self.screen.change_screen("menu")
