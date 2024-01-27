import json
import math

rx = 5.0
pixel_size = 4

ray_dir = PVector(0, 0, 1)

scene = {}

redraw = True


def setup():
    global scene
    colorMode(RGB, 1, 1, 1)
    size(400, 400)
    noStroke()    
    scene = load_scene('scene_step4.json')


def draw():
    global redraw
    if not redraw:
        return
    
    background(0)
    for x in range(0, width, pixel_size):
        for y in range(0, height, pixel_size):
            ray_origin = PVector(map(x+pixel_size/2, 0, width, -rx, rx), map(y+pixel_size/2, 0, height, -rx, rx), -8.0)
            min_dist = float('inf')
            closest_obj = None
            
            for obj in scene['objects']:
                #pos = PVector(obj['x'], obj['y'], obj['z'])
                if obj['type'] != 'sphere':
                    continue

                intersections = ray_sphere_intersection(ray_origin, ray_dir, obj['pos'], obj['r'])
                if intersections:
                    if intersections[0] < min_dist:
                        min_dist = intersections[0]
                        closest_obj = obj
                        
            if closest_obj is not None:
                intersection_pt = ray_origin + ray_dir * min_dist
                pt_normal = (intersection_pt - closest_obj['pos']).normalize() 
                fill(calculate_lighting(scene, closest_obj, intersection_pt, pt_normal, ray_origin))
                rect(x, y, pixel_size, pixel_size)
    redraw = False


def get_color_from_string(s):
    arr = [float(trim(v))/255.0 for v in s.split(',')]
    return PVector(arr[0], arr[1], arr[2])


def load_scene(path):
    lines = loadStrings(path)
    scene = json.loads(' '.join(lines))
    if 'objects' in scene:
        for i, obj in enumerate(scene['objects']):
            obj['ind'] = i
            obj['pos'] = PVector(obj['x'], obj['y'], obj['z'])
            obj['color_vector'] = get_color_from_string(obj['color'])
    if 'lights' in scene:
        for obj in scene['lights']:
            obj['color_vector'] = get_color_from_string(obj['color'])
            
            if obj['type'] == 'directional':
                obj['dir'] = PVector(obj['x'], obj['y'], obj['z']).normalize()
                
            if obj['type'] == 'point':
                obj['pos'] = PVector(obj['x'], obj['y'], obj['z'])
    return scene


def reflection(v_light, v_normal):
    return 2.0 * v_light.dot(v_normal) * v_normal - v_light


def calculate_lighting(scene, obj, pt, pt_normal, ray_origin):    
    col = PVector(0, 0, 0)
    for o in scene['lights']:
        if o['type'] == 'ambient':
            col += mult_vectors(o['color_vector'], obj['color_vector'])
            #print(o['color_vector'], obj['color_vector'], col)
            
        if o['type'] == 'directional':
            v_light = o['dir'] * -1.0
        elif o['type'] == 'point':
            v_light = o['pos'] - pt
        else:
            # unknown light type
            continue
        
        v_light = v_light.normalize()
        diffuse_intensity = pt_normal.dot(v_light)
        if diffuse_intensity > 0.0:
            col += mult_vectors(o['color_vector'], obj['color_vector']) * diffuse_intensity
        
        v_viewer = (ray_origin-pt).normalize()
        v_reflected = reflection(v_light, pt_normal)
        specular_intensity = v_viewer.dot(v_reflected)
        if specular_intensity > 0.0:
            col += o['color_vector'] * math.pow(max(0.0, specular_intensity), 137)

    for i in range(3):
        col[i] = constrain(col[i], 0.0, 1.0)
    return color(col[0], col[1], col[2]) 


# component-wise multiplication
def mult_vectors(v1, v2):
    return PVector(v1.x*v2.x, v1.y*v2.y, v1.z*v2.z)
    

def mousePressed():
    saveFrame('screenshot_####.png')


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
