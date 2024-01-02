import math
import random


BOID_LENGTH = 10
BOID_WIDTH = 6

EDGE_MARGIN = 80

boids = []

max_velocity = 5
min_velocity = 2

range_visibility = 160.0
range_separation = 20.0

factor_separation = 0.05
factor_alignment = 0.05
factor_cohesion = 0.0002
factor_edge = 0.45


def setup():
    size(800, 600)
    noStroke()
    smooth()
    textSize(16)
    
    init_boids(100)

    
def draw():
    background(0)
    fill(192)
    for i in range(len(boids)):
        boids[i].update(boids)
        boids[i].draw()
        
    fill(255)
    text('separation: {0:.5f}'.format(factor_separation), 10, 20)
    text('alignment: {0:.5f}'.format(factor_alignment), 10, 40)
    text('cohesion: {0:.5f}'.format(factor_cohesion), 10, 60)
    text('edge: {0:.5f}'.format(factor_edge), 10, 80)
    text('visiblity r: {0:.0f}'.format(range_visibility), 10, 120)
    text('separation r: {0:.0f}'.format(range_separation), 10, 140)
    #saveFrame('movie_####.png')


def init_boids(num=10):
    global boids
    for i in range(num):
        boid = Boid(ind=i,
                    x=random.randint(EDGE_MARGIN, width-EDGE_MARGIN),
                    y=random.randint(EDGE_MARGIN, height-EDGE_MARGIN),
                    alpha=random.uniform(0, 2.0*math.pi))
        boids.append(boid)    

def mousePressed():
    global boids 
    boids.append(Boid(ind=len(boids),
                      x=mouseX,
                      y=mouseY,
                      alpha=random.uniform(0, 2.0*math.pi)))    
    
def keyPressed():
    global factor_separation, factor_alignment, factor_cohesion, factor_edge, range_visibility, range_separation
    
    sc = 1.05
    if key == 'q':
        factor_separation *= sc
    if key == 'a':
        factor_separation /= sc
        
    if key == 'w':
        factor_alignment *= sc
    if key == 's':
        factor_alignment /= sc
        
    if key == 'e':
        factor_cohesion *= sc
    if key == 'd':
        factor_cohesion /= sc
        
    if key == 'r':
        factor_edge *= sc
    if key == 'f':
        factor_edge /= sc
        
    if key == 't':
        range_visibility *= sc
    if key == 'g':
        range_visibility /= sc 
        
    if key == 'y':
        range_separation *= sc
    if key == 'h':
        range_separation /= sc 
        
        
class Boid:
    def __init__(self, ind, x, y, alpha):
        self.ind = ind
        self.pos = PVector(x, y) 
        self.vel = PVector(random.uniform(-1, 1), random.uniform(-1, 1))
        self.alpha = alpha
        
    def draw(self):
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        rotate(self.vel.heading())
        triangle(-BOID_LENGTH, -BOID_WIDTH, BOID_LENGTH, 0, -BOID_LENGTH, BOID_WIDTH)
        popMatrix()
        
    def update(self, boids):
        v_sep = PVector(0, 0)
        v_align = PVector(0, 0)
        v_cohesion = PVector(0, 0)
        n_visible = 0
        
        for i in range(len(boids)):
            if i == self.ind:
                continue

            d = self.pos.dist(boids[i].pos)
                        
            if d < range_separation:
                v_sep += self.pos - boids[i].pos
    
            if d < range_visibility:
                n_visible += 1    
                v_align += boids[i].vel
                v_cohesion += boids[i].pos
                
        if self.pos.x < EDGE_MARGIN:
            self.vel.x += factor_edge
        if self.pos.x > width - EDGE_MARGIN:
            self.vel.x -= factor_edge
        if self.pos.y < EDGE_MARGIN:
            self.vel.y += factor_edge
        if self.pos.y > height - EDGE_MARGIN:
            self.vel.y -= factor_edge    
        
        
        self.vel += v_sep * factor_separation
        if n_visible > 0:
            average_vel = v_align / n_visible
            self.vel += (average_vel - self.vel) * factor_alignment
            
            mass_center = v_cohesion / n_visible
            self.vel += (mass_center - self.pos) * factor_cohesion
            
        s = 0.25
        self.vel += PVector(random.uniform(-s, s), random.uniform(-s, s))
            
        # Cap min/max velocity
        if self.vel.mag() > max_velocity:
            self.vel.setMag(max_velocity)
        if self.vel.mag() < min_velocity:
            self.vel.setMag(min_velocity)
        
        self.pos += self.vel
        
