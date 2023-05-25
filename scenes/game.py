from classes.player import Player
from classes.projectile import Projectile
from visuals.draw import Draw
from visuals.click import Click
from state.functions import fake_atan
from visuals.process import Process
import math


def none(s):
    pass


def game_select_class(index):
    def func_wrapper(self=None):
        v = self.screen.variables
        v.player.class_id = index
        Click.remove_by_class("classes")
        Draw.remove_by_class("classes")
        v.freeze_player = False
    return func_wrapper


def showcase_class(index):
    def func_wrapper(self=None):
        r = self.screen.resources
        Draw.get_key("class_showcase").img = r.classes[index]
    return func_wrapper


def attack_e_cooldown_start(self):
    d = Draw.get_key("e_cooldown")
    d.w = 1/15


def attack_e_cooldown_exists(self):
    d = Draw.get_key("e_cooldown")
    d.w = 1/15*(self.frames - self.frame) / self.frames


def attack_q_cooldown_start(self):
    d = Draw.get_key("q_cooldown")
    d.w = 1/15


def attack_q_cooldown_exists(self):
    d = Draw.get_key("q_cooldown")
    d.w = 1/15*(self.frames - self.frame) / self.frames


def sw_e_end(self):
    v = self.screen.variables
    v.player.vel -= 0.6


def sw_q_end(self):
    v = self.screen.variables
    v.player.vel += 0.3
    v.player.defense -= 8.5


def mg_q_end(self):
    v = self.screen.variables
    v.player.vel -= 0.6


def swordsman_handle(screen):
    v = screen.variables

    if screen.mouseDown[1] and not Process.get_key("q_attack_exists") and not Process.get_key("normal_attack"):
        deg = math.atan2(screen.mouse_pos[1] / screen.h - 0.5, screen.mouse_pos[0] / screen.w - 0.5)
        # v.player.current_projectiles.append(("swordsman_atk", deg))

        proj = "swordsman_atk"
        if Process.key_exists("e_attack_exists"):
            proj = "swordsman_atk_e"
        Projectile(screen, -1, (proj, deg))
        # v.conn.send(["add_projectile", (proj, deg)])

        screen.Process(frames=4, dict_key="normal_attack")

    if not Process.get_key("e_attack") and screen.keysDown["e"]:
        screen.Process(attack_e_cooldown_exists, none, attack_e_cooldown_start, frames=450, dict_key="e_attack")
        screen.Process(remove_func=sw_e_end, frames=90, dict_key="e_attack_exists")
        v.player.vel += 0.6

    if not Process.get_key("q_attack") and screen.keysDown["q"]:
        screen.Process(attack_q_cooldown_exists, none, attack_q_cooldown_start, frames=300, dict_key="q_attack")
        screen.Process(remove_func=sw_q_end, frames=80, dict_key="q_attack_exists")
        v.player.vel -= 0.3
        v.player.defense += 8.5


def magician_handle(screen):
    v = screen.variables
    if screen.mouseDown[1] and not Process.key_exists("e_attack_exists") and not Process.get_key("normal_attack"):
        deg = math.atan2(screen.mouse_pos[1] / screen.h - 0.5, screen.mouse_pos[0] / screen.w - 0.5)
        proj = "magician_atk"
        Projectile(screen, -1, (proj, deg))
        # v.conn.send(["add_projectile", (proj, deg)])
        Projectile(screen, -1, (proj, deg))
        # v.conn.send(["add_projectile", (proj, deg)])
        screen.Process(frames=6, dict_key="normal_attack")

    if not Process.get_key("e_attack") and screen.keysDown["e"]:
        screen.Process(attack_e_cooldown_exists, none, attack_e_cooldown_start, frames=450, dict_key="e_attack")
        screen.Process(frames=30, dict_key="e_attack_exists")
        Projectile(screen, -1, ("magician_knockback", 0))

    if not Process.get_key("q_attack") and screen.keysDown["q"]:
        screen.Process(attack_q_cooldown_exists, none, attack_q_cooldown_start, frames=300, dict_key="q_attack")
        screen.Process(remove_func=mg_q_end, frames=80, dict_key="q_attack_exists")
        v.player.vel += 0.6


# ["archer", "assassin", "magician", "marksman", "spearsman", "swordsman", "darkmage", "glasscannon", "ninja", "priest"]
class_handlers = [none, none, magician_handle, none, none, swordsman_handle, none, none, none, none]


def start(screen):
    r = screen.resources
    v = screen.variables

    v.freeze_player = True
    screen.Draw(r.map, (0, 0, 2, 2j), dict_key="bg", z_index=-100)
    temp = screen.Draw(r.walkcolor0l, (0.5, 0.5, 1 / 15, 1.25j / 15), (0.5, 0.5), "self_player", "players",
                       stick_to_camera=True)
    temp.z = fake_atan(screen.cal_len_h(Draw.get_key("self_player").y / 50))

    l = len(r.classes)
    for i in range(l):
        screen.Draw(r.classes[i], (1.01 / 4 * 1j * (i % (-(-l // 2))), (i * 2 // l) / 2, 1 / 4 * 1j, 1 / 2), (0.0, 0.0),
                    "", "classes", stick_to_camera=True, z_index=100)
    screen.Draw(r.classes[0], (1, 0, 1j/2, 1), (1, 0), dict_key="class_showcase", class_name="classes", stick_to_camera=True, z_index=100)
    for i in range(l):
        screen.Click((1.01 / 4 * 1j * (i % (-(-l // 2))), (i * 2 // l) / 2, 1 / 4 * 1j, 1 / 2), (0.0, 0.0), "",
                     "classes", stick_to_camera=True, on_click=game_select_class(i), on_hover_start=showcase_class(i))

    screen.Draw((20, 20, 20), (1-1/100-1/15, 1-1j/100-1j/15, 1/15, 1j/15), (0, 0), stick_to_camera=True, z_index=49)
    screen.Draw((120, 120, 120), (1 - 1 / 100 - 1 / 15, 1 - 1j / 100 - 1j / 15, 0, 1j / 15), (0, 0), stick_to_camera=True, z_index=50, dict_key="q_cooldown")
    screen.Text(["Q", "Aharoni", 1 / 20, (200, 200, 200)], (1-1/100-1/30, 1-1j/100), (0.5, 1), stick_to_camera=True, z_index=51)

    screen.Draw((20, 20, 20), (1 - 1 / 50 - 2 / 15, 1 - 1j / 100 - 1j / 15, 1 / 15, 1j / 15), (0, 0), stick_to_camera=True, z_index=49)
    screen.Draw((120, 120, 120), (1 - 1 / 50 - 2 / 15, 1 - 1j / 100 - 1j / 15, 0, 1j / 15), (0, 0), stick_to_camera=True, z_index=50, dict_key="e_cooldown")
    screen.Text(["E", "Aharoni", 1 / 20, (200, 200, 200)], (1 - 2 / 100 - 3 / 30, 1 - 1j / 100), (0.5, 1), stick_to_camera=True, z_index=51)


def end(screen):
    pass


def tick(screen):
    v = screen.variables

    if not v.freeze_player:
        v.player.update_pos()

    if screen.keysDown["p"]:
        print(v.player.mode)

    if not v.player.stun and v.player.mode == 0:
        class_handlers[v.player.class_id](screen)

    stored = v.conn.get_stored()
    if None in stored:
        v.conn.quit()
        return

    for _id, cmd, *args in stored:
        if cmd == "reduce_hp":
            player = Player.players[_id]
            player.hp -= args[0]
            if player.hp <= 0:
                player.hp = 0
                player.set_mode(1)
            player.hp_display.w = 1 / 12 * (player.hp / 100)
        elif cmd == "add_player":
            if _id not in Player.players:
                Player(screen, _id, args[0])
                v.conn.send(["update_player_pos", v.player.get_player_desc()])
        elif cmd == "add_players":
            for arg in args:
                Player(screen, *arg)
        elif cmd == "update_player_pos":
            if _id in Player.players:
                Player.players[_id].update_pos(*args[0])
            else:
                v.conn.send(["requesting_player", _id])
        elif cmd == "add_projectile":
            Projectile(screen, _id, args[0])
        elif cmd == "remove_player":
            Player.players[_id].delete()
        elif cmd == "requesting_player":
            if args[0] == v.conn.id:
                v.conn.send(["add_player", v.conn.name])
        else:
            print("unknown command")

    # for i in Variables.data:
    #     for proj in Network.iter[1]:
    #         Projectile(proj)
    for proj in Projectile.projectile_list:
        proj.script()
    if screen.keysDown["esc"]:
        v.conn.quit()


def render(screen):
    # pygame.draw.rect(Screen.win, (255, 255, 255), (-Test.pos[0] + Screen.w / 2 - Screen.w / 20, -Test.pos[1] + Screen.h / 2 - Screen.w / 20, Screen.w, Screen.w))

    # for i in Test.other:
    #     Test.draw(i)
    pass
