import random,  socket, server, protocol
import threading
import time

from state.screen import Screen
from visuals.orderedVisual import OrderedVisual
from state.game import Game
import pygame
import math
from state.functions import *
from visuals.draw import Draw
from visuals.click import Click
from visuals.process import Process
from visuals.text import Text

# from _interface import *
# from _fundementals import *
# from OpenGL.GL import *
# from OpenGL.GLU import *
from shapely.geometry import Polygon

PI = 3.14159265359


# functions
if True:
    def none(self=None):
        pass

    def debug(self=None):
        print("debug: " + str(self))

    def menu_green(self=None):
        Draw.get_key("start").w *= 0.95
        Draw.get_key("start").h *= 0.95

    def menu_white(self=None):
        Draw.get_key("start").w /= 0.95
        Draw.get_key("start").h /= 0.95

    def menu_s_white(self=None):
        self.screen.Process(menu_retract_settings, menu_retract_finish, none, 9, "sbgr")
        if Process.key_exists("sbg"):
            Process.remove_by_key("sbg")
        self.screen.variables.menu_settings_open = False

    def menu_open_settings(self=None):
        v = self.screen.variables
        r = self.screen.resources
        if v.menu_settings_open:
            self.screen.Process(menu_retract_settings, menu_retract_finish, none, 9, "sbgr")
        else:
            self.screen.Process(menu_extend_settings, none, none, 9, "sbg")
            if not Draw.key_exists("note"):
                self.screen.Draw(r.note if v.sound else r.no_note, [1 / 27, 1j / 27, 1 / 15, 1j / 15], (0.5, 0.5), "note", "", 0.5)
                self.screen.Draw(r.double_note if v.music else r.no_double_note, [1 / 27, 1j / 27, 1 / 15, 1j / 15], (0.5, 0.5), "double_note", "", 0.5)
                self.screen.Draw(r.fullscreen if self.screen.fullscreen else r.windowed, [1 / 27, 1j / 27, 1 / 15, 1j / 15], (0.5, 0.5), "windowed", "", 0.5)
                print("extend!")
        v.menu_settings_open = not v.menu_settings_open

    def menu_extend_settings(self=None):
        screen = self.screen
        if screen.cal_len_h(Click.get_key("sbg").h) >= screen.cal_len_w(1 / 15 + 9 * 1 / 45 - 0.01):
            print("extend end!")
            screen.Click((1 / 27, 1j / 27 + 8 * 1j / 120, 1 / 15, 1j / 20), (0.5, 0.5), "", "settings", on_click=toggle_sound)
            screen.Click((1 / 27, 1j / 27 + 8 * 1j / 65, 1 / 15, 1j / 20), (0.5, 0.5), "", "settings", on_click=toggle_music)
            screen.Click((1 / 27, 1j / 27 + 8 * 1j / 45, 1 / 15, 1j / 20), (0.5, 0.5), "", "settings", on_click=toggle_fullscreen)
            self.remove()
        else:
            Draw.get_key("sbg").h += 1j / 40
            Click.get_key("sbg").h += 1j / 40
            Draw.get_key("settings").y += 1j / 720
            try:
                Draw.get_key("note").y += 1j / 120
                Draw.get_key("double_note").y += 1j / 65
                Draw.get_key("windowed").y += 1j / 45
            except KeyError:
                pass

    def menu_retract_settings(self=None):
        screen = self.screen
        if self.frame == 0:
            Click.remove_by_class("settings")

        if screen.cal_len_h(Click.get_key("sbg").h) <= screen.cal_len_w(1 / 15 + 0.01):
            self.remove()
        else:
            Draw.get_key("sbg").h -= 1j / 40
            Click.get_key("sbg").h -= 1j / 40
            Draw.get_key("settings").y -= 1j / 720
            try:
                Draw.get_key("note").y -= 1j / 120
                Draw.get_key("double_note").y -= 1j / 65
                Draw.get_key("windowed").y -= 1j / 45
            except KeyError:
                pass

    def menu_retract_finish(self=None):
        print(124)
        Draw.remove_by_key("note")
        Draw.remove_by_key("double_note")
        Draw.remove_by_key("windowed")
        Draw.get_key("sbg").h = 1j / 15
        Click.get_key("sbg").h = 1j / 15
        Draw.get_key("settings").y = 1j / 270

    def menu_connect(self=None):
        v = self.screen.variables
        if Process.key_exists("delete_status"):
            Process.remove_by_key("delete_status") # ,False
        Click.get_key("start").enabled = False
        Text.get_key("status").text = "loading..."
        try:
            ip = v.ip_inserted[:v.ip_inserted.index(":")]
            port = int(v.ip_inserted[v.ip_inserted.index(":") + 1:])
        except ValueError:
            Click.get_key("start").enabled = True
            Text.get_key("status").text = "syntax error"
            self.screen.Process(none, menu_delete_status, frames=100, dict_key="delete_status")
            return

        try:
            v.conn = Connection(self.screen, ip, port)
        except socket.gaierror:
            Click.get_key("start").enabled = True
            Text.get_key("status").text = "invalid ip address"
            self.screenProcess(none, menu_delete_status, frames=100, dict_key="delete_status")

    def menu_backspace_combo(self=None):
        self.screen.variables.backspace_combo = False

    def menu_backspace_combo_allow(self=None):
        self.screen.variables.backspace_combo = True

    def menu_start_game(self=None):
        v = self.screen.variables
        _server = server.Server()
        v.server = _server
        v.stop_event = threading.Event()
        threading.Thread(target=_server.run_threads, args=tuple()).start()

        v.conn = Connection(self.screen, _server.ip, _server.port)
        pygame.scrap.put(pygame.SCRAP_TEXT, pygame.compat.as_bytes(_server.ip + ":" + str(_server.port)))
        self.screen.Text(["ip copied", "Aharoni", 1 / 25, (150, 150, 150)], (1 / 200, 1), (0, 1), "ipc", stick_to_camera=True)
        self.screen.Process(none, game_remove_ipc, frames=60)

    def menu_start_wtg(self=None):
        temp = pygame.PixelArray(Draw.get_key("start_solo").img)
        temp.replace((136, 136, 136), (40, 255, 40))
        Draw.get_key("start_solo").img = temp.make_surface()

    def menu_start_gtw(self=None):
        temp = pygame.PixelArray(Draw.get_key("start_solo").img)
        temp.replace((40, 255, 40), (136, 136, 136))
        Draw.get_key("start_solo").img = temp.make_surface()

    def menu_delete_status(self=None):
        Text.get_key("status").text = ""

    def game_remove_ipc(self=None):
        Text.remove_by_key("ipc")

    def test_change(self=None):
        r = self.screen.resources
        temp = self.frame // 5 % 4
        if temp == 0:
            Draw.get_key("test1").img = r.walkcolor1r
        elif temp == 1:
            Draw.get_key("test1").img = r.walkcolor2r
        elif temp == 2:
            Draw.get_key("test1").img = r.walkcolor3r
        elif temp == 3:
            Draw.get_key("test1").img = r.walkcolor4r

    def game_select_class(index):

        def func_wrapper(self=None):
            v = self.screen.variables
            v.player.class_id = index
            Click.remove_by_class("classes")
            Draw.remove_by_class("classes")

        return func_wrapper

# game classes

    # class ABCD:
    #     h = 10 * (2 ** (1 / 2) - 1)
    #     w = h * Screen.aspect_ratio
    #
    #     perspective = (45, Screen.aspect_ratio, 4.99, 5.01)
    #     translate = (0.0, 0.0, -5.0)
    #     rotate = (0, 0, 0, 0)
    #
    #     camera_pos = (0.0, 0.0)
    #     # vbo = glGenBuffers(1)
    #     # glBindBuffer(GL_ARRAY_BUFFER, vbo)
    #     # glBufferData(GL_ARRAY_BUFFER,)
    #
    #     @staticmethod
    #     def setup():
    #         pass
    #         # gluPerspective(*OGL.perspective)
    #         # glTranslatef(*OGL.translate)
    #         # glRotatef(*OGL.rotate)
    #         # glDisable(GL_DEPTH_TEST)
    #         # glEnable(GL_BLEND)
    #         # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #
    #     @staticmethod
    #     def blit(image, rect, shade=(1, 1, 1, 1)):
    #         Screen.win(image, (cal_len_w(rect[0]), cal_len_w(rect[1])))
    #
    #         return
    #         glEnable(GL_TEXTURE_2D)
    #         glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_rect().width, image.get_rect().height, 0, GL_RGBA,
    #                      GL_UNSIGNED_BYTE, pygame.image.tostring(image, "RGBA", 1))
    #
    #         # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    #         # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    #         glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    #         glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    #
    #         temp2 = (
    #             (0, 0),
    #             (1, 0),
    #             (1, 1),
    #             (0, 1),
    #         )
    #
    #         glBegin(GL_QUADS)
    #         glColor4fv(shade)
    #         for vertex in (0, 1, 2, 3):
    #             glTexCoord2f(*temp2[vertex])
    #             glVertex2fv((rect[vertex]))
    #         glEnd()
    #
    #         glDisable(GL_TEXTURE_2D)
    #
    #     @staticmethod
    #     def rect(color, rect, width=0):
    #         if isinstance(color[0], int):
    #             multicolor = False
    #         else:
    #             multicolor = True
    #
    #         if width:
    #             temp2 = (
    #                 (0, 1),
    #                 (0, 3),
    #                 (2, 1),
    #                 (2, 3),
    #             )
    #
    #             glBegin(GL_LINES)
    #             if not multicolor:
    #                 glColor4fv(color)
    #             for i in (0, 1, 2, 3):
    #                 if multicolor:
    #                     glColor4fv(color[i])
    #                 for j in temp2[i]:
    #                     glVertex2fv(rect[j])
    #         else:
    #             glBegin(GL_QUADS)
    #             if not multicolor:
    #                 glColor4fv(color)
    #             for i in (0, 1, 2, 3):
    #                 if multicolor:
    #                     glColor4fv(color[i])
    #                 glVertex2fv(rect[i])
    #         glEnd()
    #
    #     @staticmethod
    #     def circle(color, circle, precision=4):
    #         glBegin(GL_POLYGON)
    #         glColor4fv(color)
    #         for i in range(precision):
    #             deg = i * 2 * PI / precision
    #             glVertex2fv((circle[0] + circle[2] * math.sin(deg), circle[1] + circle[2] * math.cos(deg)))
    #         glEnd()
    #
    #     @staticmethod
    #     def move_camera(x, y):
    #         Screen.camera_pos = (Screen.camera_pos[0] + x, Screen.camera_pos[1] + y)
    #         for i in Manage.sticky_objects:
    #             i.translate(x, y)


# projectile function
if True:
    def swordsman_atk_start(self):
        if self.creator is None:
            self.draw.stick = True
            self.draw.x = 0.5
            self.draw.y = 0.5
        else:
            self.info["pos"] = (self.creator.draw.x, self.creator.draw.y)
            self.draw.x = self.creator.draw.x
            self.draw.y = self.creator.draw.y

        self.draw.d_rot = -0.4
        if abs(self.angle) > PI / 2:
            self.angular *= -1
            self.draw.alignment = (1, 1)
            self.draw.d_rot *= -1


    def swordsman_atk_exist(self):
        if self.creator is not None:
            self.draw.x += self.creator.draw.x - self.info["pos"][0]
            self.draw.y += self.creator.draw.y - self.info["pos"][1]
            self.info["pos"] = (self.creator.draw.x, self.creator.draw.y)


# important classes
if True:
    class Connection:

        def __init__(self, screen, ip, port):
            a = time.time()
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

            self.id, self.name = protocol.receive(skt)
            self.thread = threading.Thread(target=self.run, args=tuple())
            # print(time.time() - a)
            if self.id is None:
                Click.get_key("start").enabled = True
                Text.get_key("status").text = "connection failed"
                self.screen.Process(none, menu_delete_status, frames=100, dict_key="delete_status")
                screen.variables.conn = None
            else:
                change_screen(screen, "game")
                self.screen.Text((self.name, "Arial", 1 / 35, (255, 255, 255)), (0.5, 0.5 - 1j / 20), (0.5, 0.65), "self_player",
                                    f"player_{self.id}", stick_to_camera=True, z_index=2)
                v.player = SelfPlayer(screen)
                v.conn.send(["update_player_pos", v.player.get_player_desc()])
                self.thread.start()

        # def tick(self):
        #     read, _, _ = select.select([self.client], [self.client], [])
        #     if read:
        #         data = protocol.receive(read[0])
        #         if data is None:
        #             self.quit()
        #         for _id in data:
        #             if _id not in self.recv_data:
        #                 self.recv_data[_id] = data[_id]
        #             else:
        #                 self.recv_data[_id] += data[_id]
            # if write and self.send_data:
            #     if self.send_data["|test"]:
            #         print("AGAGAGAGA")
            #     protocol.send(write[0], self.send_data)
            #     self.send_data.used()

        def send(self, data):
            protocol.send(self.client, data)
            # _, write, _ = select.select([], [self.client], [])
            # if write:
            #     write, = write
            #     protocol.send(self.client, data)
            # else:
            #     self.cache.append(data)

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

        # def get(self, condition):
        #     ret = []
        #     for i in range(len(self.recv_data) - 1, -1, -1):
        #         if condition(self.recv_data[i]):
        #             ret.append(self.recv_data.pop(i))
        #     return ret

        def quit(self):
            v = self.screen.variables
            Projectile.projectile_list.clear()
            self.running = False
            self.client.close()
            v.ip_inserted = ""
            v.conn = None
            if v.server is not None:
                v.server.server.close()
                v.stop_event.set()
                v.server = None
                v.stop_event = None
            change_screen(self.screen, "menu")

# other classes
if True:
    class ShootingStar:
        s_list = []

        def __init__(self, screen):
            self.screen = screen
            self.size = random.randint(3, 6) / 300
            self.speed = random.uniform(1, 6) / 300
            self.degree = random.uniform(-PI/6, PI/6)
            self.y = random.random()
            self.x = random.random() - 1 / 6
            self.frames = random.randint(30, 180)
            self.color = (random.uniform(0.8, 1), random.uniform(0.8, 1), random.uniform(0.8, 1), random.uniform(0.8, 1))
            self.frame = 0
            self.__class__.s_list.append(self)

        def draw(self):
            self.screen.circle(self.color, (self.x, self.y, self.size), camera=False)

        def script(self):
            self.x += self.speed * math.cos(self.degree)
            self.y += self.speed * math.sin(self.degree)
            self.frame += 1
            if self.frame >= self.frames:
                self.size -= 0.2 / 300
            if self.size <= 0 or not (self.x <= 1.01 and -0.01 <= self.y <= 1.01):
                self.__class__.s_list.remove(self)


    class Player:
        players = {}

        def __init__(self, screen, _id, _name):
            self.screen = screen
            self.id = _id
            self.hp = 100
            self.name = _name
            self.draw = self.screen.Draw(screen.resources.walkcolor0l, (0, 0, 1 / 15, 1.25j / 15), (0.5, 0.5), f"player_{_id}", f"player_{_id}")
            self.draw.z = fake_atan(screen.cal_len_h(Draw.get_key("self_player").y / 50))
            self.text_name = self.screen.Text((_name, "arial", 1 / 35, (255, 255, 255)), (0, 0), (0.5, 0.65), f"player_{_id}", f"player_{_id}", z_index=-30)
            self.text_class = self.screen.Text(("", "arial", 1 / 35, (255, 255, 255)), (0, 0), (0.5, 0), f"player_class_{_id}", f"player_{_id}", z_index=-30)
            self.hp_display = self.screen.Draw((0, 255, 0), (0, 0, 1/12, 1/45), (0.5, 0.5), f"player_hp_{_id}", f"player_{_id}", z_index=-30)
            self.mode = 0
            Player.players[_id] = self

        @staticmethod
        def get_by_name(_name):
            return [i for i in Player.players if i.name == _name][0]

        def reduce_hp(self, hp):
            self.hp -= hp

        def update_pos(self, pos, animation, class_id):
            r = self.screen.resources
            if self.mode != 0:
                return
            if r.cls_list[class_id] != self.text_class.text:
                self.text_class.text = r.cls_list[class_id]

            if self.draw.x != pos[0]:
                self.draw.x = pos[0]
                self.text_name.x = pos[0]
                self.text_class.x = pos[0]
                self.hp_display.x = pos[0]

            if self.draw.y != pos[1]:
                self.draw.y = pos[1]
                self.text_name.y = pos[1] - 1j / 20 - 1j/50
                self.text_class.y = pos[1] + 1j / 25
                self.hp_display.y = pos[1] - 1j/20
                self.draw.z = fake_atan(self.screen.cal_len_h(self.draw.y / 50))
            self.draw.img = r.animation[animation]

        def delete(self):
            _id = self.id
            Draw.remove_by_key(f"player_{_id}")
            Text.remove_by_key(f"player_{_id}")
            Text.remove_by_key(f"player_class_{_id}")
            Draw.remove_by_key(f"player_hp_{_id}")
            del Player.players[self.id]

        def set_mode(self, mode):
            if self.mode == mode:
                return
            if mode == 1:
                self.draw.disable = True
                self.text_name.disable = True
                self.text_class.disable = True
                self.hp_display.disable = True
            if mode == 0:
                self.draw.disable = False
                self.text_name.disable = False
                self.text_class.disable = False
                self.hp_display.disable = False
            self.mode = mode


    class SelfPlayer:
        def __init__(self, screen):
            self.screen = screen
            self.animation = -1
            self.direction = "r"
            self.vel = 2
            self.mode = 0  # 0 - alive, 1 - dead, 2 - spectator
            self.class_id = 0
            self.current_projectiles = []
            self.retries = 0
            self.moved = False
            self.draw = Draw.get_key("self_player")

        def get_player_desc(self):
            return [self.screen.pos_with_camera(Draw.get_key("self_player")),
                        str(self.animation // 4 + 1) + self.direction,
                        self.class_id]

        def update_pos(self):
            r = self.screen.resources
            v = self.screen.variables
            temp = [0, 0]
            if self.screen.keysHeld["w"]:
                temp[1] -= self.vel / 100
            if self.screen.keysHeld["a"]:
                self.direction = "l"
                temp[0] -= self.vel / 100
            if self.screen.keysHeld["s"]:
                temp[1] += self.vel / 100
            if self.screen.keysHeld["d"]:
                self.direction = "r"
                temp[0] += self.vel / 100

            if temp[0] ** 2 + temp[1] ** 2 >= (self.vel / 100) ** 2 * 1.5:
                temp = [i*0.7 for i in temp]

            if temp != [0, 0]:
                self.screen.move_camera(temp[0], temp[1] * 1j)
                # Draw.draw_dict["self_player"].x += temp[0]
                # Draw.draw_dict["self_player"].y += temp[1] * 1j
                # Draw.draw_dict["self_player"].z = fake_atan(cal_len_h(Draw.draw_dict["self_player"].y / 50))

                Draw.get_key("self_player").z = fake_atan(self.screen.cal_len_h((self.screen.camera_pos[1]+Draw.get_key("self_player").y) / 50))
                self.animation = (self.animation + 1) % 16
                Draw.get_key("self_player").img = r.animation[str(self.animation // 4 + 1) + self.direction]
                v.conn.send(["update_player_pos", self.get_player_desc()])
                self.moved = True
            else:
                self.animation = -1
                if self.moved:
                    v.conn.send(["update_player_pos", self.get_player_desc()])
                    self.moved = False
                try:
                    Draw.get_key("self_player").img = r.animation["0" + self.direction]
                except KeyError:
                    pass

        def get_proj(self):
            temp = list(self.current_projectiles)
            self.current_projectiles.clear()
            return temp


    class Projectile:
        # projectile_stats= {
        #   "stats": [damage, knockback, stun, duration, hit_mode]
        #   "display": [size=(circle=radius, rect=(width, height)), image, scale]
        #   "start": [velocity, angular_velocity, spread]
        # }
        # hit_mode: 0-once, 1-once per touch, 2-continuous
        # death func gets info of how the projectile died
        projectile_types = {
            "swordsman_atk": ((8, 2, 0, 12, 0),
                              (open_texture("resources/projectiles/swordsman_sword.png", flip_y=True), 1/28),
                              (0.025, 7, 0))
        }

        projectile_list = []
        current_id = 0

        # info = {
        #   "
        #
        # }

        def __init__(self, screen, _id, info):
            self.screen = screen
            self.creator_id = _id
            if _id != -1:
                self.creator = Player.players[_id]
            else:
                self.creator = None
            self.id = Projectile.current_id
            Projectile.current_id += 1

            if self.creator is None:
                temp = Draw.get_key("self_player")
                x = temp.x
                y = temp.y
            else:
                # self.creator = Player.get_by_name(info[0])
                x = complex(self.creator.draw.x)
                y = complex(self.creator.draw.y)

            self.type = info[0]
            self.angle = info[1]
            self.new_hit = True
            self.first_hit = True

            info = Projectile.projectile_types[self.type]  # <----
            self.damage = info[0][0]
            self.knockback = info[0][1]
            self.stun = info[0][2]
            self.duration = info[0][3]
            self.hit_mode = info[0][4]

            self.texture = info[1][0]
            self.width = info[1][1]

            self.vx = math.cos(self.angle) * info[2][0]
            self.vy = math.sin(self.angle) * info[2][0]

            self.angular = info[2][1]
            self.spread = info[2][2]

            self.frames = 0
            self.draw = self.screen.Draw(self.texture, (x, y, self.width, None), (0, 1), z_index=10)
            self.projectile_list.append(self)
            self.info = {}

            try:
                globals()[self.type + "_start"](self)
            except KeyError:
                pass

        def script(self):
            v = self.screen.variables
            self.draw.x += Game.dt * self.vx
            self.draw.y += Game.dt * self.vy
            self.draw.d_rot += self.angular * Game.dt

            try:
                response = globals()[self.type + "_exist"](self)
            except KeyError:
                response = None

            if v.player.mode == 0 and v.player.draw.hitbox.intersects(self.draw.hitbox):
                response1 = None
                try:
                    response1 = globals()[self.type + "_hit"](self)
                except KeyError:
                    pass
                if response1 is None and self.creator_id != -1 and ((self.hit_mode == 0 and self.first_hit) or (self.hit_mode == 1 and self.new_hit) or (self.hit_mode == 2)):
                    # Variables.player.hp -= self.damage
                    # Variables.player.hp_display.w = 1/12 * (Variables.player.hp / 100)
                    v.conn.send(["reduce_hp", self.damage])
                self.first_hit = False
                self.new_hit = False
            else:
                self.new_hit = True

            if self.duration != -1 and self.frames >= self.duration:
                try:
                    globals()[self.type + "_end"](self, response)
                except KeyError:
                    pass
                self.__class__.projectile_list.remove(self)
                self.draw.remove()

            self.frames += 1


# in game methods
if True:
    def key_list(screen):
        if True:
            for reset_key in screen.mouseDown:
                screen.mouseDown[reset_key] = False
            for reset_key in screen.mouseUp:
                screen.mouseUp[reset_key] = False
            for reset_key in screen.keysDown:
                screen.keysDown[reset_key] = False
            for reset_key in screen.keysUp:
                screen.keysUp[reset_key] = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.mouseDown[event.button] = True
                screen.mouseHeld[event.button] = True

            if event.type == pygame.MOUSEBUTTONUP:
                screen.mouseUp[event.button] = True
                screen.mouseHeld[event.button] = False

            if event.type == pygame.KEYDOWN:
                for key in screen.keysList:
                    if event.key == screen.keysList[key]:
                        screen.keysDown[key] = True
                        screen.keysHeld[key] = True

            if event.type == pygame.KEYUP:
                for key in screen.keysList:
                    if event.key == screen.keysList[key]:
                        screen.keysUp[key] = True
                        screen.keysHeld[key] = False

            if event.type == pygame.VIDEORESIZE and not screen.fullscreen:
                temp = int(screen.w)
                event.w = max(event.w, 640)
                if event.w != screen.w:
                    screen.win = pygame.display.set_mode((event.w, int(event.w / screen.aspect_ratio)), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
                    screen.w = event.w
                    screen.h = int(event.w / screen.aspect_ratio)
                else:
                    screen.win = pygame.display.set_mode((int(event.h * screen.aspect_ratio), event.h), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
                    screen.w = int(event.h * screen.aspect_ratio)
                    screen.h = event.h

                for i in Text.class_list:
                    i.size = i.size
                    i.calc_rect()

                for i in Click.class_list:
                    i.calc_rect()

                for i in Draw.class_list:
                    if i.org_img is not None:
                        i.img = i.org_img
                        i.calc_rect()

                # for i in Click.click_list:
                #     i.scale(Screen.w / temp)
                # for i in Text.text_list:
                #     i.size = i.size
                # Screen.screen_rect = pygame.Rect(0, 0, Screen.w, Screen.h)
                # OGL.setup()
            if event.type == pygame.QUIT:
                v = screen.variables
                if v.conn:
                    v.conn.quit()
                screen.run = False
                pygame.quit()
                quit()

        if screen.keysDown["F11"]:
            toggle_fullscreen(screen)

    def toggle_fullscreen(screen):
        if isinstance(screen, Click):
            screen = screen.screen
        r = screen.resources
        screen.fullscreen = not screen.fullscreen
        try:
            Draw.get_key("windowed").img = r.fullscreen if screen.fullscreen else r.windowed
        except KeyError:
            pass
        if screen.fullscreen:
            screen.win = pygame.display.set_mode(screen.size, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
            screen.w, screen.h = screen.size
        else:
            screen.win = pygame.display.set_mode((int(screen.size[0] / 2), int(screen.size[1] / 2)), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
            screen.w = screen.size[0] / 2
            screen.h = screen.size[1] / 2

        for i in Text.class_list:
            i.size = i.size
            i.calc_rect()

        for i in Click.class_list:
            i.calc_rect()

        for i in Draw.class_list:
            if i.org_img is not None:
                i.img = i.org_img
                i.calc_rect()

        screen.screen_rect = pygame.Rect(0, 0, screen.w, screen.h)
        # OGL.setup()

    def toggle_sound(self=None):
        v = self.screen.variables
        r = self.screen.resources

        v.sound = not v.sound
        try:
            Draw.get_key("note").img = r.note if v.sound else r.no_note
        except KeyError:
            pass

    def toggle_music(self=None):
        v = self.screen.variables
        r = self.screen.resources

        v.music = not v.music
        try:
            Draw.get_key("double_note").img = r.double_note if v.music else r.no_double_note
        except KeyError:
            pass


def change_screen(screen, _name):
    OrderedVisual.z_sorted_list = []
    Draw.class_list = []
    Draw.class_dict = {}
    Click.class_list = []
    Click.class_dict = {}
    Text.class_list = []
    Text.class_dict = {}
    Process.class_dict = {}
    Process.class_list = []
    if _name == screen.screen:
        return
    screen.camera_pos = (0.0, 0.0)
    globals()["end_" + screen.screen](screen)
    screen.screen = _name
    globals()["start_" + screen.screen](screen)


# game methods
if True:
    def end_(screen):
        ShootingStar.s_list = []

    # menu
    if True:
        def start_menu(screen):
            r = screen.resources

            screen.Text(("by erez", "Aharoni", 1 / 60, (0, 0, 0)), (1, 1), (1.02, 1))
            screen.Click([1 / 2, 1 - 1j / 10, 1 / 6, 1j / 8], (0.5, 0.5), "start", on_hover_start=menu_green, on_hover_end=menu_white, on_click=menu_connect)
            screen.Draw(r.text_logo, [1 / 2, 1 / 6, 1 / 3, 1j / 3], (0.5, 0.5))
            screen.Draw(r.play_btn, [1 / 2, 1 - 1j / 10, 1 / 5, 1j / 5], (0.5, 0.5), "start")
            screen.Draw(r.settings_btn, [1 / 270, 1j / 270, 1 / 15, 1j / 15], (0, 0), "settings", "", 1)
            screen.Draw(r.settings_back, [1 / 270, 1j / 270, 1 / 15, 1j / 15], (0, 0), "sbg", "", 0)
            screen.Click([1 / 270, 1j / 270, 1 / 15, 1j / 15], (0, 0), "sbg", on_hover_start=menu_open_settings, on_hover_end=menu_s_white)
            screen.Text(("insert ip:", "Aharoni", 1 / 25, (255, 255, 255)), (1 / 2, 1 / 2 - 1 / 25), (0.5, 1), "ipa", z_index=2)
            screen.Text(("", "Aharoni", 1 / 20, (255, 255, 255)), (1 / 2, 1 / 2 - 1 / 25), (0.5, 0), "ip", z_index=2)
            screen.Text(("", "Aharoni", 1 / 25, (255, 255, 255)), (1 / 2, 1 / 2 - 1 / 25), (0.5, -1.5), "status", z_index=2)
            screen.Draw(r.solo_play, [1 / 27, 1 - 1j / 27, 1 / 15, 1j / 15], (0.5, 0.5), "start_solo")
            screen.Click([1 / 27, 1 - 1j / 27, 1 / 15, 1j / 15], (0.5, 0.5), on_click=menu_start_game, on_hover_start=menu_start_wtg, on_hover_end=menu_start_gtw)
            screen.Draw(r.background, (0.5, 0.5, 1, 1), (0.5, 0.5), z_index=-5)

            screen.Draw(r.walkcolor1r, [1 - 1j / 75, 1/75, 1/15, 1.25j/15], (1, 0), "test1", z_index=20)
            screen.Process(test_change)

        def end_menu(screen):
            pass

        def tick_menu(screen):
            v = screen.variables

            if screen.frame % 2 == 0:
                ShootingStar(screen)
            for i in ShootingStar.s_list:
                i.script()

            for i in [str(j) for j in range(10)]:
                if screen.keysDown[i]:
                    v.ip_inserted += i
                    Text.get_key("ip").text += i

            if screen.keysDown["."] and v.ip_inserted[-1] != "." and ":" not in v.ip_inserted:
                v.ip_inserted += "."
                Text.get_key("ip").text += "."

            if screen.keysDown[";"] and ":" not in v.ip_inserted and v.ip_inserted[-1] != ".":
                v.ip_inserted += ":"
                Text.get_key("ip").text += ":"

            if screen.keysDown["backspace"]:
                v.ip_inserted = v.ip_inserted[:-1]
                Text.get_key("ip").text = Text.get_key("ip").text[:-1]
                try:
                    Process.get_key("bsc").remove()
                    screen.Process(none, menu_backspace_combo_allow, menu_backspace_combo, 10, "bsc")
                except KeyError:
                    screen.Process(none, menu_backspace_combo_allow, menu_backspace_combo, 10, "bsc")

            if screen.keysDown["v"]:
                temp = str(pygame.scrap.get(pygame.SCRAP_TEXT), 'utf-8').replace("\0", "")

                v.ip_inserted += temp
                Text.get_key("ip").text += temp

            if screen.keysDown["a"]:
                v.ip_inserted = ""
                Text.get_key("ip").text = ""

            if screen.keysHeld["backspace"] and v.backspace_combo:
                v.ip_inserted = v.ip_inserted[:-1]
                Text.get_key("ip").text = Text.get_key("ip").text[:-1]

        def render_menu(screen):
            for i in ShootingStar.s_list:
                i.draw()

    # lobby
    if True:
        def start_lobby(screen):
            pass

        def end_lobby(screen):
            pass

        def tick_lobby(screen):
            pass

        def render_lobby(screen):
            pass

    # game
    if True:
        def start_game(screen):
            r = screen.resources
            screen.Draw(r.map, (0, 0, 2, 2j), dict_key="bg", z_index=-100)
            temp = screen.Draw(r.walkcolor0l, (0.5, 0.5, 1 / 15, 1.25j / 15), (0.5, 0.5), "self_player", "players", stick_to_camera=True)
            temp.z = fake_atan(screen.cal_len_h(Draw.get_key("self_player").y / 50))

            l = len(r.classes)
            for i in range(l):
                screen.Draw(r.classes[i], (1.01/4*1j * (i % (-(-l // 2))), (i * 2 // l) / 2, 1/4*1j, 1/2), (0.0, 0.0), "", "classes", stick_to_camera=True, z_index=100)

            for i in range(l):
                screen.Click((1.01 / 4 * 1j * (i % (-(-l // 2))), (i * 2 // l) / 2, 1 / 4 * 1j, 1 / 2), (0.0, 0.0), "", "classes", stick_to_camera=True, on_click=game_select_class(i))

        def end_game(screen):
            pass

        def tick_game(screen):
            v = screen.variables
            v.player.update_pos()
            if screen.mouseDown[3]:
                deg = math.atan2(screen.mouse_pos[1] / screen.h - 0.5, screen.mouse_pos[0] / screen.w - 0.5)
                v.player.current_projectiles.append(("swordsman_atk", deg))
                Projectile(screen, -1, ("swordsman_atk", deg))
                v.conn.send(["add_projectile", ("swordsman_atk", deg)])

            # try:
            #     if Variables.multiplier and Network.iter is not None:
            #         players, projectiles = Network.iter
            #         for user in players:
            #             if user[1] is None:
            #                 try:
            #                     Player.get_by_name(user[0]).delete()
            #                 except IndexError:
            #                     pass
            #                 continue
            #             try:
            #                 self = Player.get_by_name(user[0])
            #             except IndexError:
            #                 self = Player(user[0])
            #             self.update_pos(user[1], user[2], user[3])
            #
            # except TypeError:
            #     Network.quit()
            #     Text.text_dict["status"].text = "server closed"
            #     Process(none, menu_delete_status, frames=120)
            # user_data = UserData(
            #     pos_with_camera(Draw.draw_dict["self_player"]),
            #     str(SelfPlayer.animation // 4 + 1) + SelfPlayer.direction,
            #     SelfPlayer.class_id,
            # )
            #
            # # + - add, else replace
            # Variables.conn.send_data += {
            #     "=user_data": user_data,
            #     "+projectiles": SelfPlayer.get_proj(),
            #     "|test": keysDown["t"]
            # }
            # if keysDown["t"]:
            #     Variables.test = time.time()
            # if Variables.conn.send_data["|test"]:
            #     print("AGAGAGAGA")

            stored = v.conn.get_stored()
            for _id, cmd, *args in stored:
                # if _id == 0:
                #     if _dict["=test"]:
                #         print(time.time() - Variables.test)
                #     continue
                # if _dict["|test"]:
                #     print("YAY")
                # if "=stopped" in _dict:
                #     Player.players[_id].delete()
                #     del Variables.conn.recv_data[_id]
                #     continue
                if cmd == "reduce_hp":
                    player = Player.players[_id]
                    player.hp -= args[0]
                    if player.hp <= 0:
                        player.hp = 0
                        player.set_mode(1)
                    player.hp_display.w = 1 / 12 * (player.hp / 100)
                elif cmd == "add_player":
                    print("id", _id, args[0])
                    Player(screen, _id, args[0])
                elif cmd == "add_players":
                    for arg in args:
                        Player(screen, *arg)
                elif cmd == "update_player_pos":
                    if _id in Player.players:
                        Player.players[_id].update_pos(*args[0])
                    else:
                        print("WARNING: invalid player id was searched")
                elif cmd == "add_projectile":
                    Projectile(screen, _id, args[0])
                elif cmd == "remove_player":
                    print("12345")
                    Player.players[_id].delete()
                else:
                    print("unknown command")

            # for i in Variables.data:
            #     for proj in Network.iter[1]:
            #         Projectile(proj)
            for proj in Projectile.projectile_list:
                proj.script()
            if screen.keysDown["esc"]:
                v.conn.quit()

        def render_game(screen):
            # pygame.draw.rect(Screen.win, (255, 255, 255), (-Test.pos[0] + Screen.w / 2 - Screen.w / 20, -Test.pos[1] + Screen.h / 2 - Screen.w / 20, Screen.w, Screen.w))

            # for i in Test.other:
            #     Test.draw(i)
            pass


def main():
    screen = Screen()

    # game setters
    if True:
        pygame.display.set_caption("bean mafia")
        change_screen(screen, "menu")
        pygame.scrap.init()
        # OGL.setup()

    while screen.run:
        Game.current_time = time.time()
        Game.delta += (Game.current_time - Game.last_time) * Game.ticks_per_second
        Game.last_time = float(Game.current_time)

        while Game.delta >= 1:
            Game.dt = time.time() - Game.dt_last
            Game.dt_last = time.time()

            screen.mouse_pos = pygame.mouse.get_pos()
            key_list(screen)
            globals()["tick_" + screen.screen](screen)
            for _i in Click.class_list + Process.class_list:
                if _i.enabled:
                    _i.script()

            screen.frame += 1
            Game.frame += 1
            Game.delta -= 1

            if screen.keysHeld["j"]:
                Draw.get_key("self_player").s_rot += PI/16

            if screen.keysHeld["h"]:
                Draw.get_key("self_player").d_rot += PI/16
            screen.camera_calculated = (screen.cal_len_w(screen.camera_pos[0]), screen.cal_len_h(screen.camera_pos[1]))

        if screen.run:
            screen.win.fill((0, 0, 0))

            for _i in filter(lambda _x: _x.z < 0, OrderedVisual.z_sorted_list):
                _i.draw()

            globals()["render_" + screen.screen](screen)

            for _i in filter(lambda _x: _x.z >= 0, OrderedVisual.z_sorted_list):
                _i.draw()

            if Click.show_borders:
                for _i in Click.class_list:
                    _i.draw()

            pygame.display.flip()

        if time.time() - Game.time_start > 1:
            Game.time_start += 1
            # print(Game.frame)
            Game.frame = 0


if __name__ == "__main__":
    main()
