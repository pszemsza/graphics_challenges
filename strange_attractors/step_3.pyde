import math
import random


STEPS_PER_FRAME = 2000
PARAM_CIRCLE_COLOR = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0]]
PARAM_CIRCLE_RADIUS = 10 
ALPHA = 30

rx = 4.0

params = [-2.3, 1.1375, 0.805, -0.98, -1.05, 2.17, 1.4, -0.8]


params_circle = []

drag_ind = None
show_param_circles = True

starting_hue = 0

# 0 - black on white
# 1 - white on black
# 2 - solid color
# 3 - colorful
color_mode = 0

def setup():
    global x, y, params_circle
    ellipseMode(RADIUS)
    size(800, 800)
    
    reset_animation()
    
    for i in range(4):
        pc = ParamCircle(i, PARAM_CIRCLE_COLOR[i])
        pc.set_pos_from_params(params, rx)
        params_circle.append(pc)


def draw():
    global x, y
    colorMode(HSB, 360, 100, 100)
    
    for _ in range(STEPS_PER_FRAME):
        nx = params[0] * math.sin(params[1]*y) + params[2] * math.cos(params[3]*x)
        ny = params[4] * math.sin(params[5]*x) - params[6] * math.cos(params[7]*y)
        
        if color_mode == 0:
            stroke(color(0, 100, 0), ALPHA)
        elif color_mode == 1:
            stroke(color(0, 0, 100), ALPHA)
        elif color_mode == 2:
            stroke(color(starting_hue, 100, 100), ALPHA)
        elif color_mode == 3:
            color_hue = map(dist(x, y, nx, ny), 0.0, 10.0, 0, 200)
            stroke(color((starting_hue+color_hue)%360, 100, 100), ALPHA)
            
        x, y = nx, ny
        point(map(x, -rx, rx, 0, width), map(y, -rx, rx, 0, height))
        
    if show_param_circles:
        colorMode(RGB, 255)
        for pc in params_circle:
            pc.draw()


def mousePressed():
    global drag_ind
    min_dist = float('inf')
    for i, pc in enumerate(params_circle):
        curr_dist = dist(pc.x, pc.y, mouseX, mouseY)
        if curr_dist < min_dist and curr_dist <= PARAM_CIRCLE_RADIUS:
            drag_ind = i
            min_dist = curr_dist


def reset_animation():
    global x, y
    x = random.random()
    y = random.random()
    background(255 if color_mode == 0 else 0)


def mouseReleased():
    global drag_ind
    drag_ind = None


def mouseDragged():
    if drag_ind is not None:
        params_circle[drag_ind].x = mouseX
        params_circle[drag_ind].y = mouseY
        params_circle[drag_ind].set_param_from_pos(params, rx)
        reset_animation()


def keyPressed():
    global x, y, show_param_circles, params, color_mode, starting_hue

    # change color mode 
    if key == 'c':
        color_mode = (color_mode + 1) % 4
        reset_animation()

    # randomize the hue (only used in solid and gradient color modes)
    if key == 'h':
        starting_hue = random.randint(0, 360)
        reset_animation()

    if key == 'r':
        x = random.random()
        y = random.random()

    # print params
    if key == 'p':
        print([round(p, 4) for p in params])
        
    if key == 's':
        show_param_circles = not show_param_circles
        reset_animation()

    # randomize params
    if key == 'q':
        params = [(random.random() - 0.5) * 3.0 for _ in range(len(params))]
        for pc in params_circle:
            pc.set_pos_from_params(params, rx)
        reset_animation()

    # change params by small random values
    if key == 'w':
        params = [p + (random.random() - 0.5) * 0.4 for p in params]
        for pc in params_circle:
            pc.set_pos_from_params(params, rx)
        reset_animation()


class ParamCircle:
    def __init__(self, ind, color, size=PARAM_CIRCLE_RADIUS):
        self.ind = ind
        self.color = color
        self.size = size
        self.x = 0
        self.y = 0
    
    def draw(self):
        noFill()
        stroke(self.color[0], self.color[1], self.color[2])
        ellipse(self.x, self.y, self.size, self.size)
        
    def set_pos_from_params(self, params, param_range):
        self.x = map(params[2*self.ind], -param_range, param_range, 0, width)
        self.y = map(params[2*self.ind+1], -param_range, param_range, 0, height)
        
    def set_param_from_pos(self, params, param_range):
        params[2*self.ind] = map(self.x, 0, width, -param_range, param_range)
        params[2*self.ind+1] = map(self.y, 0, height, -param_range, param_range)
