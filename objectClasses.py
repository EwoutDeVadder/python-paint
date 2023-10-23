import pygame
from pygame.locals import *

class Object:
    def __init__(self, position, dimension, displaySurface, objType, color, string = '', sliderDimension = 15, sliderValueRange = [0, 15], accentColor = (0, 0, 0)) -> None:
        self.position = position
        self.dimension = dimension
        self.displaySurface = displaySurface

        self.type = objType

        self.string = string

        self.sliderValueRange = sliderValueRange
        self.sliderDimension = sliderDimension

        self.accentColor = accentColor

        self.addComponentByType()

        self.color = color

    def addAccentColor(self, color):
        self.accentColor = color

    def addCollider(self):
        self.collider = Collider(self.position, self.dimension)

    def addComponentByType(self):
        if self.type == 'slider':
            self.slider = Slider(self.position, self.dimension, self.sliderDimension, self.sliderValueRange)
            return
        
        if self.type == 'rectangle':
            self.rectangle = Rectangle(self.position, self.dimension)
            return
        
        if self.type == 'text':
            self.text = Text()
            return

    def drawObject(self):
        if self.type == 'slider':
            self.slider.updateSliderValue(self.position, self.dimension)
            pygame.draw.rect(self.displaySurface, self.color, self.slider.rectangle)
            pygame.draw.circle(self.displaySurface, self.accentColor, self.slider.center, self.slider.sliderDimension)

        if self.type == 'rectangle':
            pygame.draw.rect(self.displaySurface, self.color, self.rectangle.rectangle)

        if self.type == 'text':
            self.textFont = self.text.font.render(self.string, True, self.accentColor, self.color)
            self.displaySurface.blit(self.textFont, self.position)

class Slider:
    def __init__(self, position, dimension, sliderDimension, valueRange = [0, 15]) -> None:
        self.valueRange = valueRange
        self.currentValue = valueRange[0]
        self.center = (position[0], (position[1]+position[1]+dimension[1])/2)

        self.rectangle = pygame.Rect(position[0], position[1], dimension[0], dimension[1])
        self.sliderDimension = sliderDimension
        self.sliderPosition = (position[0], (position[1]+position[1]+dimension[1])/2)

    def updateSliderValue(self, position, dimension):
        self.currentValue = round(self.center[0]/(dimension[0]+position[0])*self.valueRange[1])

class Rectangle:
    def __init__(self, position, dimension) -> None:
        self.rectangle = pygame.Rect(position[0], position[1], dimension[0], dimension[1])


class Text:
    def __init__(self) -> None:
        self.font = pygame.font.Font('freesansbold.ttf', 32)

class Collider:
    def __init__(self, position, dimension) -> None:
        self.position = position
        self.dimension = dimension

    def checkForMouseCollision(self, event):
        if self.position[0] < event['pos'][0] < self.position[0]+self.dimension[0] and self.position[1] < event['pos'][1] < self.position[1]+self.dimension[1]:
            return True