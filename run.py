#-------------------------
# LIBRARIES
#-------------------------
import pygame
pygame.init()
import sys
from pygame.locals import *
import json

from objectClasses import *
#-------------------------
# GLOBAL VARIABLES
#-------------------------

fullscreen = False
# A minimum of atleast 800x400 is required
screenResolution = [1600, 800]
screenResolutionForColors = [0,200]

drawingGrid = [16, 16]

# percentage of screen what should be dead space. FOR THE WIDTH AND HEIGHT
deadSpaceBetweenGrid = 0.2

#RGB VALUES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BGCOLOR = BLACK

#-------------------------
# BASIC CONFIGURATIONS AND CHECKS
#-------------------------
def config(screenResolution):
    minimumScreenResolution = [800, 400]
    # configuring screen height , width
    if fullscreen:
        screenResolution = pygame.display.list_modes()[0]

    elif screenResolution[0] < minimumScreenResolution[0] or screenResolution[1] < minimumScreenResolution[1]:
        print("ERR: RESOLUTION WAS NOT CONFIGURED PROPERLY, STANDARD RESOLUTION HAS BEEN USED INSTEAD.")
        screenResolution = minimumScreenResolution
    
    # configuring pixel_width and deadspace according to screen-width and height
    screenResolutionForPixels = [screenResolution[0]-screenResolutionForColors[0], screenResolution[1]-screenResolutionForColors[1]]
    pixelWidth = (screenResolutionForPixels[0]-screenResolutionForPixels[0]*deadSpaceBetweenGrid)/drawingGrid[0]
    if pixelWidth*screenResolutionForPixels[1] > screenResolution[1]:
        pixelWidth = (screenResolutionForPixels[1]-screenResolutionForPixels[1]*deadSpaceBetweenGrid)/drawingGrid[1]
    
    deadSpacePerPixel = screenResolutionForPixels[1]*deadSpaceBetweenGrid/pixelWidth

    # configuring the display surface, fps clock
    displaySurface = pygame.display.set_mode((screenResolution[0], screenResolution[1]))
    fpsClock = pygame.time.Clock()
    # return some nessesary values for other parts of the code
    return pixelWidth, deadSpacePerPixel, displaySurface, fpsClock

pixelWidth, deadSpacePerPixel, displaySurface, fpsClock = config(screenResolution)

#-------------------------
# MAIN CODE
#-------------------------

def main():
    # drawing the pixel grid
    pixelGrid = []
    for x_pixel in range(drawingGrid[0]):
        y_pixels = []
        for y_pixel in range(drawingGrid[1]):
            y_pixels.append(Object(
                position= ((pixelWidth+deadSpacePerPixel)*x_pixel, (pixelWidth+deadSpacePerPixel)*y_pixel),
                dimension= (pixelWidth, pixelWidth),
                displaySurface= displaySurface,
                objType= 'rectangle',
                color= WHITE
            ))
            y_pixels[y_pixel].addComponentByType()

        pixelGrid.append(y_pixels)

    while True:

        for row in pixelGrid:
            for pixel in row:
                pixel.drawObject()

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()

        pygame.display.update()
        displaySurface.fill(BGCOLOR)
        fpsClock.tick(0)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()