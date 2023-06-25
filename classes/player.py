from state.functions import fake_atan
from visuals.draw import Draw
from visuals.text import Text


class Player:
    players = {}

    def __init__(self, screen, _id, _name):
        self.screen = screen
        r = screen.info("resources")
        self.id = _id
        self.hp = 100

        self.name = _name
        self.draw = self.screen.Draw(r.walkcolor0l, (0, 0, 1 / 15, 1.25j / 15), (0.5, 0.5),
                                     f"player_{_id}", f"player_{_id}")
        self.draw.z = fake_atan(screen.cal_len_h(Draw.get_key("self_player").y / 50))
        self.text_name = self.screen.Text((_name, "arial", 1 / 35, (255, 255, 255)), (0, 0), (0.5, 0.65),
                                          f"player_{_id}", f"player_{_id}", z_index=-15) # z=-30
        self.text_class = self.screen.Text(("", "arial", 1 / 35, (255, 255, 255)), (0, 0), (0.5, 0),
                                           f"player_class_{_id}", f"player_{_id}", z_index=-15)
        self.hp_display = self.screen.Draw((0, 255, 0), (0, 0, 1 / 12, 1 / 45), (0.5, 0.5), f"player_hp_{_id}",
                                           f"player_{_id}", z_index=15)
        self.mode = 0
        Player.players[_id] = self

    @staticmethod
    def get_by_name(_name):
        return [i for i in Player.players if i.name == _name][0]

    def reduce_hp(self, hp):
        self.hp -= hp

    def update_pos(self, pos, animation, class_id):
        r = self.screen.info("resources")
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
            self.text_name.y = pos[1] - 1j / 20 - 1j / 50
            self.text_class.y = pos[1] + 1j / 25
            self.hp_display.y = pos[1] - 1j / 20
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
