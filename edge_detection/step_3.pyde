IMAGE = "peppers.png"


def setup():
    size(1024, 512)
    global img, imgr
    img = loadImage(IMAGE)
    imgr = createImage(img.width, img.height, RGB)
    
    kernel = get_kernel('edge_v')
    apply_filter(img, imgr, kernel)
  

def draw():
    image(img, 0, 0)
    image(imgr, 512, 0)


def keyPressed():
    kernel = None
    
    if key == '1':
        kernel = get_kernel('identity')
    if key == '2':
        kernel = get_kernel('blur')
    if key == '3':
        kernel = get_kernel('sharpen')
    if key == '4':
        kernel = get_kernel('edge_v')
    if key == '5':
        kernel = get_kernel('edge_h')
    if key == '6':
        kernel = get_kernel('edge')
    if key == '7':
        kernel = get_kernel('sobel')
    
    if kernel is not None: 
        apply_filter(img, imgr, kernel)
    

def get_kernel(type):
    if type == 'identity':
        return [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    if type == 'blur':
        v = 1.0 / 9.0
        return [[v, v, v], [v, v, v], [v, v, v]]
    if type == 'sharpen':
        return [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
    if type == 'edge':
        return [[1, 1, 1], [1, 0, -1], [-1, -1, -1]]
    if type == 'edge_v':
        return [[1, 0, -1], [1, 0, -1], [1, 0, -1]]
    if type == 'edge_h':
        return [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]
    if type == 'sobel':
        return [[1, 0, -1], [2, 0, -2], [1, 0, -1]]


def apply_filter(org, img, kernel):    
    img.loadPixels()
    for x in range(org.width):
        for y in range(org.height):            
            total = 0
            if x>0 and x<org.width-1 and y>0 and y<org.height-1:
                for dx in range(3):
                    for dy in range(3):
                        val = red(org.pixels[(y+dy-1)*org.width + x+dx-1])
                        total += val * kernel[dy][dx]
            img.pixels[y * org.width + x] = color(abs(total))
    img.updatePixels()
