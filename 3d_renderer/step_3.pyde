import math

is_running = True       
matrix_proj = None
objects = []


def setup():
    global matrix_proj
    background(0)
    size(400, 300)
    stroke(255)
    strokeWeight(1)
     
    objects.append(Object.cube(200, 150, 200, 140))
    matrix_proj = Matrix.ortographic_projection()   


def draw():
    if not is_running:
        return
    background(0)

    mat_rot = Matrix.rotation(0.01, 0.006, 0.0055)
    for o in objects:
        o.transform_local(mat_rot)
        draw_object(o)


def draw_object(o):  
    pts_2d = [None] * len(o.vertices)
    
    for i, v in enumerate(o.vertices):
        pts_2d[i] = matrix_proj.mul_vector(v)
        
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


def mousePressed():
    global is_running
    is_running = not is_running


class Vector:
    def __init__(self, x=0, y=0, z=0, w=0):
        self.v = [x, y, z, w]
            
    def __getitem__(self, key):
        return self.v[key]


class Matrix:
    def __init__(self, data):
        self.m = data
        self.size = 4


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
    def translation(x, y, z):
        return Matrix([
                  [1.0, 0.0, 0.0, x],
                  [0.0, 1.0, 0.0, y],
                  [0.0, 0.0, 1.0, z],
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

        
    @staticmethod
    def ortographic_projection():
        return Matrix([
                  [1.0, 0.0, 0.0, 0.0],
                  [0.0, 1.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0, 1.0],
                  ])
        
    def mul_vector(self, v):
        ret = Vector()
        for d in range(self.size):
            ret.v[d] = 0
            for i in range(self.size):
                ret.v[d] += self.m[d][i] * v[i]
        return ret
    
    def mul_matrix(self, m):
        ret = Matrix.zero()
        for r in range(self.size):
            for c in range(self.size):
                for i in range(self.size):
                    ret.m[r][c] += self.m[r][i] * m.m[i][c]
        return ret
    
    def __repr__(self):
        return str(self.m)


class Object:
    def __init__(self, cx=0.0, cy=0.0, cz=0.0):
        self.center = Vector(cx, cy, cz)
        self.vertices = []
        self.indices = []
        
    def transform(self, m):
        for i in range(len(self.vertices)):
            self.vertices[i] = m.mul_vector(self.vertices[i])
            
    def transform_local(self, m):
        trans_m = Matrix.translation(self.center[0], self.center[1], self.center[2])
        trans_m = trans_m.mul_matrix(m)
        trans_m = trans_m.mul_matrix(Matrix.translation(-self.center[0], -self.center[1], -self.center[2]))
        self.transform(trans_m)

    @staticmethod
    def cuboid(cx, cy, cz, sx, sy, sz):
        ret = Object()
        ret.center = [cx, cy, cz]
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
