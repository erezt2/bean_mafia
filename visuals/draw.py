from visuals.orderedVisual import OrderedVisual
from pygame.transform import scale
from visuals.duper import duper


class Draw(OrderedVisual):
    class_list = []
    class_dict = {}
    show_hitboxes = False

    def __init__(self, screen, img, rect, alignment=(0.0, 0.0), dict_key="", class_name="", z_index=0.0, stick_to_camera=False,
                 dot_rotation=0.0, self_rotation=0.0):

        if rect[3] is None:
            if rect[2] is None:
                raise TypeError("both width and height are None")
            else:
                _w = rect[2]
                _h = rect[2] / img.get_width() * img.get_height() * 1j
        else:
            if rect[2] is None:
                _h = rect[3]
                _w = rect[3] / img.get_height() * img.get_width() * 1j
            else:
                _w = rect[2]
                _h = rect[3]
        super().__init__(screen, [rect[0], rect[1], _w, _h], alignment, dict_key, class_name,
                         stick_to_camera, z_index)

        self.d_rot = dot_rotation
        self.s_rot = self_rotation

        self.color = (255, 255, 255)
        self.is_rect = True
        self.org_img = None
        self.width = None
        if isinstance(img, tuple):
            self.width = 0
            self.color = img
        elif isinstance(img, list):
            self.width = 1
            self.color = tuple(img)
        else:
            self._img = None
            self.is_rect = False
            self.org_img = img
            self.img = self.org_img

        self.hitbox = self.get_hitbox()

    def draw(self):
        if self.disable:
            return
        if self.is_rect:
            self.hitbox = self.screen.rect(self.color, self.rect, self.width, self.stick)
        else:
            dx = self.screen.camera_calculated[0] if not self.stick else 0
            dy = self.screen.camera_calculated[1] if not self.stick else 0
            rect = (round(self.rect[0] - dx), round(self.rect[1] - dy))
            self.hitbox = self.screen.blit_rotated_texture(self.img, rect[0], rect[1], self.rect[2], self.rect[3], self.s_rot,
                                               self.alignment, self.d_rot, show_hitbox=Draw.show_hitboxes)
            # Screen.circle((0, 255, 0), (cal_len_w(self.x), cal_len_h(self.y), 5))
        # if self.hitbox is None:  # executes when blit_rotated texture is None (kinda redundant but whatever)
        #     rect = self.rect
        #     dx = Screen.camera_calculated[0] if not self.stick else 0
        #     dy = Screen.camera_calculated[1] if not self.stick else 0
        #     rect = (round(rect[0]) - dx, round(rect[1] - dy), round(rect[2]), round(rect[3]))
        #     self.hitbox = ((rect[0], rect[1]),
        #      (rect[0] + rect[2], rect[1]),
        #      (rect[0] + rect[2], rect[1] + rect[3]),
        #      (rect[0], rect[1] + rect[3]))
        # self.hitbox = Polygon(self.hitbox)

    def get_hitbox(self):
        if self.is_rect:
            hitbox = self.screen.rect(self.color, self.rect, self.width, self.stick, draw=False)
        else:
            dx = self.screen.camera_calculated[0] if not self.stick else 0
            dy = self.screen.camera_calculated[1] if not self.stick else 0
            rect = (round(self.rect[0] - dx), round(self.rect[1] - dy))
            hitbox = self.screen.blit_rotated_texture(self.img, rect[0], rect[1], self.rect[2], self.rect[3], self.s_rot,
                                          self.alignment, self.d_rot, draw=False)
        return hitbox

    # properties
    if True:
        @property
        def img(self):
            return self._img

        @img.setter
        def img(self, value):
            if not self.is_rect:
                self._img = scale(value, (round(self.screen.cal_len_w(self.w)), round(self.screen.cal_len_h(self.h))))

        @property
        def w(self):
            return self._w

        @w.setter
        def w(self, value):
            duper(super()).w = value
            self.img = self.org_img

        @property
        def h(self):
            return self._h

        @h.setter
        def h(self, value):
            duper(super()).h = value
            self.img = self.org_img
