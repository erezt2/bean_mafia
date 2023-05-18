from visuals.visual import Visual


def none(self=None):
    pass


class Click(Visual):
    show_borders = False
    class_list = []
    class_dict = {}

    def __init__(self, screen, rect, alignment=(0.0, 0.0), dict_key="", class_name="", stick_to_camera=False,
                 on_hover_start=none, on_hover=none, on_hover_end=none, on_click=none, on_hold=none, on_release=none):
        super().__init__(screen, rect, alignment, dict_key, class_name,
                         stick_to_camera)
        self.on_hover_start = on_hover_start
        self.on_hover = on_hover
        self.on_hover_end = on_hover_end
        self.on_click = on_click
        self.on_hold = on_hold
        self.on_release = on_release

        self.is_held = False
        self.held_frames = 0
        self.is_hovering = False
        self.inside = False
        self.hover_frames = 0
        self.enabled = True

    def script(self):
        screen = self.screen
        inside = self.rect.collidepoint(*screen.mouse_pos)
        self.inside = inside
        if inside:
            if self.is_hovering:
                self.on_hover(self)
                self.hover_frames += 1
            else:
                self.is_hovering = True
                self.on_hover_start(self)

            if screen.mouseDown[1]:
                self.is_held = True
                self.on_click(self)

        elif self.is_hovering:
            self.on_hover_end(self)
            self.is_hovering = False
            self.hover_frames = 0

        if self.is_held:
            if screen.mouseUp[1]:
                self.on_release(self)
                self.is_held = False
                self.held_frames = 0
            else:
                self.on_hold(self)
                self.held_frames += 1

    def draw(self):
        self.screen.rect((255, 0, 0, 0.4), self.rect, 1, self.stick)

    def toggle_button(self):
        self.enabled = not self.enabled
