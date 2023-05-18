from visuals.base import Base
from pygame import Rect


class Visual(Base):
    def __init__(self, screen, rect, alignment, dict_key, class_name,
                 stick_to_camera):
        super().__init__(screen, dict_key, class_name)
        self._w = rect[2]
        self._h = rect[3]
        self._x = rect[0]
        self._y = rect[1]

        self._alignment = list(alignment)

        self.stick = stick_to_camera

        self.rect = None
        self.calc_rect()

        self.disable = False

    def draw(self):
        return self.disable

    def calc_rect(self):
        self.rect = Rect(self.screen.cal_len_w(self.x - self.alignment[0] * self.w),
                                self.screen.cal_len_h(self.y - self.alignment[1] * self.h),
                                self.screen.cal_len_w(self.w), self.screen.cal_len_h(self.h))

    def translate(self, x, y):
        self.x -= x
        self.y += y

    @classmethod
    def class_action(cls, class_name, action):
        ret = []
        for self in cls.get_by_class(class_name):
            val = action(self)
            ret.append(val)
        return list(filter(lambda x: x is not None, ret))

    if True:
        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, value):
            self._x = value
            self.calc_rect()

        @property
        def y(self):
            return self._y

        @y.setter
        def y(self, value):
            self._y = value
            self.calc_rect()

        @property
        def w(self):
            return self._w

        @w.setter
        def w(self, value):
            self._w = value
            self.calc_rect()

        @property
        def h(self):
            return self._h

        @h.setter
        def h(self, value):
            self._h = value
            self.calc_rect()

        @property
        def alignment(self):
            return self._alignment

        @alignment.setter
        def alignment(self, value):
            self._alignment = value
            self.calc_rect()
