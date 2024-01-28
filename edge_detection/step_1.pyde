import random

IMAGE = "peppers.png"


def setup():
    size(1024, 512)
    global img, imgr
    img = loadImage(IMAGE)  
    imgr = createImage(img.width, img.height, RGB);
    imgr.loadPixels()
    for x in range(img.width):
        for y in range(img.height):
            pos = y * img.width + x
            imgr.pixels[pos] = color(red(img.pixels[pos]) / 2)
    imgr.updatePixels()
    

def draw():
    image(img, 0, 0)
    image(imgr, 512, 0)
