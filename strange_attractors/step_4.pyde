import math
import random

C1_CONTINUITY = True

rx = 4.0

params_circle = []

animation = None

color_hsv_start = 100
color_hsv_diff = 40


def setup():
    global x, y, animation, colors
    noStroke()
    size(800, 800)
    colorMode(HSB, 360, 100, 100)
    animation = Animation(dims=6, rx=rx)


def draw():
    background(0)
    animation.draw_curve()        
    #animation.draw_points()
    animation.draw_current_point()
    animation.next_step()


class Animation:
    def  __init__(self, dims, rx, step=0.005):
        self.dims = dims
        self.step = step
        self.rx = rx
        self.t = 0.0
        
        self.pts = []
        for i in range(4):
            self.pts.append(self.get_random_point())
        
    def get_random_point(self):
        sc = 0.5
        return [random.uniform(-self.rx*sc, self.rx*sc) for _ in range(self.dims)]
        
    def draw_points(self):
        for i in range(0, self.dims, 2):
            old_px, old_py = None, None
            for ind in range(4):
                px = map(self.pts[ind][i], -self.rx, self.rx, 0, width)
                py = map(self.pts[ind][i+1], -self.rx, self.rx, 0, height)
                noStroke()
                fill((color_hsv_start + ind*color_hsv_diff) % 360, 100, 100)
                ellipse(px, py, 20, 20)
                
                if old_px is not None:
                    stroke(192)
                    line(px, py, old_px, old_py)
                old_px = px
                old_py = py
            
            
    def draw_curve(self, step=0.01):
        noStroke()          
        x = 0
        while x < 1.0:
            fill((color_hsv_start + x * 3 * color_hsv_diff) % 360, 100, 100)
            pt = self.get_point(x)
            for i in range(0, self.dims, 2):
                px = map(pt[i], -self.rx, self.rx, 0, width)
                py = map(pt[i+1], -self.rx, self.rx, 0, height)
                ellipse(px, py, 4, 4)
            x += step
            
    def draw_current_point(self):
        noStroke()           
        fill(0, 100, 100)
        pt = self.get_current_point()
        for i in range(0, self.dims, 2):
            px = map(pt[i], -self.rx, self.rx, 0, width)
            py = map(pt[i+1], -self.rx, self.rx, 0, height)
            ellipse(px, py, 12, 12)             
        
    def get_point(self, t):
        t3 = t*t*t
        t2 = 3.0*t*t*(1-t)
        t1 = 3.0*t*(1-t)*(1-t)
        t0 = (1-t)*(1-t)*(1-t)
        ret = [0.0] * self.dims
        for i in range(self.dims):
            ret[i] = self.pts[0][i] * t0 + self.pts[1][i] * t1 + self.pts[2][i] * t2 + self.pts[3][i] * t3
        return ret
    
    def get_current_point(self):
        return self.get_point(self.t)
    
    def next_step(self):
        def get_point_reflection(pt, center):
            return [2*center[i]-pt[i] for i in range(len(pt))]
    
        global color_hsv_start
        self.t += self.step
        if self.t > 1.0:
            self.t -= 1.0
            self.pts[0] = self.pts[3]
            if C1_CONTINUITY:
                self.pts[1] = get_point_reflection(self.pts[2], self.pts[3])
            else:
                self.pts[1] = self.get_random_point()
            self.pts[2] = self.get_random_point()
            self.pts[3] = self.get_random_point()
            color_hsv_start += (2 * color_hsv_diff % 360)
