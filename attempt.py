from math import cos, sin
from engine.objects import Rect
from engine.default import pos2, size2
import engine
import pygame
import random
import numpy
import os

def are_rects_colliding(rect1: engine.objects.Rectangular_obj, rect2: engine.objects.Rectangular_obj):
    pos1, size1 = rect1.get_projection()
    pos2, size2 = rect2.get_projection()
    x1 = pos1[0]
    x2 = pos2[0]
    y1 = pos1[1]
    y2 = pos2[1]
    x11 = x1+size1[0]
    x21 = x2+size2[0]
    y11 = y1+size1[1]
    y21 = y2+size2[1]

    if x1 <= x21 and x11 >= x2:
        if y1 <= y21 and y11 >= y2:
            return True
    return False


class Image(engine.objects.Rectangular_obj):
    def __init__(self, window: engine.Window, position, size, path) -> None:
        self.position = engine.default.pos2(position[0], position[1], numpy.int32)
        self.size = engine.default.size2(size[0], size[1], numpy.int32)
        self.path = path
        self.window = window
        self.first_calculation()

    def first_calculation(self):
        img = pygame.image.load(self.path)
        pos, size = self.get_projection()
        pos = pos.astype("int32")
        self.img = pygame.transform.scale(img, size.astype("int32"))

    def draw(self):
        pos, size = self.get_projection()
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.window._pygame_display.blit(self.img, self.rect)
        
        
class RandRect(Rect):
    def __init__(self, window: engine.Window) -> None:
        rand = random.randrange(0, 4)
        if rand == 0:
            posx = random.randint(-200, -100)
            posy = random.randint(0, 600)
            way_vec = numpy.array([1, 0])
        elif rand == 1:
            posx = random.randint(0, 1200)
            posy = random.randint(720, 800)
            way_vec = numpy.array([0, -1])
        elif rand == 2:
            posx = random.randint(1280, 1400)
            posy = random.randint(0, 600)
            way_vec = numpy.array([-1, 0])
        elif rand == 3:
            posx = random.randint(0, 1200)
            posy = random.randint(-200, -100)
            way_vec = numpy.array([0, 1])
        else:
            raise ZeroDivisionError

        self.way_vec = way_vec

        super().__init__(window, [posx, posy], [random.randint(10, 100), random.randint(10, 100)], color=[255, 0, 0])

    def draw(self):
        self.position.x += self.way_vec[0]*5
        self.position.y += self.way_vec[1]*5
        return super().draw()

def key_binds(win: engine.Window, player: Image):
    if win.is_holding(engine.constants.K_a): player.position.x -= 10
    if win.is_holding(engine.constants.K_d): player.position.x += 10
    if win.is_holding(engine.constants.K_w): player.position.y -= 10
    if win.is_holding(engine.constants.K_s): player.position.y += 10

win = engine.Window([1280, 720], "Attempt", 60)
win.camera.position = pos2(1280/2, 720/2)
# win.camera.size = size2(2, 2)
img = Image(win, [0, 0], [110, 185], "ba.png")
# img = engine.objects.Rect(win, [100, 100], [110, 185])
objlist = []
t = 0

stop = 100

while 1:
    win.camera.position.x += sin(t/10)*min(t/60/60, 1)
    win.camera.position.y += cos(t/10)*min(t/60/60, 1)
    key_binds(win, img)
    if t % (max(60-t//60, (101-stop)/5*3)) == 0:
        objlist.append(RandRect(win))
    t += 1
    os.system("cls") if os.name == "nt" else os.system("clear")
    print(f"Object count: {len(objlist)}")
    win.set_caption(f"Score: {t}")
    win.display.fill([min(t/60/60, 1)*255/2, 0, 0])
    img.draw()
    for obj in objlist:
        if are_rects_colliding(img, obj):
            while not win.is_just_tapped(engine.constants.K_r): win.update()
            t = 0
            objlist = []
        if obj.position.x > 1500 or obj.position.x < -500 or obj.position.y > 1000 or obj.position.y < -500: objlist.remove(obj)
        obj.draw()
    win.update()
