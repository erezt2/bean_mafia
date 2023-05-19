import server, pygame, threading, socket
from visuals.draw import Draw
from visuals.click import Click
from visuals.process import Process
from visuals.text import Text
from classes.shootingStar import ShootingStar
from connection import Connection
import protocol

PI = 3.14159265359


def none(self=None):
    pass


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


def game_remove_ipc(self=None):
    Text.remove_by_key("ipc")


def menu_retract_finish(self=None):
    Draw.remove_by_key("note")
    Draw.remove_by_key("double_note")
    Draw.remove_by_key("windowed")
    Draw.get_key("sbg").h = 1j / 15
    Click.get_key("sbg").h = 1j / 15
    Draw.get_key("settings").y = 1j / 270


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
    self.screen.Text(["ip copied", "Aharoni", 1 / 25, (150, 150, 150)], (1 / 200, 1), (0, 1), "ipc",
                     stick_to_camera=True)
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


def menu_green(self=None):
    Draw.get_key("start").w *= 0.95
    Draw.get_key("start").h *= 0.95


def menu_white(self=None):
    Draw.get_key("start").w /= 0.95
    Draw.get_key("start").h /= 0.95


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
        screen.Click((1 / 27, 1j / 27 + 8 * 1j / 45, 1 / 15, 1j / 20), (0.5, 0.5), "", "settings", on_click=lambda c: c.screen.toggle_fullscreen())
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


def menu_s_white(self=None):
    self.screen.Process(menu_retract_settings, menu_retract_finish, none, 9, "sbgr")
    if Process.key_exists("sbg"):
        Process.remove_by_key("sbg")
    self.screen.variables.menu_settings_open = False


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


def start(screen):
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

    screen.Draw(r.walkcolor1r, [1 - 1j / 75, 1/ 75, 1 / 15, 1.25j / 15], (1, 0), "test1", z_index=20)
    screen.Process(test_change)


def end(screen):
    pass


def tick(screen):
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


def render(screen):
    for i in ShootingStar.s_list:
        i.draw()
