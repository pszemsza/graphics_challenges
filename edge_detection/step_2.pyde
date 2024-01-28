IMAGE = "peppers.png"
KERNEL = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]


def setup():
    size(1024, 512)
    global img, imgr
    img = loadImage(IMAGE)
    imgr = createImage(img.width, img.height, RGB)
    apply_filter(img, imgr, KERNEL)
  

def draw():
    image(img, 0, 0)
    image(imgr, 512, 0)


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
