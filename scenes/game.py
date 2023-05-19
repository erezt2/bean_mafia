from classes.player import Player
from classes.projectile import Projectile
from visuals.draw import Draw
from visuals.click import Click
from state.functions import fake_atan
import math


def game_select_class(index):
    def func_wrapper(self=None):
        v = self.screen.variables
        v.player.class_id = index
        Click.remove_by_class("classes")
        Draw.remove_by_class("classes")

    return func_wrapper


def start(screen):
    r = screen.resources
    screen.Draw(r.map, (0, 0, 2, 2j), dict_key="bg", z_index=-100)
    temp = screen.Draw(r.walkcolor0l, (0.5, 0.5, 1 / 15, 1.25j / 15), (0.5, 0.5), "self_player", "players",
                       stick_to_camera=True)
    temp.z = fake_atan(screen.cal_len_h(Draw.get_key("self_player").y / 50))

    l = len(r.classes)
    for i in range(l):
        screen.Draw(r.classes[i], (1.01 / 4 * 1j * (i % (-(-l // 2))), (i * 2 // l) / 2, 1 / 4 * 1j, 1 / 2), (0.0, 0.0),
                    "", "classes", stick_to_camera=True, z_index=100)

    for i in range(l):
        screen.Click((1.01 / 4 * 1j * (i % (-(-l // 2))), (i * 2 // l) / 2, 1 / 4 * 1j, 1 / 2), (0.0, 0.0), "",
                     "classes", stick_to_camera=True, on_click=game_select_class(i))


def end(screen):
    pass


def tick(screen):
    v = screen.variables
    v.player.update_pos()
    if screen.mouseDown[3]:
        deg = math.atan2(screen.mouse_pos[1] / screen.h - 0.5, screen.mouse_pos[0] / screen.w - 0.5)
        v.player.current_projectiles.append(("swordsman_atk", deg))
        Projectile(screen, -1, ("swordsman_atk", deg))
        v.conn.send(["add_projectile", ("swordsman_atk", deg)])

    # try:
    #     if Variables.multiplier and Network.iter is not None:
    #         players, projectiles = Network.iter
    #         for user in players:
    #             if user[1] is None:
    #                 try:
    #                     Player.get_by_name(user[0]).delete()
    #                 except IndexError:
    #                     pass
    #                 continue
    #             try:
    #                 self = Player.get_by_name(user[0])
    #             except IndexError:
    #                 self = Player(user[0])
    #             self.update_pos(user[1], user[2], user[3])
    #
    # except TypeError:
    #     Network.quit()
    #     Text.text_dict["status"].text = "server closed"
    #     Process(none, menu_delete_status, frames=120)
    # user_data = UserData(
    #     pos_with_camera(Draw.draw_dict["self_player"]),
    #     str(SelfPlayer.animation // 4 + 1) + SelfPlayer.direction,
    #     SelfPlayer.class_id,
    # )
    #
    # # + - add, else replace
    # Variables.conn.send_data += {
    #     "=user_data": user_data,
    #     "+projectiles": SelfPlayer.get_proj(),
    #     "|test": keysDown["t"]
    # }
    # if keysDown["t"]:
    #     Variables.test = time.time()
    # if Variables.conn.send_data["|test"]:
    #     print("AGAGAGAGA")

    stored = v.conn.get_stored()
    for _id, cmd, *args in stored:
        # if _id == 0:
        #     if _dict["=test"]:
        #         print(time.time() - Variables.test)
        #     continue
        # if _dict["|test"]:
        #     print("YAY")
        # if "=stopped" in _dict:
        #     Player.players[_id].delete()
        #     del Variables.conn.recv_data[_id]
        #     continue
        if cmd == "reduce_hp":
            player = Player.players[_id]
            player.hp -= args[0]
            if player.hp <= 0:
                player.hp = 0
                player.set_mode(1)
            player.hp_display.w = 1 / 12 * (player.hp / 100)
        elif cmd == "add_player":
            print("id", _id, args[0])
            Player(screen, _id, args[0])
        elif cmd == "add_players":
            for arg in args:
                Player(screen, *arg)
        elif cmd == "update_player_pos":
            if _id in Player.players:
                Player.players[_id].update_pos(*args[0])
            else:
                print("WARNING: invalid player id was searched")
        elif cmd == "add_projectile":
            Projectile(screen, _id, args[0])
        elif cmd == "remove_player":
            print("12345")
            Player.players[_id].delete()
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
