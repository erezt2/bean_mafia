from visuals.base import Base


def none(self=None):
    pass


class Process(Base):
    class_list = []
    class_dict = {}

    def __init__(self, screen, func=none, remove_func=none, add_func=none, frames=-1, dict_key="", class_name="", arg=None):
        add_func(self)
        if dict_key in self.__class__.class_dict:
            return
        if arg is None:
            arg = []
        super().__init__(screen, dict_key, class_name)
        self.remove_func = remove_func
        self.func = func
        self.frames = frames
        self.frame = 0
        self.arg = arg
        self.enabled = True

    def remove(self):
        self.remove_func(self)
        super().remove()

    def script(self):
        if self not in self.__class__.class_list:
            return
        if self.frame < self.frames or self.frames == -1:
            self.frame += 1
            self.func(self)
        else:
            self.remove()

    def toggle_process(self):
        self.enabled = not self.enabled
