from visuals.orderedVisual import OrderedVisual
from pygame.font import SysFont


class Text(OrderedVisual):
    class_list = []
    class_dict = {}

    def __init__(self, screen, text, point, alignment=(0.0, 0.0), dict_key="", class_name="", z_index=0, stick_to_camera=False):
        self._text = text[0]
        self._font = text[1]
        self._size = text[2]
        self.color = text[3]
        self.surface = SysFont(self.font, round(screen.cal_len_w(self.size))).render(self.text, False, self.color)
        txt = self.surface.get_rect()
        _w = txt.width / screen.w
        _h = txt.height / screen.h
        super().__init__(screen, [point[0], point[1], _w, _h], alignment, dict_key, class_name,
                         stick_to_camera, z_index)

        self.point = list(point)

    def draw(self):
        if self.disable:
            return
        self.screen.blit(self.surface, self.rect[0:2], self.stick)
        # Screen.win.blit(self.surface, (int(self.x), int(self.y - self.surface.get_rect().height * self.alignment[1])))

    # def scale(self, scalar):
    # self.size *= scalar
    # self.x *= scalar
    # self.y *= scalar
    # self.surface = pygame.font.SysFont(self.font, int(self.size)).render(self.text, False, self.color)

    # properties
    if True:
        @property
        def text(self):
            return self._text

        @text.setter
        def text(self, value):
            self._text = value
            self.surface = SysFont(self.font, round(self.screen.cal_len_w(self.size))).render(self.text, False,
                                                                                              self.color)
            self._w = self.surface.get_rect().width / self.screen.w
            self._h = self.surface.get_rect().height / self.screen.h
            self.calc_rect()

        @property
        def font(self):
            return self._font

        @font.setter
        def font(self, value):
            self._font = value
            self.surface = SysFont(self.font, round(self.screen.cal_len_w(self.size))).render(self.text, False,
                                                                                              self.color)
            self._w = self.surface.get_rect().width / self.screen.w
            self._h = self.surface.get_rect().height / self.screen.h
            self.calc_rect()

        @property
        def size(self):
            return self._size

        @size.setter
        def size(self, value):
            self._size = value
            self.surface = SysFont(self.font, round(self.screen.cal_len_w(self.size))).render(self.text, False,
                                                                                              self.color)
            self._w = self.surface.get_rect().width / self.screen.w
            self._h = self.surface.get_rect().height / self.screen.h
            self.calc_rect()

        @property
        def w(self):
            return self._w

        @w.setter
        def w(self, value):
            raise "Can't change the width of text. use size"

        @property
        def h(self):
            return self._h

        @h.setter
        def h(self, value):
            raise "Can't change the width of text. use size"
        # @property
        # def color(self):
        #     return self._color
        #
        # @color.setter
        # def color(self, value):
        #     self._color = value
        #     self.surface = pygame.font.SysFont(self.font, int(self.size)).render(self.text, False, self.color)
