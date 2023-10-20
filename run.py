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

drawingGrid = [16, 16]

fullscreen = False
# A minimum of atleast 800x400 is required
screenResolution = [1600, 800]

screenResolutionForColors = [0, 200]

# percentage of screen what should be dead space. FOR THE WIDTH AND HEIGHT
deadSpaceBetweenGrid = 0.2

# is there a color_palette.json in the directory
isThereAColorPalette = True
colorPaletteName = 'color_palette.json'

# should remember how many colors?
recentColorAmount = 5

#RGB VALUES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (122, 122, 122)

colorMultiplier = 17

BGCOLOR = BLACK

#-------------------------
# BASIC CONFIGURATIONS AND CHECKS
#-------------------------

deadSpaceAtStartForRGBSliders = 20

rgbSliderDimensions = [500,20]
rgbSliderDeadSpace = 15

deadSpaceColorPalette = 20

colorPaletteWidth = 50

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
    return screenResolution, pixelWidth, deadSpacePerPixel, displaySurface, fpsClock

screenResolution, pixelWidth, deadSpacePerPixel, displaySurface, fpsClock = config(screenResolution)

# color palette screen resolution aftr the screenresolution was configured to avoid incorrect variables
colorPaletteDimensions = [rgbSliderDimensions[0]+deadSpaceAtStartForRGBSliders+deadSpaceColorPalette, screenResolution[1]-screenResolutionForColors[1]]

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
                position= ((pixelWidth+deadSpacePerPixel)*x_pixel+deadSpacePerPixel, (pixelWidth+deadSpacePerPixel)*y_pixel+deadSpacePerPixel),
                dimension= (pixelWidth, pixelWidth),
                displaySurface= displaySurface,
                objType= 'rectangle',
                color= WHITE
            ))
            y_pixels[y_pixel].addCollider()

        pixelGrid.append(y_pixels)

    # RGB sliders
    colorSliderList = []
    for index in range(3):
        colorSliderList.append(Object(
            position= (deadSpaceAtStartForRGBSliders, (screenResolution[1]-screenResolutionForColors[1])+rgbSliderDimensions[1]*(index+1)+rgbSliderDeadSpace*index),
            dimension= rgbSliderDimensions,
            displaySurface= displaySurface,
            objType= 'slider',
            color= WHITE
        ))
        colorSliderList[index].addComponentByType(13)
        colorSliderList[index].addAccentColor(GREY)
        colorSliderList[index].addCollider()

    # makes background of sliders Red, Green and Blue
    colorSliderList[0].color = (160, 0, 0)
    colorSliderList[1].color = (0, 160 ,0)
    colorSliderList[2].color = (0, 0, 160)

    # get the colorpalette.json imported
    colorPaletteList = [Object([colorPaletteDimensions[0], colorPaletteDimensions[1]], [colorPaletteWidth, colorPaletteWidth], displaySurface, 'rectangle', BLACK)]
    colorPaletteList[0].addCollider()
    if isThereAColorPalette:
        jsonPalette = open(colorPaletteName, 'r')
        colorPalette = json.load(jsonPalette)
        for index, color in enumerate(colorPalette):
            colorPaletteList.append(Object(
                position= [colorPaletteDimensions[0]+colorPaletteWidth*(index+1), colorPaletteDimensions[1]],
                dimension= [colorPaletteWidth, colorPaletteWidth],
                displaySurface= displaySurface,
                objType= 'rectangle',
                color= (colorPalette[color][0]*colorMultiplier, colorPalette[color][1]*colorMultiplier, colorPalette[color][2]*colorMultiplier)))
            colorPaletteList[index+1].addCollider()
    
    recentColors = [(0,0,0)]
    for color in range(recentColorAmount):
        pass

    mouseDown = False
    mouseDownDelay = False
    selectedColor = (0,0,0)
    # main loop function
    while True:

        # add new color to recent color if color has changed in the past frame.
        if recentColors[-1] != selectedColor:
            recentColors.append(selectedColor)

        # check if recentColors is too long
        if len(recentColors) > recentColorAmount-1:
            del(recentColors[0])

        # draw pixel grid
        for row in pixelGrid:
            for pixel in row:
                pixel.drawObject()

        # draw sliders
        for slider in colorSliderList:
            slider.drawObject()

        # draw color palette rectangles
        for color in colorPaletteList:
            color.drawObject()

        # mouse down continuous
        if mouseDown:
            # Change selected color if sliders have been changed.
            for slider in colorSliderList:
                if slider.collider.checkForMouseCollision(event.dict):
                    slider.slider.center = (event.dict['pos'][0], slider.slider.center[1])
                    selectedColor = (colorSliderList[0].slider.currentValue * colorMultiplier, colorSliderList[1].slider.currentValue * colorMultiplier, colorSliderList[2].slider.currentValue * colorMultiplier)
                    colorPaletteList[0].color =  selectedColor

            # Change color of pixel if pixel has been pressed.
            for row in pixelGrid:
                for pixel in row:
                    if pixel.collider.checkForMouseCollision(event.dict):
                        pixel.color = selectedColor

        # mouse down once
        if mouseDown != mouseDownDelay and mouseDown == True:
            mouseDownDelay = mouseDown
            
            for color in colorPaletteList:
                if color.collider.checkForMouseCollision(event.dict):
                    selectedColor = (color.color[0], color.color[1], color.color[2])
                

        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN:
                mouseDown = True
            if event.type == MOUSEBUTTONUP:
                mouseDown = False
                mouseDownDelay = False

        # Clear the screen and prepare the following frame
        pygame.display.update()
        displaySurface.fill(BGCOLOR)
        fpsClock.tick(0)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()