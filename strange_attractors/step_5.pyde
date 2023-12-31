import math
import random

MOVIE_PREFIX = 'movie'
 
ITERATIONS_PER_FRAME = 12000     # number of iterations in each draw()
FRAMES_PER_ANIMATION_STEP = 50   # how many times draw() is executed per single animations frame
ANIMATION_STEP = 0.05            # how much t changes for every animation frame 

# how many parameters there are
DIMS = 8

ALPHA = 30

C1_CONTINUITY = True

# Fixed points. They will be used as the first and last control points. Intermediate points will be randomized.
POINTS = [      
  [-2.3, 1.1375, -0.21, -0.2625, -1.05, 2.17, 1.4, -0.8],
  [-2.0825, 1.12, -0.455, -0.3325, -1.3825, 2.2575, 1.4525, -0.525],
  [-1.54, 1.1375, -0.7175, -0.4375, -1.0675, 2.3625, 1.4525, -1.0325],
  [-1.26, 1.155, -1.0675, -0.4725, -0.5775, 2.345, 1.4, -1.4],
  [-0.91, 1.2075, -1.68, -0.735, 0.0, 2.3275, 1.365, -1.855],
  [-0.7175, 1.47, -2.065, -0.945, 0.3325, 2.5375, 1.155, -2.2925],
  [-0.315, 1.785, -2.31, -1.085, 0.8225, 2.73, 1.365, -2.5025],
  [-0.0875, 1.75, -2.6075, -1.1375, 1.1025, 2.73, 1.2425, -2.8],
  [-0.07, 1.68, -2.7825, -0.7525, 1.33, 2.1525, 0.875, -2.8175],
  [0.21, 1.47, -3.08, -0.6125, 1.68, 1.8725, 1.015, -2.975],
  [0.5075, 1.715, -2.8175, -0.455, 2.0475, 1.3475, 1.855, -3.2725],
  [1.1725, 1.8375, -2.9925, 0.6125, 1.4875, 2.415, 2.2225, -2.7125],
]


rx = 5.0

animation_step_frames = 0
movie_frame = 0

# color gradient for control points
color_hsv_start = 100
color_hsv_diff = 40

animation = None

# hue of the solid color (color mode 2) or the gradient start (color mode 3)
STARTING_HUE = 10

# 0 - black on white
# 1 - white on black
# 2 - solid color
# 3 - colorful
COLOR_MODE = 3

def setup():
    global x, y, animation, params
    size(800, 800)
    clear_background()
    
    animation = Animation(dims=DIMS, rx=rx, step=ANIMATION_STEP)
    animation.set_fixed_points(POINTS)
    
    params = animation.get_current_point()


def draw():
    global x, y, animation_step_frames, params, movie_frame, current_point
    colorMode(HSB, 360, 100, 100)
    for _ in range(100):
        # randomize seed every 100 iterations to avoid cycles
        x = random.random()
        y = random.random()
        for _ in range(ITERATIONS_PER_FRAME // 100):
            nx = params[0] * math.sin(params[1]*y) + params[2] * math.cos(params[3]*x)
            ny = params[4] * math.sin(params[5]*x) - params[6] * math.cos(params[7]*y)
            
            if COLOR_MODE == 0:
                stroke(color(0, 100, 0), ALPHA)
            elif COLOR_MODE == 1:
                stroke(color(0, 0, 100), ALPHA)
            elif COLOR_MODE == 2:
                stroke(color(STARTING_HUE, 100, 100), ALPHA)
            elif COLOR_MODE == 3:
                color_hue = map(dist(x, y, nx, ny), 0.0, 10.0, 0, 200)
                stroke(color((STARTING_HUE+color_hue)%360, 100, 100), ALPHA)
          
            x, y = nx, ny
            point(map(x, -rx, rx, 0, width), map(y, -rx, rx, 0, height))
        

    colorMode(HSB, 360, 100, 100)
    #animation.draw_points()
    #animation.draw_curve()
    #animation.draw_current_point()
    
    animation_step_frames += 1
    if animation_step_frames >= FRAMES_PER_ANIMATION_STEP:
        saveFrame("{0}_{1:05d}.png".format(MOVIE_PREFIX, movie_frame))
        movie_frame += 1
        
        colorMode(RGB, 255, 255, 255)
        clear_background()
        
        animation.next_step()
        params = animation.get_current_point()
        animation_step_frames = 0


def clear_background():
    background(255 if COLOR_MODE == 0 else 0)


def keyPressed():       
    if key == 'p':
        print(params)
                    

class Animation:
    def  __init__(self, dims, rx, step=0.005):
        self.dims = dims
        self.rx = rx
        self.ry = rx
        self.t = 0.0
        self.step = step
        self.pts = []
        self.fixed_pts = None
        for i in range(4):
            self.pts.append(self.get_random_point())
            
    def set_fixed_points(self, pts):
        self.fixed_pts = pts
        self.pts[0] = self.fixed_pts[0]
        self.pts[3] = self.fixed_pts[1]
        self.pts[1] = self.get_random_point_near_ends()
        self.pts[2] = self.get_random_point_near_ends()
        self.current_fixed_point = 1
        
    def get_random_point(self):
        r = 3.0
        return [random.uniform(-r, r) for _ in range(self.dims)]
    
    def get_random_point_near_point(self, pt):
        return [pt[i] + random.uniform(-0.5, 0.5) for i in range(self.dims)]
    
    def get_random_point_near_ends(self):
        center = [(self.pts[3][i]+self.pts[0][i]) / 2.0 for i in range(self.dims)]
        v = [self.pts[3][i] - self.pts[0][i] for i in range(self.dims)]
        return [center[i] + 0.5 * random.uniform(-v[i], v[i]) for i in range(self.dims)]
        
    def draw_points(self):
        for i in range(0, self.dims, 2):
            old_px, old_py = None, None
            for ind in range(4):
                px = map(self.pts[ind][i], -self.rx, self.rx, 0, width)
                py = map(self.pts[ind][i+1], -self.rx, self.rx, 0, height)
                noStroke()
                fill((color_hsv_start + ind*color_hsv_diff) % 360, 100, 100)
                ellipse(px, py, 2, 2)
                
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
                ellipse(px, py, 1, 1)
            x += step
            
    def draw_current_point(self):
        noStroke()           
        fill(0, 100, 100)
        pt = self.get_current_point()
        for i in range(0, self.dims, 2):
            px = map(pt[i], -self.rx, self.rx, 0, width)
            py = map(pt[i+1], -self.rx, self.rx, 0, height)
            ellipse(px, py, 6, 6)             
    
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
            self.current_fixed_point += 1

            self.pts[0] = self.pts[3]
            
            randomize_endpoint = self.fixed_pts is None or self.current_fixed_point >= len(self.fixed_pts)
            if randomize_endpoint:
                if C1_CONTINUITY:
                    self.pts[1] = get_point_reflection(self.pts[2], self.pts[3])
                else:
                    self.pts[1] = self.get_random_point_near_point(self.pts[0])
                self.pts[2] = self.get_random_point_near_point(self.pts[1])
                self.pts[3] = self.get_random_point_near_point(self.pts[2])
            else:
                if C1_CONTINUITY:
                    self.pts[1] = get_point_reflection(self.pts[2], self.pts[3])
                else:
                    self.pts[1] = self.fixed_pts[self.current_fixed_point]
                    
                self.pts[3] = self.fixed_pts[self.current_fixed_point]
                self.pts[2] = self.get_random_point_near_ends()
                
            color_hsv_start += (2 * color_hsv_diff % 360)
