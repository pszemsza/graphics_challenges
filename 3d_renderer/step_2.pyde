import math
    
objects = []
 
def setup():
    background(0)
    size(800, 600)
    stroke(255)
    strokeWeight(1)
    objects.append(Object.cube(400, 300, 120, 300))


def draw():
    background(0)
    for o in objects:
        draw_object(o)


def draw_object(o):
    # Here we project the 3D points to 2D
    pts_2d = [None] * len(o.vertices)
    for i, v in enumerate(o.vertices):
        pts_2d[i] = v[0], v[1]           
        
    for face in o.indices:
        draw_triangle(pts_2d[face[0]], pts_2d[face[1]], pts_2d[face[2]])
        
            
def draw_triangle(p1, p2, p3):
    mline(p1[0], p1[1], p2[0], p2[1])
    mline(p2[0], p2[1], p3[0], p3[1])
    mline(p3[0], p3[1], p1[0], p1[1])
        

def mline(x1, y1, x2, y2):
    x1 = int(round(x1))
    x2 = int(round(x2))
    y1 = int(round(y1))
    y2 = int(round(y2))
    
    # To simplify things, we want x1 to always be smaller (or equal) to x2
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1

    # Vertical line case    
    if x1 == x2:
        if y2 > y1:
            for y in range(y1, y2+1): point(x1, y)
        else:
            for y in range(y2, y1+1): point(x1, y)
        return
    
    # Line slope
    dy = 1.0 * (y2 - y1) / (x2 - x1)
    
    if abs(dy) <= 1.0:
        # If the absolute value of a slope is at most 1 we need to draw exactly one pixel for each x coordinate. 
        y = y1
        for x in range(x1, x2+1):
            point(x, round(y))
            y += dy
    else:
        # For a larger slope switch X and Y coordinates, and draw a line along the Y coordinate. 
        dx = 1.0 * (x2 - x1) / abs(y2 - y1)
        x = x1
        step = int(math.copysign(1, y2-y1))
        for y in range(y1, y2+step, step):
            point(round(x), y)
            x += dx
            

class Object:
    def __init__(self):
        self.vertices = []
        self.indices = []

    @staticmethod
    def cuboid(cx, cy, cz, sx, sy, sz):
        ret = Object()
        ret.vertices = [
            [cx - sx/2, cy - sy/2, cz - sz / 2, 1.0],
            [cx + sx/2, cy - sy/2, cz - sz / 2, 1.0],
            [cx - sx/2, cy + sy/2, cz - sz / 2, 1.0],
            [cx + sx/2, cy + sy/2, cz - sz / 2, 1.0],
            
            [cx - sx/2, cy - sy/2, cz + sz / 2, 1.0],
            [cx + sx/2, cy - sy/2, cz + sz / 2, 1.0],
            [cx - sx/2, cy + sy/2, cz + sz / 2, 1.0],
            [cx + sx/2, cy + sy/2, cz + sz / 2, 1.0],
        ]
        ret.indices = [
            [0, 1, 2], [1, 2, 3], [0, 1, 4], [1, 4, 5],
            [0, 2, 4], [2, 4, 6], [2, 3, 6], [3, 6, 7],
            [1, 3, 5], [3, 5, 7], [4, 5, 6], [5, 6, 7],                       
        ]
        return ret
    
    @staticmethod
    def cube(cx, cy, cz, s):
        return Object.cuboid(cx, cy, cz, s, s, s) 
    
