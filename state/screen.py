from visuals.click import Click
from state.functions import *
import pygame
from shapely.geometry import Polygon
import math
from state.variables import Variables
from state.resources import Resources
from visuals.draw import Draw
from visuals.click import Click
from visuals.process import Process
from visuals.text import Text


pygame.init()


def none(self=None):
    pass


class Screen:
    initial = 3

    def __init__(self):
        with open("settings", "r") as file:
            windows_text_scaling = int(file.readlines()[1])
            self.size = (int(pygame.display.Info().current_w / windows_text_scaling * 100),
                         int(pygame.display.Info().current_h / windows_text_scaling * 100))
        self.aspect_ratio = pygame.display.Info().current_w / pygame.display.Info().current_h
        self.win = pygame.display.set_mode((int(self.size[0] / self.initial), int(self.size[1] / self.initial)),
                                           pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)

        self.w = self.size[0] / self.initial
        self.h = self.size[1] / self.initial

        self.fullscreen = False
        self.run = True
        self.screen = ""
        self.frame = 0
        self.last_frame = 0

        self.mouse_pos = (0, 0)
        self.camera_pos = (0.0, 0.0)
        self.camera_calculated = (0.0, 0.0)

        self.screen_rect = pygame.Rect(0, 0, self.w, self.h)

        self.keysList = {
            "a": pygame.K_a,
            "b": pygame.K_b,
            "c": pygame.K_c,
            "d": pygame.K_d,
            "e": pygame.K_e,
            "f": pygame.K_f,
            "g": pygame.K_g,
            "h": pygame.K_h,
            "i": pygame.K_i,
            "j": pygame.K_j,
            "k": pygame.K_k,
            "l": pygame.K_l,
            "m": pygame.K_m,
            "n": pygame.K_n,
            "o": pygame.K_o,
            "p": pygame.K_p,
            "q": pygame.K_q,
            "r": pygame.K_r,
            "s": pygame.K_s,
            "t": pygame.K_t,
            "u": pygame.K_u,
            "v": pygame.K_v,
            "w": pygame.K_w,
            "x": pygame.K_x,
            "y": pygame.K_y,
            "z": pygame.K_z,
            "space": pygame.K_SPACE,
            "1": pygame.K_1,
            "2": pygame.K_2,
            "3": pygame.K_3,
            "4": pygame.K_4,
            "5": pygame.K_5,
            "6": pygame.K_6,
            "7": pygame.K_7,
            "8": pygame.K_8,
            "9": pygame.K_9,
            "0": pygame.K_0,
            "num0": pygame.K_KP0,
            "num1": pygame.K_KP1,
            "num2": pygame.K_KP2,
            "num3": pygame.K_KP3,
            "num4": pygame.K_KP4,
            "num5": pygame.K_KP5,
            "num6": pygame.K_KP6,
            "num7": pygame.K_KP7,
            "num8": pygame.K_KP8,
            "num9": pygame.K_KP9,
            "numDel": pygame.K_KP_PERIOD,
            "up": pygame.K_UP,
            "right": pygame.K_RIGHT,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "shift": pygame.K_LSHIFT,
            "ctrl": pygame.K_LCTRL,
            "esc": pygame.K_ESCAPE,
            "tab": pygame.K_TAB,
            "+": pygame.K_KP_PLUS,
            "-": pygame.K_KP_MINUS,
            ";": pygame.K_SEMICOLON,
            "del": pygame.K_DELETE,
            "\'": pygame.K_QUOTE,
            ".": pygame.K_PERIOD,
            ",": pygame.K_COMMA,
            "?": pygame.K_SLASH,
            "_": pygame.K_MINUS,
            "NP_enter": pygame.K_KP_ENTER,
            "enter": pygame.K_RETURN,
            "backspace": pygame.K_BACKSPACE,
            "F1": pygame.K_F1,
            "F2": pygame.K_F2,
            "F3": pygame.K_F3,
            "F4": pygame.K_F4,
            "F5": pygame.K_F5,
            "F6": pygame.K_F6,
            "F7": pygame.K_F7,
            "F8": pygame.K_F8,
            "F9": pygame.K_F9,
            "F10": pygame.K_F10,
            "F11": pygame.K_F11,
            "F12": pygame.K_F12,
        }
        self.mouseDown = {key + 1: False for key in range(7)}
        self.keysDown = {key: False for key in self.keysList}
        self.mouseHeld = {key + 1: False for key in range(7)}
        self.keysHeld = {key: False for key in self.keysList}
        self.mouseUp = {key + 1: False for key in range(7)}
        self.keysUp = {key: False for key in self.keysList}

        self.variables = Variables
        self.resources = Resources

    def move_camera(self, x, y):
        self.camera_pos = (self.camera_pos[0] + x, self.camera_pos[1] + y)

    def rect(self, color, rect, width=0, camera=True, draw=True):
        if isinstance(color[0], int):
            multicolor = False
        else:
            multicolor = True
            color = color[0]

        dx = self.camera_calculated[0] if not camera else 0
        dy = self.camera_calculated[1] if not camera else 0
        rect = (round(rect[0]) - dx, round(rect[1] - dy), round(rect[2]), round(rect[3]))
        if draw:
            pygame.draw.rect(self.win, color, rect, width)
        return Polygon(((rect[0], rect[1]),
                        (rect[0] + rect[2], rect[1]),
                        (rect[0] + rect[2], rect[1] + rect[3]),
                        (rect[0], rect[1] + rect[3])))
        # if width:
        #     temp2 = (
        #         (0, 1),
        #         (0, 3),
        #         (2, 1),
        #         (2, 3),
        #     )
        #
        #     glBegin(GL_LINES)
        #     if not multicolor:
        #         glColor4fv(color)
        #     for i in (0, 1, 2, 3):
        #         if multicolor:
        #             glColor4fv(color[i])
        #         for j in temp2[i]:
        #             glVertex2fv(rect[j])
        # else:
        #     glBegin(GL_QUADS)
        #     if not multicolor:
        #         glColor4fv(color)
        #     for i in (0, 1, 2, 3):
        #         if multicolor:
        #             glColor4fv(color[i])
        #         glVertex2fv(rect[i])
        # glEnd()

    def blit(self, image, rect, camera=True):
        dx = self.camera_calculated[0] if not camera else 0
        dy = self.camera_calculated[1] if not camera else 0
        rect = (round(rect[0] - dx), round(rect[1] - dy))
        self.win.blit(image, rect)

    def circle(self, color, circle, width=0, camera=True):
        dx = self.camera_calculated[0] if not camera else 0
        dy = self.camera_calculated[1] if not camera else 0
        pos = (round(circle[0] - dx), round(circle[1] - dy))
        pygame.draw.circle(self.win, color, pos, round(circle[2]), width)

    def cal_len_w(self, num):
        return num.real * self.w + num.imag * self.h

    def cal_len_h(self, num):
        return num.real * self.h + num.imag * self.w

    def blit_rotated_texture(self, image, x, y, w=None, h=None, rot=0.0,
                             point=(0, 0), point_rot=0.0, hitbox_rot=0.0,
                             draw=True, show_hitbox=False):  # hitbox rot usless for only blitting purposes
        if w is None:
            w = image.get_width()
        if h is None:
            h = image.get_height()

        if error_range(rot % (2 * PI)) and error_range(point_rot % (2 * PI)) and error_range(hitbox_rot % (2 * PI)):
            if draw:
                self.win.blit(image, (round(x), round(y)))
            # dx = Screen.camera_calculated[0] if not camera else 0
            # dy = Screen.camera_calculated[1] if not camera else 0d
            dx = dy = 0
            rect = (x - dx, y - dy, w, h)
            hitbox = ((rect[0] + dx, rect[1]),
                      (rect[0] + dx + rect[2], rect[1]),
                      (rect[0] + rect[2], rect[1] + rect[3]),
                      (rect[0], rect[1] + rect[3]))
        else:
            np0 = (1 / 2 - point[0]) * w
            np1 = (1 / 2 - point[1]) * h
            off0 = w / 2 - point[0] * w * 2
            off1 = h / 2 - point[1] * h * 2
            # w / 2 --> -3w / 2
            x += np0
            y += np1

            hitbox = []
            rect_radius = math.sqrt(h ** 2 + w ** 2) / 2
            try:
                rect_angle = math.atan(h / w)
            except ZeroDivisionError:
                rect_angle = PI / 2

            rotated_image = pygame.transform.rotate(image, -1 * (rot + point_rot) / PI * 180)
            new_rect = rotated_image.get_rect(center=image.get_rect(center=(
                round(x + math.sqrt(np0 ** 2 + np1 ** 2) * math.cos(math.atan2(np1, np0) + point_rot)),
                round(y + math.sqrt(np0 ** 2 + np1 ** 2) * math.sin(math.atan2(np1, np0) + point_rot)))).center)
            if draw:
                self.win.blit(rotated_image, (round(new_rect.topleft[0] - off0), round(new_rect.topleft[1] - off1)))
            for dot in range(4):
                temp_angle = (1 if dot % 2 == 0 else -1) * rect_angle + (PI if dot in (0, 3) else 0) + rot + hitbox_rot
                temp2_angle = math.atan2(rect_radius * math.sin(temp_angle) + np1,
                                         rect_radius * math.cos(temp_angle) + np0) + point_rot
                temp = rect_radius ** 2 + np1 ** 2 + np0 ** 2 + 2 * rect_radius * (
                        np0 * math.cos(temp_angle) + np1 * math.sin(temp_angle))
                if temp < 0:
                    temp = 0
                temp2_radius = math.sqrt(temp)
                hitbox.append((round(x + math.cos(temp2_angle) * temp2_radius - off0),
                               round(y + math.sin(temp2_angle) * temp2_radius - off1)))
        # pygame.draw.polygon(Screen.win, (255, 255, 255), hitbox, 2)
        if show_hitbox:
            pygame.draw.polygon(self.win, (255, 0, 0), hitbox, 2)
        return Polygon(hitbox)

    def pos_with_camera(self, obj):
        dx = self.camera_pos[0] if obj.stick else 0
        dy = self.camera_pos[1] if obj.stick else 0
        return obj.x + dx, obj.y + dy

    def Click(self, rect, alignment=(0.0, 0.0), dict_key="", class_name="", stick_to_camera=False,
                    on_hover_start=none, on_hover=none, on_hover_end=none, on_click=none, on_hold=none, on_release=none):
        return Click(self, rect, alignment, dict_key, class_name, stick_to_camera,
                        on_hover_start, on_hover, on_hover_end, on_click, on_hold, on_release)

    def Draw(self, img, rect, alignment=(0.0, 0.0), dict_key="", class_name="", z_index=0.0,
                 stick_to_camera=False, dot_rotation=0.0, self_rotation=0.0):
        return Draw(self, img, rect, alignment, dict_key, class_name, z_index,
                    stick_to_camera, dot_rotation, self_rotation)

    def Process(self, func=none, remove_func=none, add_func=none, frames=-1, dict_key="", class_name="", arg=None):
        return Process(self, func, remove_func, add_func, frames, dict_key, class_name, arg)

    def Text(self, text, point, alignment=(0.0, 0.0), dict_key="", class_name="", z_index=0, stick_to_camera=False):
        return Text(self, text, point, alignment, dict_key, class_name, z_index, stick_to_camera)
