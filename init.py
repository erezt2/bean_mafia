import random,  socket, server, protocol
import threading
import time

from state.screen import Screen
from visuals.orderedVisual import OrderedVisual
from state.game import Game
import pygame
import math
from state.functions import *
from visuals.draw import Draw
from visuals.click import Click
from visuals.process import Process
from visuals.text import Text

# from _interface import *
# from _fundementals import *
# from OpenGL.GL import *
# from OpenGL.GLU import *
from shapely.geometry import Polygon

PI = 3.14159265359


# functions
if True:
    def none(self=None):
        pass

    def debug(self=None):
        print("debug: " + str(self))

# game classes

    # class ABCD:
    #     h = 10 * (2 ** (1 / 2) - 1)
    #     w = h * Screen.aspect_ratio
    #
    #     perspective = (45, Screen.aspect_ratio, 4.99, 5.01)
    #     translate = (0.0, 0.0, -5.0)
    #     rotate = (0, 0, 0, 0)
    #
    #     camera_pos = (0.0, 0.0)
    #     # vbo = glGenBuffers(1)
    #     # glBindBuffer(GL_ARRAY_BUFFER, vbo)
    #     # glBufferData(GL_ARRAY_BUFFER,)
    #
    #     @staticmethod
    #     def setup():
    #         pass
    #         # gluPerspective(*OGL.perspective)
    #         # glTranslatef(*OGL.translate)
    #         # glRotatef(*OGL.rotate)
    #         # glDisable(GL_DEPTH_TEST)
    #         # glEnable(GL_BLEND)
    #         # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #
    #     @staticmethod
    #     def blit(image, rect, shade=(1, 1, 1, 1)):
    #         Screen.win(image, (cal_len_w(rect[0]), cal_len_w(rect[1])))
    #
    #         return
    #         glEnable(GL_TEXTURE_2D)
    #         glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_rect().width, image.get_rect().height, 0, GL_RGBA,
    #                      GL_UNSIGNED_BYTE, pygame.image.tostring(image, "RGBA", 1))
    #
    #         # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    #         # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    #         glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    #         glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    #
    #         temp2 = (
    #             (0, 0),
    #             (1, 0),
    #             (1, 1),
    #             (0, 1),
    #         )
    #
    #         glBegin(GL_QUADS)
    #         glColor4fv(shade)
    #         for vertex in (0, 1, 2, 3):
    #             glTexCoord2f(*temp2[vertex])
    #             glVertex2fv((rect[vertex]))
    #         glEnd()
    #
    #         glDisable(GL_TEXTURE_2D)
    #
    #     @staticmethod
    #     def rect(color, rect, width=0):
    #         if isinstance(color[0], int):
    #             multicolor = False
    #         else:
    #             multicolor = True
    #
    #         if width:
    #             temp2 = (
    #                 (0, 1),
    #                 (0, 3),
    #                 (2, 1),
    #                 (2, 3),
    #             )
    #
    #             glBegin(GL_LINES)
    #             if not multicolor:
    #                 glColor4fv(color)
    #             for i in (0, 1, 2, 3):
    #                 if multicolor:
    #                     glColor4fv(color[i])
    #                 for j in temp2[i]:
    #                     glVertex2fv(rect[j])
    #         else:
    #             glBegin(GL_QUADS)
    #             if not multicolor:
    #                 glColor4fv(color)
    #             for i in (0, 1, 2, 3):
    #                 if multicolor:
    #                     glColor4fv(color[i])
    #                 glVertex2fv(rect[i])
    #         glEnd()
    #
    #     @staticmethod
    #     def circle(color, circle, precision=4):
    #         glBegin(GL_POLYGON)
    #         glColor4fv(color)
    #         for i in range(precision):
    #             deg = i * 2 * PI / precision
    #             glVertex2fv((circle[0] + circle[2] * math.sin(deg), circle[1] + circle[2] * math.cos(deg)))
    #         glEnd()
    #
    #     @staticmethod
    #     def move_camera(x, y):
    #         Screen.camera_pos = (Screen.camera_pos[0] + x, Screen.camera_pos[1] + y)
    #         for i in Manage.sticky_objects:
    #             i.translate(x, y)


# projectile function

def main():
    screen = Screen()

    # game setters
    if True:
        pygame.display.set_caption("bean mafia")
        screen.change_screen("menu")
        pygame.scrap.init()
        # OGL.setup()

    while screen.run:
        Game.current_time = time.time()
        Game.delta += (Game.current_time - Game.last_time) * Game.ticks_per_second
        Game.last_time = float(Game.current_time)

        while Game.delta >= 1:
            Game.dt = time.time() - Game.dt_last
            Game.dt_last = time.time()

            screen.mouse_pos = pygame.mouse.get_pos()
            screen.key_list()
            screen.scene.tick(screen)
            # globals()["tick_" + screen.screen](screen)
            for _i in Click.class_list + Process.class_list:
                if _i.enabled:
                    _i.script()

            screen.frame += 1
            Game.frame += 1
            Game.delta -= 1

            if screen.keysHeld["j"]:
                Draw.get_key("self_player").s_rot += PI/16

            if screen.keysHeld["h"]:
                Draw.get_key("self_player").d_rot += PI/16
            screen.camera_calculated = (screen.cal_len_w(screen.camera_pos[0]), screen.cal_len_h(screen.camera_pos[1]))

        if screen.run:
            screen.win.fill((0, 0, 0))

            for _i in filter(lambda _x: _x.z < 0, OrderedVisual.z_sorted_list):
                _i.draw()

            screen.scene.render(screen)
            # globals()["render_" + screen.screen](screen)

            for _i in filter(lambda _x: _x.z >= 0, OrderedVisual.z_sorted_list):
                _i.draw()

            if Click.show_borders:
                for _i in Click.class_list:
                    _i.draw()

            pygame.display.flip()

        if time.time() - Game.time_start > 1:
            Game.time_start += 1
            # print(Game.frame)
            Game.frame = 0


if __name__ == "__main__":
    main()
