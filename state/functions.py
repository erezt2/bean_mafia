from pygame.image import load
from pygame.transform import scale, flip


PI = 3.14159265359


def fake_atan(x):
    c = 0
    return x / (1 + abs(x))


def open_texture(string, flip_x=False, flip_y=False, size=None):
    temp = load(string)
    if size is not None:
        temp = scale(temp, size)
    if flip_x or flip_y:
        temp = flip(temp, flip_x, flip_y)
    return temp


def both_ranges(x, y, z):
    return x <= y <= z or z <= y <= x


def error_range(x, y=0, err=0.005):
    return both_ranges(-err, x - y, err)