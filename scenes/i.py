from classes.projectile import Projectile


def add_variables(self):
    v = self.info
    self.enabled = False
    self.immune = True

    v.menu_settings_open = False
    v.sound = True
    v.music = True
    v.fullscreen = False
    v.ip_inserted = ""
    v.backspace_combo = True
    v.conn = None
    v.server = None
    v.stop_event = None
    v.player = None
    v.freeze_player = False
    v.test = 0


def end(screen):
    Projectile.projectile_list = []
    screen.Process(dict_key="variables", add_func=add_variables)
