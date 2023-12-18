import math
import random

STEPS_PER_FRAME = 100

rx = 3.5
ry = 3.5

params = [1.19, 1.1949999, 1.405, 1.365]

def setup():
    global x, y
    size(800, 800)
    x = random.random()
    y = random.random()

def draw():
    global x, y
    for _ in range(STEPS_PER_FRAME):
        nx = params[0] * math.sin(params[1]*y) + params[2] * math.cos(params[3]*x)
        ny = params[0] * math.sin(params[1]*x) + params[2] * math.cos(params[3]*y)
        
        x, y = nx, ny
        point(width / 2 * (1 + x / rx), height / 2 * (1 + y / ry))
