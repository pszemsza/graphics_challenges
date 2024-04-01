import math

width = 800
height = 600

minX = -2
maxX = 2
minY = -1.5
maxY = 1.5
maxIterations = 100
zoomFactor = 0.8

c_real = 0.22
c_imag = 0.52


def setup():
    size(width, height)
    colorMode(RGB, 1)
    smooth()

def draw():
    loadPixels()
    
    # loop through every pixel on the canvas
    for x in range(width):
        for y in range(height):
            # map pixel coordinates to the complex plane
            a = map(x, 0, width, minX, maxX)
            b = map(y, 0, height, minY, maxY)
            
            n = 0
            while n < maxIterations:
                real = a * a - b * b
                imaginary = 2 * a * b
                a = real + c_real
                b = imaginary + c_imag
                
                # We should check for the magnitude, but taking simply a+b also gives nice results  
                #if abs(a*a + b*b) > 2:
                if abs(a + b) > 2:
                    break
                n += 1
            
            # find a color
            col = map(n%20, 0, 20, 0.3, 1)
            if n == maxIterations:
                col = 0
                           
            # Draw the pixel
            index = x + y * width
            pixels[index] = color(col)
    
    updatePixels()


def zoom(factor):
    global minX, maxX, minY, maxY
    rx = (maxX - minX) / 2
    ry = (maxY - minY) / 2
    centerX = (maxX + minX) / 2.0
    centerY = (maxY + minY) / 2.0
    minX = centerX - rx * factor
    maxX = centerX + rx * factor
    minY = centerY - ry * factor
    maxY = centerY + ry * factor

# center at the clicked point
def center(x, y):
    global minX, maxX, minY, maxY
    rx = maxX - minX
    ry = maxY - minY
    dx = map(x, 0, width, -rx / 2.0, rx / 2.0)
    dy = map(y, 0, height, -ry / 2.0, ry / 2.0)
    minX += dx
    minY += dy       
    maxX += dx
    maxY += dy


def mousePressed():
    global c_real, c_imag    
    if mouseButton == LEFT:
        center(mouseX, mouseY)                
    elif mouseButton == RIGHT:
        c_real = map(mouseX, 0, width, -1, 1)
        c_imag = map(mouseY, 0, height, -1, 1)


def keyPressed():
    global maxIterations, zoomFactor, minX, maxX, minY, maxY
    
    d = (maxX - minX) / 10.0
    if keyCode == LEFT:
        minX += d    
        maxX += d
    if keyCode == RIGHT:
        minX -= d    
        maxX -= d
    if keyCode == UP:
        minY += d    
        maxY += d
    if keyCode == DOWN:
        minY -= d    
        maxY -= d

    if key == 'q':
        maxIterations -= 5
        if maxIterations < 5:
            maxIterations = 5
    if key == 'w':
        maxIterations += 5

    if key == 'z':
        zoom(zoomFactor)
    if key == 'x':
        zoom(1.0 / zoomFactor) 