import math


rx = 5.0
pixel_size = 4

ray_dir = PVector(0, 0, 1)
sphere_center = PVector(0, 0, 5)
sphere_r = 3.0

z_near = 2.0
z_far = 5.0

redraw = True
    
def setup():
    size(400, 400)
    noStroke()


def draw():
    global redraw
    if not redraw:
        return
    
    background(0)
    for x in range(0, width, pixel_size):
        for y in range(0, height, pixel_size):
            ray_origin = PVector(map(x+pixel_size/2, 0, width, -rx, rx), map(y+pixel_size/2, 0, height, -rx, rx), 0.0)            
            intersections = ray_sphere_intersection(ray_origin, ray_dir, sphere_center, sphere_r)
            if intersections:
                fill(map(intersections[0], z_near, z_far, 255, 0))
                rect(x, y, pixel_size, pixel_size)
    redraw = False


def ray_sphere_intersection(r_o, r_dir, s_center, s_r):
    L = s_center - r_o   # vector from ray origin to sphere center
    tca = L.dot(r_dir)
    if tca < 0:
        return False
    d2 = L.dot(L) - tca * tca;
    if d2 > s_r*s_r:
        return False
    thc = math.sqrt(s_r*s_r - d2)
    t0 = tca - thc
    t1 = tca + thc
    return t0, t1


def keyPressed():
    global rx, redraw, pixel_size
    if key == 'p':
        rx *= 1.05 
    if key == 'o':
        rx /= 1.05
        
    if key == 'k':
        if pixel_size > 1:
            pixel_size -= 1 
    if key == 'l':
        pixel_size += 1
        
    if key == '1':
        pixel_size = 1
    if key == '2':
        pixel_size = 2
    if key == '3':
        pixel_size = 4
    if key == '4':
        pixel_size = 8
    if key == '5':
        pixel_size = 16
    if key == '6':
        pixel_size = 32
        
    redraw = True
