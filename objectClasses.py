import pygame
from pygame.locals import *
import json

#
# OBJECT CLASS
#


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

#
# OBJECT CLASS :: TYPES
#

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

#
# OBJECT CLASS :: COLLIDER
#

class Collider:
    def __init__(self, position, dimension) -> None:
        self.position = position
        self.dimension = dimension

    def checkForMouseCollision(self, event):
        if self.position[0] < event['pos'][0] < self.position[0]+self.dimension[0] and self.position[1] < event['pos'][1] < self.position[1]+self.dimension[1]:
            return True
        
#
# MATRIX DATA CLASS
#

class MatrixData:
    def __init__(self, x_dim, y_dim, brightness=17, frame_time=0, num_frames=1,mode=0) -> None:
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.brightness = brightness
        self.frame_time = frame_time
        self.num_frames = num_frames
        self.mode = mode
        self.frames = []
        self.dict = {}
    
    def exportData(self, rectList):
        # reset frame to pack new one.
        self.frames = []

        # make new frames according to mode
        if self.mode == 0:
            index = 0
            while True:
                for row in rectList:
                    self.frames.append(row[index].color)
                if index == len(rectList)-1:
                    break
                index += 1
        
        self.makeDictionary()       
        self.saveJson() 

    def makeDictionary(self):
        self.dict = {
            'x_dim': self.x_dim,
            'y_dim': self.y_dim,
            'brightness': self.brightness,
            'frame_time': self.frame_time,
            'num_frames': self.num_frames,
            'mode': self.mode,
            'frames': self.frames
        }

    def saveJson(self):
        with open('save.json', 'w') as json_file:
            json.dump(self.dict, json_file)

    def importData(self):
        self.loadJson()
        self.x_dim = self.dict['x_dim']
        self.y_dim = self.dict['y_dim']
        self.brightness = self.dict['brightness']
        self.frame_time = self.dict['frame_time']
        self.num_frames = self.dict['num_frames']
        self.mode = self.dict['mode']
        self.frames = self.dict['frames']
    def loadJson(self):
        with open('save.json', 'r') as json_file:
            self.dict = json.load(json_file)