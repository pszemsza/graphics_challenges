import json
import math
import intervals


rx = 3
pixel_size = 4

ray_dist = 30

x_axis = PVector(1, 0, 0)
y_axis = PVector(0, 1, 0)
z_axis = PVector(0, 0, 1)

scene = {}
cube_intersection_normal = {}

redraw = True


totrot = 1.4

def setup():
    global scene, DIRECTIONAL_LIGHT_DIR
    
    colorMode(RGB, 1, 1, 1)
    size(400, 400)
    noStroke()
    scene = load_scene('scene_step8.json')
    rotate_ray(scene, 0.-4, 0.3, 0.1)

def draw():
    global redraw
    if not redraw:
        return
    
    background(0)
          
    for x in range(0, width, pixel_size):
        for y in range(0, height, pixel_size):
            
            ray_origin = -1.0 * z_axis * ray_dist + x_axis * map(x, 0, width, -rx, rx) + y_axis * map(y, 0, height, -rx, rx) 
            obj, d = raycast_scene(scene, ray_origin, z_axis)
            
            if obj is None:
                continue
    
            hit_pt = ray_origin + z_axis * d
            
            if obj['type'] == 'sphere':
                pt_normal = (hit_pt - obj['pos']).normalize()
            else:
                pt_normal = cube_intersection_normal[obj['ind']]
                
            fill(calculate_lighting(scene, obj, hit_pt, pt_normal, ray_origin))
            rect(x, y, pixel_size, pixel_size)

    redraw = False

    
# component-wise multiplication
def mult_vectors(v1, v2):
    return PVector(v1.x*v2.x, v1.y*v2.y, v1.z*v2.z)


def is_zero(val, tol=1e-6):
    return val > -tol and val < tol 


def reflection(v_light, v_normal):
    return 2.0 * v_light.dot(v_normal) * v_normal - v_light


def calculate_lighting(scene, obj, pt, pt_normal, ray_origin):
    cos_angle = z_axis.dot(pt_normal)
    if cos_angle > 0:
        pt_normal *= -1.0

    col = PVector(0, 0, 0)
    for o in scene['lights']:
        if o['type'] == 'ambient':
            col += mult_vectors(o['color_vector'], obj['color_vector'])

        if o['type'] == 'directional':
            v_light = o['dir']
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
                obj['dir'] = PVector(-obj['x'], -obj['y'], -obj['z']).normalize()
                
            if obj['type'] == 'point':
                obj['pos'] = PVector(obj['x'], obj['y'], obj['z'])
                
    if 'tree_compressed' in scene: 
        scene['tree'], _ = process(scene['tree_compressed'].split(), 0)             
    return scene 

OP_TO_NAME = {
              '-': 'subtract',
              '+': 'union',
              '*': 'intersect',
              }

def process(a, ind):
    if a[ind].isnumeric():
        return int(a[ind]), ind+1
    else:
        node = {}
        node['op'] = OP_TO_NAME[a[ind]]
        node['left'], ind = process(a, ind+1)
        node['right'], ind = process(a, ind)
    return node, ind
     

def process_node(el, intersections):
    if isinstance(el, int):
        return intersections[el]
        
    if 'op' in el:
        left = process_node(el['left'], intersections)
        right = process_node(el['right'], intersections)
        if el['op'] == 'union':
            return left.union(right)
        if el['op'] == 'intersect':
            return left.intersect(right)
        if el['op'] == 'subtract':
            return left.subtract(right)
        print('unknown operation: {0}'.format(el['op']))
    
        
# return obj hit and hit distance
def raycast_scene(scene, ray_origin, ray_dir, verbose=False):
    intersections = {}
    if verbose:
        print(ray_origin, ray_dir)
    for i, obj in enumerate(scene['objects']):
        if obj['type'] == 'sphere':
            iv = ray_sphere_intersection(ray_origin, ray_dir, obj['pos'], obj['r'], i)
            if verbose: print(obj['pos'], obj['r'], 'intersection:', str(iv))
            
        elif obj['type'] == 'cube':
            iv = ray_cube_intersection(ray_origin, ray_dir, obj['pos'], obj['size'], i)
            
        intersections[i] = intervals.IntervalSet(iv)
        

    if verbose:
        print('intersections: ', intersections)
    ray_intersections = process_node(scene['tree'], intersections)
    if verbose:
        print('ray intersections: ', ray_intersections)

    if len(ray_intersections.ivs) == 0:
        return None, 0
    
    ray_intersections.sort()
    obj = scene['objects'][ray_intersections.ivs[0].ia]
    return obj, ray_intersections.ivs[0].a
    

    
def mousePressed():
    # for debugging: display intersections for the clicked pixel   
    ray_origin = -1.0 * z_axis * ray_dist + x_axis * map(mouseX, 0, width, -rx, rx) + y_axis * map(mouseY, 0, height, -rx, rx)
    raycast_scene(scene, ray_origin, z_axis, verbose=True)
    
def keyPressed():
    global rx, redraw, pixel_size
    if key == 'k':
        rx *= 1.05 
    if key == 'l':
        rx /= 1.05
        
    if key == 'o':
        if pixel_size > 1:
            pixel_size -= 1 
    if key == 'p':
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
        
    rotation_angle = 0.02
    if key == 'w':
        rotate_ray(scene, -rotation_angle, 0, 0)
    if key == 's':
        rotate_ray(scene, rotation_angle, 0, 0)
    if key == 'a':
        rotate_ray(scene, 0, rotation_angle, 0)
    if key == 'd':
        rotate_ray(scene, 0, -rotation_angle, 0)
    if key == 'q':
        rotate_ray(scene, 0, 0, rotation_angle)
    if key == 'e':
        rotate_ray(scene, 0, 0, rotation_angle)    
    redraw = True


def rotate_ray(scene, ax, ay, az):
    global x_axis, y_axis, z_axis
    m = Matrix.rotation(ax, ay, az)
    x_axis = m.mul_vector(x_axis)
    y_axis = m.mul_vector(y_axis)
    z_axis = m.mul_vector(z_axis)
    
    for obj in scene['lights']:        
        if obj['type'] == 'directional':
            obj['dir'] = m.mul_vector(obj['dir'])
                
        if obj['type'] == 'point':
            obj['pos'] = m.mul_vector(obj['pos'])



def ray_sphere_intersection(r_origin, r_dir, s_center, s_r, ind):
    L = s_center - r_origin
    tc = L.dot(r_dir)
    if tc < 0:
        return None
    d2 = L.dot(L) - tc * tc;
    s_r2 = s_r * s_r
    if d2 > s_r2:
        return None
    th = math.sqrt(s_r2 - d2)
    return intervals.Interval(tc - th, tc + th, ia=ind, ib=ind)


def ray_cube_intersection(r_origin, r_dir, c_center, c_size, ind):
    global cube_intersection_normal
    t_min = float('-inf')
    t_max = float('inf')
    for d in range(3):
        if is_zero(r_dir[d]):
            inv = float('inf')
        else:
            inv = 1.0 / r_dir[d]
            
        t0 = (c_center[d] - c_size - r_origin[d]) * inv 
        t1 = (c_center[d] + c_size - r_origin[d]) * inv
        if t0 > t1:
            t0, t1 = t1, t0
            
        if t0 > t_min:
            face_normal = PVector(0, 0, 0)
            face_normal[d] = 1
            cube_intersection_normal[ind] = face_normal 
            
        t_min = t0 if t0 > t_min else t_min
        t_max = t1 if t1 < t_max else t_max
        if t_max <= t_min:
            return None
    return intervals.Interval(t_min, t_max, ia=ind, ib=ind)


class Matrix:
    def __init__(self, data):
        self.m = data
        self.size = 3

    @staticmethod
    def zero():
        return Matrix([
                  [0.0, 0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0, 0.0],
                  ])
        
    @staticmethod
    def identity():
        return Matrix([
                  [1.0, 0.0, 0.0, 0.0],
                  [0.0, 1.0, 0.0, 0.0],
                  [0.0, 0.0, 1.0, 0.0],
                  [0.0, 0.0, 0.0, 1.0],
                  ])
        
    @staticmethod
    def rotationX(alpha):
        return Matrix([
                  [1.0, 0.0, 0.0, 0.0],
                  [0.0, math.cos(alpha), -math.sin(alpha), 0.0],
                  [0.0, math.sin(alpha), math.cos(alpha), 0.0],
                  [0.0, 0.0, 0.0, 1.0],
                  ])
        
    @staticmethod
    def rotationY(alpha):
        return Matrix([
                  
                  [math.cos(alpha), 0.0, math.sin(alpha), 0.0],
                  [0.0, 1.0, 0.0, 0.0],
                  [-math.sin(alpha), 0.0, math.cos(alpha), 0.0],
                  [0.0, 0.0, 0.0, 1.0],
                  ])
        
    @staticmethod
    def rotationZ(alpha):
        return Matrix([
                  [math.cos(alpha), -math.sin(alpha), 0.0, 0.0],
                  [math.sin(alpha), math.cos(alpha), 0.0, 0.0],
                  [0.0, 0.0, 1.0, 0.0],
                  [0.0, 0.0, 0.0, 1.0],
                  ])
        
    @staticmethod
    def rotation(ax, ay, az):
        mat = Matrix.identity()
        if abs(ax) > 0.0001:
            mat = mat.mul_matrix(Matrix.rotationX(ax))
        if abs(ay) > 0.0001:
            mat = mat.mul_matrix(Matrix.rotationY(ay))
        if abs(az) > 0.0001:
            mat = mat.mul_matrix(Matrix.rotationZ(az))
        return mat

    def mul_vector(self, v):
        ret = PVector()
        for d in range(self.size):
            ret[d] = 0
            for i in range(self.size):
                ret[d] += self.m[d][i] * v[i]
        return ret
    
    def mul_matrix(self, m):
        ret = Matrix.zero()
        for r in range(self.size):
            for c in range(self.size):
                for i in range(self.size):
                    ret.m[r][c] += self.m[r][i] * m.m[i][c]
        return ret
