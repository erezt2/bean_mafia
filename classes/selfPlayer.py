from state.functions import fake_atan
from visuals.draw import Draw


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
        self.hp_bar = screen.Draw((0, 255, 0), (1/200, 1-1j/200, 1/3, 1/25), (0, 1), z_index=100, stick_to_camera=True)

        self.hp = 100

    def damage(self, damage):
        self.screen.variables.conn.send(["reduce_hp", damage])
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        self.hp_bar.w = 1/3 * self.hp / 100
        print(self.hp_bar.w)

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
            temp = [i * 0.7 for i in temp]

        if temp != [0, 0]:
            self.screen.move_camera(temp[0], temp[1] * 1j)

            Draw.get_key("self_player").z = fake_atan(
                self.screen.cal_len_h((self.screen.camera_pos[1] + Draw.get_key("self_player").y) / 50))
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
