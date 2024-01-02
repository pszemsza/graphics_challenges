import math

BOID_LENGTH = 12
BOID_WIDTH = 8

def setup():
    size(800, 120)
    background(0) 
    fill(192)
    noStroke()
    smooth()


def draw():
    for i in range(20):
        draw_boid(20 + i*40, height/2, 2.0*math.pi*i/19)


def draw_boid(x, y, alpha):
    pushMatrix()
    translate(x, y)
    rotate(alpha)
    triangle(-BOID_LENGTH, -BOID_WIDTH, BOID_LENGTH, 0, -BOID_LENGTH, BOID_WIDTH)
    popMatrix()    
    
