import pygame
from pygame.locals import *

class Object:
    def __init__(self, position, dimension, displaySurface, objType, color) -> None:
        self.position = position
        self.dimension = dimension
        self.displaySurface = displaySurface

        self.type = objType

        self.color = color

    def addAccentColor(self, color):
        self.accentColor = color

    def addCollider(self):
        self.collider = Collider(self.position, self.dimension)

    def addComponentByType(self):
        if self.type == 'slider':
            self.slider = Slider(self.positon, self.dimension)
            return
        
        if self.type == 'rectangle':
            self.rectangle = Rectangle(self.position, self.dimension)
            return
        
    def drawObject(self):
        if self.type == 'slider':
            pygame.draw.rect(self.displaySurface, self.color, self.slider.rectangle)
            pygame.draw.circle(self.displaySurface, self.accentColor, ())

        if self.type == 'rectangle':
            pygame.draw.rect(self.displaySurface, self.color, self.rectangle.rectangle)


class Slider:
    def __init__(self, position, dimension, sliderDimension, valueRange = [0, 15]) -> None:
        self.valueRange = valueRange
        self.currentValue = valueRange[0]

        self.rectangle = pygame.Rect(position[0], position[1], dimension[0], dimension[1])
        self.sliderRect = pygame.Rect(position[0], position[1]+(dimension[1]/2), sliderDimension[0], sliderDimension[1])

class Rectangle:
    def __init__(self, position, dimension) -> None:
        self.rectangle = pygame.Rect(position[0], position[1], dimension[0], dimension[1])


class Collider:
    def __init__(self, position, dimension) -> None:
        self.position = position
        self.dimension = dimension

    def checkForMouseCollision(self, event):
        if self.position[0] < event['pos'][0] < self.position[0]+self.dimension[0] and self.position[1] < event['pos'][1] < self.position[1]+self.dimension[1]:
            return True