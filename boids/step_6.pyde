import math
import random


BOID_LENGTH = 10
BOID_WIDTH = 6

EDGE_MARGIN = 80

boids = []
predators = []

max_velocity = 5
min_velocity = 2

max_velocity_predator = 4
min_velocity_predator = 2

range_visibility = 160.0
range_separation = 30.0
range_kill = 10

predator_visibility = 300.0

factor_separation = 0.05
factor_alignment = 0.05
factor_cohesion = 0.0002
factor_edge = 2.5
factor_predator = 0.02
factor_hunt = 0.025
factor_separation_predator = 0.01


def setup():
    size(800, 600)
    
    fill(192)
    noStroke()
    smooth()
    textSize(16)
    
    init_boids(100, 2)

    
def draw():
    background(0)
    fill(192)
    for i in range(len(boids)):
        boids[i].update(boids, predators)
        boids[i].draw()
        
    fill(255, 0, 0)
    for i in range(len(predators)):
        predators[i].update(boids, predators)
        predators[i].draw()
    
    fill(255)
    text('separation: {0:.5f}'.format(factor_separation), 10, 20)
    text('alignment: {0:.5f}'.format(factor_alignment), 10, 40)
    text('cohesion: {0:.5f}'.format(factor_cohesion), 10, 60)
    text('edge: {0:.5f}'.format(factor_edge), 10, 80)
    text('predator: {0:.5f}'.format(factor_predator), 10, 100)
    text('hunt: {0:.5f}'.format(factor_hunt), 10, 120)
    text('visiblity r: {0:.0f}'.format(range_visibility), 10, 160)
    text('separation r: {0:.0f}'.format(range_separation), 10, 180)
    

def init_boids(num=50, num_predators=3):
    global boids, predators
    for i in range(num):
        boid = Boid(ind=i,
                    x=random.randint(EDGE_MARGIN, width-EDGE_MARGIN),
                    y=random.randint(EDGE_MARGIN, height-EDGE_MARGIN),
                    alpha=random.uniform(0, 2.0*math.pi))
        boids.append(boid)
        
    for i in range(num_predators):
        predator = Predator(ind=i,
                            x=random.randint(EDGE_MARGIN, width-EDGE_MARGIN),
                            y=random.randint(EDGE_MARGIN, height-EDGE_MARGIN),
                            alpha=random.uniform(0, 2.0*math.pi))
        predators.append(predator)        

def mousePressed():
    global boids 
    boids.append(Boid(ind=len(boids),
                      x=mouseX,
                      y=mouseY,
                      alpha=random.uniform(0, 2.0*math.pi)))    
    
def keyPressed():
    global factor_separation, factor_alignment, factor_cohesion, factor_edge, factor_predator, factor_hunt, range_visibility, range_separation
    
    if key == 'q':
        factor_separation *= 1.1
    if key == 'a':
        factor_separation *= 0.9
        
    if key == 'w':
        factor_alignment *= 1.1
    if key == 's':
        factor_alignment *= 0.9
        
    if key == 'e':
        factor_cohesion *= 1.1
    if key == 'd':
        factor_cohesion *= 0.9
        
    if key == 'r':
        factor_edge *= 1.1
    if key == 'f':
        factor_edge *= 0.9
        
    if key == 't':
        factor_predator *= 1.1
    if key == 'g':
        factor_predator *= 0.9
        
    if key == 'y':
        factor_hunt *= 1.1
    if key == 'h':
        factor_hunt *= 0.9

    if key == 'u':
        range_visibility *= 1.1
    if key == 'j':
        range_visibility *= 0.9
        
    if key == 'i':
        range_separation *= 1.1
    if key == 'k':
        range_separation *= 0.9
        
        
        
        

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
        
    def update(self, boids, predators):
        v_sep = PVector(0, 0)
        v_align = PVector(0, 0)
        v_cohesion = PVector(0, 0)
        v_predator = PVector(0, 0)
        n_visible = 0
        
        for i in range(len(boids)):
            if boids[i].ind == self.ind:
                continue

            d = self.pos.dist(boids[i].pos)
            if d < range_separation:
                v_sep += self.pos - boids[i].pos
    
            if d < range_visibility:
                n_visible += 1    
                v_align += boids[i].vel
                v_cohesion += boids[i].pos
                
        for i in range(len(predators)):
            d = self.pos.dist(predators[i].pos)
                        
            if d < range_visibility:
                v_predator += self.pos - predators[i].pos
                    
        # Edges
        if self.pos.x < EDGE_MARGIN:
            self.vel.x += factor_edge
        if self.pos.x > width - EDGE_MARGIN:
            self.vel.x -= factor_edge
        if self.pos.y < EDGE_MARGIN:
            self.vel.y += factor_edge
        if self.pos.y > height - EDGE_MARGIN:
            self.vel.y -= factor_edge    
        
        
        self.vel += v_sep * factor_separation
        self.vel += v_predator * factor_predator
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
        
        
class Predator(Boid):
    
    def draw(self):
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        rotate(self.vel.heading())
        triangle(-BOID_LENGTH, -BOID_WIDTH, BOID_LENGTH, 0, -BOID_LENGTH, BOID_WIDTH)
        popMatrix()

    def update(self, boids, predators):
        v_hunt = PVector(0, 0)
        v_sep = PVector(0, 0)
        n_hunt = 0
        
        min_dist = float('inf')
        min_ind = None
        for i in range(len(boids)):
            d = self.pos.dist(boids[i].pos)     
            if d < range_visibility and d < min_dist:
                min_dist = d
                min_ind = i
        if min_ind is not None:
            if min_dist < range_kill:
                del(boids[min_ind])
            else:
                v_hunt = boids[min_ind].pos - self.pos            
        
                
        for i in range(len(predators)):
            if i == self.ind:
                continue

            d = self.pos.dist(predators[i].pos)
            if d < range_visibility:
                v_sep += self.pos - predators[i].pos
                
        if self.pos.x < EDGE_MARGIN:
            self.vel.x += factor_edge
        if self.pos.x > width - EDGE_MARGIN:
            self.vel.x -= factor_edge
        if self.pos.y < EDGE_MARGIN:
            self.vel.y += factor_edge
        if self.pos.y > height - EDGE_MARGIN:
            self.vel.y -= factor_edge    
        
        self.vel += v_sep * factor_separation_predator
        self.vel += v_hunt * factor_hunt

        s = 0.25
        self.vel += PVector(random.uniform(-s, s), random.uniform(-s, s))
        
        self.v_hunt = v_hunt 
        self.v_sep = v_sep
            
        # Cap min/max velocity
        if self.vel.mag() > max_velocity_predator:
            self.vel.setMag(max_velocity_predator)
        if self.vel.mag() < min_velocity_predator:
            self.vel.setMag(min_velocity_predator)
        
        self.pos += self.vel
