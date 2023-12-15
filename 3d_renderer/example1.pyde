import math

def setup():
    size(800, 600)
    background(0)
    stroke(255)
    strokeWeight(1)
        
    cx = width / 2
    cy = height / 2
    
    r = 25
    R = 240
    
    d_alpha = 2*math.pi / 36
    alpha = 0
    while alpha < 2 * math.pi:
        sx = cx + math.sin(alpha) * r
        sy = cy + math.cos(alpha) * r
        ex = cx + math.sin(alpha) * R
        ey = cy + math.cos(alpha) * R        
        mline(sx, sy, ex, ey)
        alpha += d_alpha

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
    
