import math, random


PI = 3.14159265359


class ShootingStar:
    s_list = []

    def __init__(self, screen):
        self.screen = screen
        self.size = random.randint(3, 6) / 300
        self.speed = random.uniform(1, 6) / 300
        self.degree = random.uniform(-PI / 6, PI / 6)
        self.y = random.random()
        self.x = random.random() - 1 / 6
        self.frames = random.randint(30, 180)
        self.color = (random.uniform(0.8, 1), random.uniform(0.8, 1), random.uniform(0.8, 1), random.uniform(0.8, 1))
        self.frame = 0
        self.__class__.s_list.append(self)

    def draw(self):
        self.screen.circle(self.color, (self.x, self.y, self.size), camera=False)

    def script(self):
        self.x += self.speed * math.cos(self.degree)
        self.y += self.speed * math.sin(self.degree)
        self.frame += 1
        if self.frame >= self.frames:
            self.size -= 0.2 / 300
        if self.size <= 0 or not (self.x <= 1.01 and -0.01 <= self.y <= 1.01):
            self.__class__.s_list.remove(self)
