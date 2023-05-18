import time
from pygame.time import Clock


class Game:
    frame = 0
    clock = Clock()
    last_time = time.time()
    current_time = time.time()
    ticks_per_second = 30
    delta = 0
    time_start = time.time()
    dt = 0
    dt_last = time.time()
