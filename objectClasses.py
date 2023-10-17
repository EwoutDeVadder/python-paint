import pygame
from pygame.locals import *

class Object:
    def __init__(self) -> None:
        self.position
        self.dimension
        self.displaySurface

        self.type

        self.color

    def addAccentColor(self, color):
        self.accentColor = color

    def addCollider(self):
        self.collider = Collider()


class Slider:
    def __init__(self) -> None:
        self.position
        self.dimension
        self.displaySurface

        self.valueRange
        self.currentValue

        self.color
        self.accentColor


class Rectangle:
    def __init__(self) -> None:
        self.position
        self.dimension
        self.displaySurface

        self.rectangle


class Collider:
    def __init__(self) -> None:
        self.position
        self.dimension

    def checkForMouseCollision(self, event):
        if self.position[0] < event['pos'][0] < self.position[0]+self.dimension[0] and self.position[1] < event['pos'][1] < self.position[1]+self.dimension[1]:
            return True