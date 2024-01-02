import math
import random


BOID_LENGTH = 10
BOID_WIDTH = 6

BOID_SPEED = 1.5

boids = []

def setup():
    size(400, 300)
    fill(192)
    noStroke()
    smooth()
    
    init_boids(40)


def draw():
    background(0)
    for i in range(len(boids)):
        boids[i].update()
        boids[i].draw()


def init_boids(num=10):
    global boids
    for i in range(num):
        boid = Boid(x=random.randint(0, width),
                    y=random.randint(0, height),
                    alpha=random.uniform(0, 2.0*math.pi))
        boids.append(boid)    


class Boid:
    def __init__(self, x, y, alpha):
        self.x = x 
        self.y = y
        self.alpha = alpha
        
    def draw(self):
        pushMatrix()
        translate(self.x, self.y)
        rotate(self.alpha)
        triangle(-BOID_LENGTH, -BOID_WIDTH, BOID_LENGTH, 0, -BOID_LENGTH, BOID_WIDTH)
        popMatrix()
        
    def update(self):
        self.x += math.cos(self.alpha) * BOID_SPEED
        self.y += math.sin(self.alpha) * BOID_SPEED
        self.alpha += random.uniform(-0.2, 0.2)
        
        if self.x > width:
            self.x -= width
        if self.x < 0:
            self.x += width
        if self.y > height:
            self.y -= height
        if self.y < 0:
            self.y += height
        
    
