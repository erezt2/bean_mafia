from state.functions import open_texture
from classes.player import Player
from visuals.draw import Draw
from state.game import Game
import math


PI = 3.14159265359


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
                          (open_texture("resources/projectiles/swordsman_sword.png", flip_y=True), 1 / 28),
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
            if response1 is None and self.creator_id != -1 and (
                    (self.hit_mode == 0 and self.first_hit) or (self.hit_mode == 1 and self.new_hit) or (
                    self.hit_mode == 2)):
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
