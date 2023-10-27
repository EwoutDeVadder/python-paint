import pygame
from pygame.locals import *
import json
from tkinter import filedialog as fd

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
        self.colorList = []
    
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

        if self.mode == 1:
            x_index = 0
            y_index = 0
            goBackwards = False
            while True:
                self.frames.append(rectList[x_index][y_index].color)
                if goBackwards:
                    x_index -= 1
                else:
                    x_index += 1
                
                if x_index >= self.x_dim:
                    x_index -= 1
                    goBackwards = True

                    y_index += 1
                elif x_index < 0:
                    x_index += 1
                    goBackwards = False

                    y_index += 1

                if y_index >= self.y_dim:
                    break


        if self.mode == 2:
            x_index = 0
            y_index = 0
            goBackwards = False
            while True:
                self.frames.append(rectList[y_index][x_index].color)
                if goBackwards:
                    x_index -= 1
                else:
                    x_index += 1
                
                if x_index >= self.y_dim:
                    x_index -= 1
                    goBackwards = True

                    y_index += 1
                elif x_index < 0:
                    x_index += 1
                    goBackwards = False

                    y_index += 1

                if y_index >= self.x_dim:
                    break

        if self.mode == 3:
            x_index = self.x_dim-1
            y_index = 0
            goBackwards = True
            while True:
                self.frames.append(rectList[x_index][y_index].color)
                if goBackwards:
                    x_index -= 1
                else:
                    x_index += 1
                
                if x_index >= self.x_dim:
                    x_index -= 1
                    goBackwards = True

                    y_index += 1
                elif x_index < 0:
                    x_index += 1
                    goBackwards = False

                    y_index += 1

                if y_index >= self.y_dim:
                    break
        
        if self.mode == 4:
            x_index = 0
            y_index = self.y_dim-1
            goBackwards = False
            while True:
                self.frames.append(rectList[y_index][x_index].color)
                if goBackwards:
                    x_index -= 1
                else:
                    x_index += 1
                
                if x_index >= self.y_dim:
                    x_index -= 1
                    goBackwards = True

                    y_index -= 1
                elif x_index < 0:
                    x_index += 1
                    goBackwards = False

                    y_index -= 1

                if y_index < 0:
                    break
        
        if self.mode == 5:
            x_index = 0
            y_index = self.y_dim-1
            goBackwards = False
            while True:
                self.frames.append(rectList[x_index][y_index].color)
                if goBackwards:
                    x_index -= 1
                else:
                    x_index += 1
                
                if x_index >= self.x_dim:
                    x_index -= 1
                    goBackwards = True

                    y_index -= 1
                elif x_index < 0:
                    x_index += 1
                    goBackwards = False

                    y_index -= 1

                if y_index < 0:
                    break

        if self.mode == 6:
            x_index = self.x_dim-1
            y_index = 0
            goBackwards = True
            while True:
                self.frames.append(rectList[y_index][x_index].color)
                if goBackwards:
                    x_index -= 1
                else:
                    x_index += 1
                
                if x_index >= self.y_dim:
                    x_index -= 1
                    goBackwards = True

                    y_index += 1
                elif x_index < 0:
                    x_index += 1
                    goBackwards = False

                    y_index += 1

                if y_index >= self.x_dim:
                    break

        if self.mode == 7:
            x_index = self.x_dim-1
            y_index = self.y_dim-1
            goBackwards = True
            while True:
                self.frames.append(rectList[x_index][y_index].color)
                if goBackwards:
                    x_index -= 1
                else:
                    x_index += 1
                
                if x_index >= self.x_dim:
                    x_index -= 1
                    goBackwards = True

                    y_index -= 1
                elif x_index < 0:
                    x_index += 1
                    goBackwards = False

                    y_index -= 1

                if y_index < 0:
                    break

        if self.mode == 8:
            x_index = self.x_dim-1
            y_index = self.y_dim-1
            goBackwards = True
            while True:
                self.frames.append(rectList[y_index][x_index].color)
                if goBackwards:
                    x_index -= 1
                else:
                    x_index += 1
                
                if x_index >= self.y_dim:
                    x_index -= 1
                    goBackwards = True

                    y_index -= 1
                elif x_index < 0:
                    x_index += 1
                    goBackwards = False

                    y_index -= 1

                if y_index < 0:
                    break

        
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

    def importData(self):
        self.loadJson()
        try:
            self.x_dim = self.dict['x_dim']
            self.y_dim = self.dict['y_dim']
            self.brightness = self.dict['brightness']
            self.frame_time = self.dict['frame_time']
            self.num_frames = self.dict['num_frames']
            self.mode = self.dict['mode']
            self.frames = self.dict['frames']
        except :
            raise TypeError(f'Opened wrong type of file. Opened file is not an image or gif with the right values.') 
        
        self.decodeFrames()
    
    def decodeFrames(self):
        newList = []
        rows = round(len(self.frames)/self.x_dim)
        if self.mode == 0:
            for x in range(self.x_dim):
                for y in range(self.y_dim):
                    newList.append(self.dict['frames'][x+rows*y])
        if self.mode == 1:
            itemlist = []
            index = 0
            x_index = 0
            lock = False
            for x in range(self.x_dim):
                    itemlist.append([])
            while True:
                for x in range(self.x_dim):
                    itemlist[x_index].append(self.dict['frames'][index])
                    index += 1

                if lock:
                    x_index -= 1
                else:
                    x_index += 1

                if x_index > self.x_dim:
                    lock = True
                    x_index -= 1
                elif x_index < 0:
                    lock = False
                    x_index += 1

                if index == (self.y_dim*self.x_dim):
                    print(itemlist)
                    break
            for list in itemlist:
                for item in list:
                    newList.append(item)
                                
        self.colorList = newList
    
    def saveJson(self):
        file  = fd.asksaveasfile(filetypes=[['json file','*.json']], defaultextension=[['json file','*.json']])
        if file == None:
            return
        try:
            with open(file.name, 'w') as json_file:
                json.dump(self.dict, json_file)
        except :
            raise TypeError(f'Something went wrong. Please issue a bug to https://github.com/EwoutDeVadder/python-paint/issues') 
            

    def loadJson(self):
        file  = fd.askopenfile(filetypes=[['json file','*.json']])
        if file == None:
            return
        with open(file.name, 'r') as json_file:
            self.dict = json.load(json_file)