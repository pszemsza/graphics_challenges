import math
import random


BOID_LENGTH = 10
BOID_WIDTH = 6

EDGE_MARGIN = 120

boids = []
predators = []

max_velocity = 5
min_velocity = 2

max_velocity_predator = 4
min_velocity_predator = 2

range_visibility = 160.0
range_separation = 40.0
range_kill = 10

predator_visibility = 300.0

factor_separation = 0.8
factor_alignment = 0.05
factor_cohesion = 0.0002
factor_edge = 0.75
factor_predator = 1.2
factor_hunt = 0.025
factor_separation_predator = 0.3

draw_info = False


def setup():
    size(800, 600)
    
    fill(192)
    noStroke()
    smooth()
    textSize(16)
    
    init_boids(100, 3)

    
def draw():
    background(0)
    
    noStroke()
    fill(192)
    for i in range(len(boids)):
        boids[i].update(boids, predators)
        boids[i].draw()
        
    fill(255, 0, 0)
    for i in range(len(predators)):
        predators[i].update(boids, predators)
        predators[i].draw()
    
    
    if draw_info:
        stroke(192)
        noFill()
        rect(EDGE_MARGIN, EDGE_MARGIN, width-2*EDGE_MARGIN, height-2*EDGE_MARGIN)
        
        fill(255)
        text('separation: {0:.5f}'.format(factor_separation), 10, 20)
        text('alignment: {0:.5f}'.format(factor_alignment), 10, 40)
        text('cohesion: {0:.5f}'.format(factor_cohesion), 10, 60)
        text('edge: {0:.5f}'.format(factor_edge), 10, 80)
        text('predator: {0:.5f}'.format(factor_predator), 10, 100)
        text('hunt: {0:.5f}'.format(factor_hunt), 10, 120)
        text('separation (pr): {0:.5f}'.format(factor_separation_predator), 10, 140)
        text('visiblity r: {0:.0f}'.format(range_visibility), 10, 180)
        text('separation r: {0:.0f}'.format(range_separation), 10, 200)


def init_boids(num=50, num_predators=3):
    global boids, predators
    for i in range(num):
        boids.append(Boid(ind=i,
                          x=random.randint(EDGE_MARGIN, width-EDGE_MARGIN),
                          y=random.randint(EDGE_MARGIN, height-EDGE_MARGIN)))
        
    for i in range(num_predators): 
        predators.append(Predator(ind=i,
                                  x=random.randint(EDGE_MARGIN, width-EDGE_MARGIN),
                                  y=random.randint(EDGE_MARGIN, height-EDGE_MARGIN)))        


def mousePressed():
    global boids, predators
    if mouseButton == LEFT: 
        boids.append(Boid(len(boids), mouseX, mouseY))    
    else:
        predators.append(Predator(len(predators), mouseX, mouseY))
                       
    
def keyPressed():
    global draw_info, factor_separation, factor_alignment, factor_cohesion, factor_edge, factor_predator, factor_hunt, factor_separation_predator, range_visibility, range_separation
    sc = 1.05
    
    if key == 'z':
        draw_info = not draw_info
        
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
        factor_predator *= sc
    if key == 'g':
        factor_predator /= sc 
        
    if key == 'y':
        factor_hunt *= sc
    if key == 'h':
        factor_hunt /= sc 
        
    if key == 'u':
        factor_separation_predator *= sc
    if key == 'j':
        factor_separation_predator /= sc

    if key == 'i':
        range_visibility *= sc
    if key == 'k':
        range_visibility /= sc 
        
    if key == 'o':
        range_separation *= sc
    if key == 'l':
        range_separation /= sc 
        
        
        
        

class Boid:
    def __init__(self, ind, x, y):
        self.ind = ind
        self.pos = PVector(x, y) 
        self.vel = PVector(random.uniform(-1, 1), random.uniform(-1, 1))
        self.alpha = random.uniform(0, 2.0*math.pi)
        
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
                v = self.pos - boids[i].pos
                v_sep += v.normalize() * (1.0 - d / range_separation)
    
            if d < range_visibility:
                n_visible += 1    
                v_align += boids[i].vel
                v_cohesion += boids[i].pos
                
        for i in range(len(predators)):
            d = self.pos.dist(predators[i].pos)
            if d < range_visibility:
                v = self.pos - predators[i].pos
                v_predator += v.normalize() * (1.0 - d / range_visibility)
       
        # Edges
        if self.pos.x < EDGE_MARGIN:
            self.vel.x += (EDGE_MARGIN - self.pos.x) / EDGE_MARGIN * factor_edge
        if self.pos.x > width - EDGE_MARGIN:
            self.vel.x -= (EDGE_MARGIN - width + self.pos.x) / EDGE_MARGIN * factor_edge
        if self.pos.y < EDGE_MARGIN:
            self.vel.y += (EDGE_MARGIN - self.pos.y) / EDGE_MARGIN * factor_edge
        if self.pos.y > height - EDGE_MARGIN:
            self.vel.y -= (EDGE_MARGIN - height + self.pos.y) / EDGE_MARGIN * factor_edge
        
        
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
    def update(self, boids, predators):
        v_hunt = PVector(0, 0)
        v_sep = PVector(0, 0)
        
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
                v = self.pos - predators[i].pos
                v_sep += v.normalize() * (1.0 - d / range_visibility)
                
        # Edges
        if self.pos.x < EDGE_MARGIN:
            self.vel.x += (EDGE_MARGIN - self.pos.x) / EDGE_MARGIN * factor_edge
        if self.pos.x > width - EDGE_MARGIN:
            self.vel.x -= (EDGE_MARGIN - width + self.pos.x) / EDGE_MARGIN * factor_edge
        if self.pos.y < EDGE_MARGIN:
            self.vel.y += (EDGE_MARGIN - self.pos.y) / EDGE_MARGIN * factor_edge
        if self.pos.y > height - EDGE_MARGIN:
            self.vel.y -= (EDGE_MARGIN - height + self.pos.y) / EDGE_MARGIN * factor_edge
        
        self.vel += v_sep * factor_separation_predator
        self.vel += v_hunt * factor_hunt

        s = 0.25
        self.vel += PVector(random.uniform(-s, s), random.uniform(-s, s))
                    
        # Cap min/max velocity
        if self.vel.mag() > max_velocity_predator:
            self.vel.setMag(max_velocity_predator)
        if self.vel.mag() < min_velocity_predator:
            self.vel.setMag(min_velocity_predator)
        
        self.pos += self.vel
