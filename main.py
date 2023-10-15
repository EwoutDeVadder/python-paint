# ---------------------------------------------------------------------- #
## GENERAL INFORMATION ##
# Mode by: Ewout
# Project Manager: Mr. Buys
# About: Mspaint sucks so we're making our own.
# ---------------------------------------------------------------------- #
## SOURCES ##
# - JSON
# https://www.geeksforgeeks.org/read-json-file-using-python/
# https://www.w3schools.com/python/python_json.asp
# ---------------------------------------------------------------------- #
## CHANGELOG ##
# v0.1
# Forgot to keep track of all my progress but I will from now on.
# Added sliders
# Added custom color palettes
# Added sliders for custom colors
# Added dynamic pixel ranges (x,y)
# Added fullscreen
# Sorted everything in classes
# Cleaned up some abandoned code
# ---------------------------------------------------------------------- #
## TODO ##
# Recent colors
# save current color palette if new one was made
# save current drawing + open a previous drawing
# --> different ways to save to JSON (bottom to top, top to bottom, left to right, right to left, ...)
# [COMPLETE]Color palletes
# [COMPLETE]--> basic color palette at start
# ---------------------------------------------------------------------- #
import pygame
pygame.init()
import sys
from pygame.locals import *
import json

pixelDimentions = [16, 16]
spaceBetween = 0.1
pixel_width = 50

startingDeadSpace = 10

slider_width = 500
slider_height = 50
sliderExtraHeight = 2
slidersOffset = 30

fullscreenMode = True
colorPickerHeight = 150

customColorPalette = True
colorPaletteName = "color_palette.json"
colorPalette = 0
colorPaletteOffset = 10
colorPaletteWidth = pixel_width

extraWidth = slider_width+colorPaletteWidth*2

if customColorPalette:
    json_palette = open(colorPaletteName)
    colorPalette = json.load(json_palette)

#colours
#R    G    B
WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)

BGCOLOR = BLACK

class Slider:
    def __init__(self, display, pos, width, height, color, subColor,  maximum = 255) -> None:
        self.width = width
        self.height = height
        self.pos = pos
        self.displaysurf = display
        self.rectangle = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.color = color
        self.secondaryColor = subColor
        self.max = maximum
        self.sliderCirclePosition = (self.pos[0], self.pos[1]+(self.height/2))

    def drawRect(self):
        pygame.draw.rect(self.displaysurf, self.color, self.rectangle, 2)
    
    def drawSlider(self):
        pygame.draw.circle(self.displaysurf,self.secondaryColor, self.sliderCirclePosition, self.height/2+sliderExtraHeight)

    def moveSlider(self, mousePos):
        if self.pos[0] < mousePos[0] and self.pos[1] < mousePos[1] and self.pos[0]+self.width > mousePos[0] and self.pos[1]+self.height > mousePos[1]:
            self.sliderCirclePosition = (mousePos[0], self.pos[1]+(self.height/2))

    def getColor(self):
        return round((self.sliderCirclePosition[0]/(self.pos[0]+self.width))*self.max)
            
class WindowHandler:
    def __init__(self,fullscreenMode = False) -> None:
        self.isFullscreen = fullscreenMode
        self.FPSCLOCK = pygame.time.Clock()
    
    def screenDimentions(self, pixelDimentions, pixel_width, spaceBetween = 0.5, startingDeadSpace = 20, colorPickerHeight = 150, extraWidth = 0):
        if self.isFullscreen:
            fullscreenList = pygame.display.list_modes()
            self.width = fullscreenList[0][0]
            self.height = fullscreenList[0][1]
        else:
            self.width = (pixel_width*pixelDimentions[0]) + ((pixel_width*pixelDimentions[0]) * spaceBetween) + startingDeadSpace + extraWidth
            self.height = (pixel_width*pixelDimentions[1]) + ((pixel_width*pixelDimentions[1]) * spaceBetween) + colorPickerHeight
        self.space_per_pixel_width = ((pixel_width*pixelDimentions[0]) * spaceBetween) / pixelDimentions[0]
        self.space_per_pixel_height = ((pixel_width*pixelDimentions[1]) * spaceBetween) / pixelDimentions[1]

        self.DISPLAYSURF = pygame.display.set_mode((self.width, self.height))

class Rectangle:
    def __init__(self, rectangle, startingPosition = 0, endingPosition = 0, color = WHITE) -> None:
        self.rectangle = rectangle
        self.startingPosition = startingPosition
        self.endingPosition = endingPosition
        self.color = color
    

class HandleRectangles:
    def __init__(self, pixelDimention, rectWidth) -> None:
        self.rectList = []
        self.pixelDimentions = pixelDimentions
        self.rectangleWidth = rectWidth

    def drawRectangles(self, display):
        for row in self.rectList:
            for rectangle in row:
                pygame.draw.rect(display, rectangle.color, rectangle.rectangle)

    def makeRectangleList(self, space_per_pixel_width, space_per_pixel_height):
        for index_x in range(self.pixelDimentions[0]):
            myList = []
            for index_y in range(self.pixelDimentions[1]):
                position = (space_per_pixel_width+self.rectangleWidth)*index_x+startingDeadSpace,(space_per_pixel_height+self.rectangleWidth)*index_y+startingDeadSpace
                rect = pygame.Rect(position[0], position[1],self.rectangleWidth,self.rectangleWidth)
                myList.append(Rectangle(rect, position, (position[0]+self.rectangleWidth, position[1]+self.rectangleWidth), WHITE))
            self.rectList.append(myList)
    
    def buttonHandlerForSquares(self, event):
        posInList = [0,0]
        for rectRows in self.rectList:
            for rect in rectRows:
                if rect.startingPosition[0] <= event['pos'][0] and rect.startingPosition[1] <= event['pos'][1] and rect.endingPosition[0] >= event['pos'][0] and rect.endingPosition[1] >= event['pos'][1]:
                    return rect, posInList
                posInList[1] += 1
            posInList[1] = 0
            posInList[0] += 1
        return False

class ColorPaletteHandler:
    def __init__(self, customPalette, colorPalette) -> None:
        self.colors = colorPalette
        self.customPalette = customPalette
        self.rects = []

    def rectangleConfiguration(self, pos, width):
        self.rects.append(Rectangle( pygame.Rect(pos[0]+width, pos[1], width, width), (pos[0]+width, pos[1]), (pos[0]+width+width, pos[1]+width)))
        if self.customPalette == False:
            return
        for index, color in enumerate(self.colors):
            self.rects.append(Rectangle( pygame.Rect(pos[0]+width*(index+2), pos[1], width, width), (pos[0]+width*(index+2), pos[1]), (pos[0]+width*(index+2)+width, pos[1]+width), (self.colors[color][0]*17, self.colors[color][1]*17, self.colors[color][2]*17)))
        

    def buttonHandler(self, event):
        for colorpos in self.rects:
            if colorpos.startingPosition[0] < event['pos'][0] < colorpos.endingPosition[0] and colorpos.startingPosition[1] < event['pos'][1] < colorpos.endingPosition[1]:
                return colorpos.color
            
    def drawColors(self, dislpay):
        for rect in self.rects:
            pygame.draw.rect(dislpay, rect.color, rect.rectangle)


def main():
    rectangleList = HandleRectangles(pixelDimentions, pixel_width)

    window = WindowHandler(fullscreenMode)
    window.screenDimentions(rectangleList.pixelDimentions, rectangleList.rectangleWidth, spaceBetween=spaceBetween, startingDeadSpace=startingDeadSpace, colorPickerHeight=colorPickerHeight, extraWidth=extraWidth)
    window.DISPLAYSURF.fill(BGCOLOR)

    rectangleList.makeRectangleList(window.space_per_pixel_width, window.space_per_pixel_height)
    rectangleList.drawRectangles(window.DISPLAYSURF)

    redSlider = Slider(window.DISPLAYSURF, (startingDeadSpace, window.height-colorPickerHeight-30+slider_height), slider_width, slider_height/2, GREY, WHITE, 15)
    greenSlider = Slider(window.DISPLAYSURF, (startingDeadSpace, window.height-colorPickerHeight-30+slider_height + slidersOffset), slider_width, slider_height/2, GREY, WHITE, 15)
    blueSlider = Slider(window.DISPLAYSURF, (startingDeadSpace, window.height-colorPickerHeight-30+slider_height + slidersOffset*2), slider_width, slider_height/2, GREY, WHITE, 15)

    customcolorpalettest = ColorPaletteHandler( customColorPalette, colorPalette)
    customcolorpalettest.rectangleConfiguration((startingDeadSpace+slider_width+colorPaletteOffset, window.height-colorPickerHeight+slider_height), colorPaletteWidth)

    selectedColor = tuple([0,0,0])
    mouseDown = False
    mousePos = (0,0)
    while True:

        rectangleList.drawRectangles(window.DISPLAYSURF)

        customcolorpalettest.drawColors(window.DISPLAYSURF)

        redSlider.drawRect()
        greenSlider.drawRect()
        blueSlider.drawRect()

        redSlider.drawSlider()
        greenSlider.drawSlider()
        blueSlider.drawSlider()

        if customcolorpalettest.rects[0].color != (redSlider.getColor() * 17, greenSlider.getColor() * 17, blueSlider.getColor() * 17):
            customcolorpalettest.rects[0].color = (redSlider.getColor() * 17, greenSlider.getColor() * 17, blueSlider.getColor() * 17)
            selectedColor = customcolorpalettest.rects[0].color

        if mouseDown:
            rectangleFound = rectangleList.buttonHandlerForSquares(event.dict)
            if rectangleFound:
                rectangleList.rectList[rectangleFound[1][0]][rectangleFound[1][1]].color = selectedColor

            rectangleFound = customcolorpalettest.buttonHandler(event.dict)
            if rectangleFound:
                selectedColor = rectangleFound

            redSlider.moveSlider(mousePos)
            greenSlider.moveSlider(mousePos)
            blueSlider.moveSlider(mousePos)

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN:
                mouseDown = True
            if event.type == MOUSEBUTTONUP:
                mouseDown = False
            if event.type == MOUSEMOTION:
                mousePos = event.dict['pos']

        pygame.display.update()
        window.DISPLAYSURF.fill(BGCOLOR)
        window.FPSCLOCK.tick(0)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()