import math
import random


BOID_LENGTH = 12
BOID_WIDTH = 8

BOID_SPEED = 2.5

def setup():
    global x, y, alpha
    size(400, 300)
    
    fill(192)
    noStroke()
    smooth()
    
    x = width / 2
    y = height / 2
    alpha = 0.0

def draw():
    global x, y, alpha
    
    background(0)
    
    draw_boid(x, y, alpha)
    
    x += math.cos(alpha) * BOID_SPEED
    y += math.sin(alpha) * BOID_SPEED
    alpha += 0.2 * (random.random() - 0.5)
    
    if x > width:
        x -= width
    if x < 0:
        x += width
    if y > height:
        y -= height
    if y < 0:
        y += height


def draw_boid(x, y, alpha):
    pushMatrix()
    translate(x, y)
    rotate(alpha)
    triangle(-BOID_LENGTH, -BOID_WIDTH, BOID_LENGTH, 0, -BOID_LENGTH, BOID_WIDTH)
    popMatrix()    
    
