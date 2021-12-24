import tkinter as tk
import pygame
from PIL import Image as img
import PIL
from datetime import datetime
import shutil
import os
import random

currentDir = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.mkdir(f"local/{currentDir}")
os.mkdir(f"local/{currentDir}/edited")


class Image:
    def __init__(self, id, image, canvas, x=0, y=0, width=None, height=None, scale=1):
        self.x = 0
        self.y = 0
        self.ID = id
        self.scale = 1
        self.name = image.split("/")[-1].split(".")[0] + "_" + str(id)
        self.canvas = canvas
        self.ext = image.split("/")[-1].split(".")[-1]
        self.type = "image"
        
        file = self.name + "." + self.ext
        shutil.copy(image, f"local/{currentDir}/{file}")
        shutil.copy(image, f"local/{currentDir}/edited/{file}")
        
        self.unedited = r"local/{currentDir}/{file}".format(currentDir = currentDir, file = file)
        self.edited = r"local/{currentDir}/edited/{file}".format(currentDir = currentDir, file = file)
        openedImage = img.open(self.unedited)
        self.width, self.height = openedImage.size
        self.file = tk.PhotoImage(file = self.edited)
        self.code = []
    
    def changeName(self, name, objects):
        if name not in objects.keys():
            self.name = name
            os.rename(self.unedited, r"local/{currentDir}/{name}.{ext}".format(currentDir = currentDir, name = name, ext = self.unedited.split("/")[-1].split(".")[-1]))
            self.unedited = r"local/{currentDir}/{name}.{ext}".format(currentDir = currentDir, name = name, ext = self.unedited.split("/")[-1].split(".")[-1])
            os.rename(self.edited, r"local/{currentDir}/edited/{name}.{ext}".format(currentDir = currentDir, name = name, ext = self.edited.split("/")[-1].split(".")[-1]))
            self.edited = r"local/{currentDir}/edited/{name}.{ext}".format(currentDir = currentDir, name = name, ext = self.edited.split("/")[-1].split(".")[-1])
    
    def changeX(self, x):
        self.x = x
        self.canvas.move(self.canvasObject, self.x, self.y)
        
    def changeY(self, y):
        self.y = y
        self.canvas.move(self.canvasObject, self.x, self.y)
        
    def changeWidth(self, width):
        self.width = width
        image = img.open(self.unedited)
        image = image.resize((int(self.width*self.scale), int(self.height*self.scale)))
        image.save(self.edited)
        self.file = tk.PhotoImage(file = self.edited)
        
    def changeHeight(self, height):
        self.height = height
        image = img.open(self.unedited)
        image = image.resize((int(self.width*self.scale), int(self.height*self.scale)))
        image.save(self.edited)
        self.file = tk.PhotoImage(file = self.edited)
        
    def changeScale(self, scale):
        self.scale = scale
        image = img.open(self.unedited)
        image = image.resize((int(self.width*self.scale), int(self.height*self.scale)))
        image.save(self.edited)
        self.file = tk.PhotoImage(file = self.edited)    
    
    def createCanvasImage(self):
        self.canvasObject = self.canvas.create_image((self.x, self.y), anchor='nw', image=self.file)
        
    def delete(self):
        self.canvas.delete(self.canvasObject)
        os.remove(self.unedited)
        os.remove(self.edited)
        
class Ellipse:
    def __init__(self, id, canvas, x=0, y=0, width=75, height=75, color="#9c9c9c", name="", scale=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.id = id
        self.canvas = canvas
        self.scale = 1
        self.type = "ellipse"
        if name != "":
            self.name = name
        else:
            self.name = "ellipse_" + str(id)
        self.code = []
    
    def changeName(self, name, objects):
        if name not in objects.keys():
            self.name = name
        
    def changeX(self, x):
        self.canvas.move(self.canvasObject, x - self.x, 0)
        self.x = x
    
    def changeY(self, y):
        self.canvas.move(self.canvasObject, 0, y - self.y)
        self.y = y
    
    def changeScale(self, scale):
        self.scale = scale
        self.width = self.width*self.scale
        self.height = self.height*self.scale
    
    def changeWidth(self, width):
        self.width = width
        
    def changeHeight(self, height):
        self.height = height
    
    def changeColor(self, color):
        self.color = color
        self.canvas.itemconfig(self.canvasObject, fill=self.color)
    
    def createCanvasObject(self):
        self.canvasObject = self.canvas.create_oval(self.x, self.y, self.x+self.width, self.y+self.height, fill=self.color)
        
    def updateObject(self):
        self.canvas.delete(self.canvasObject)
        self.canvasObject = self.canvas.create_oval(self.x, self.y, self.x+self.width, self.y+self.height, fill=self.color)
        
    def delete(self):
        self.canvas.delete(self.canvasObject)
        
class Rectangle:
    def __init__(self, id, canvas, x=0, y=0, width=75, height=75, color="#9c9c9c", name="", scale=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.id = id
        self.canvas = canvas
        self.scale = 1
        self.type = "rectangle"
        if name != "":
            self.name = name
        else:
            self.name = "rectangle_" + str(id)
        self.code = []
    
    def changeName(self, name, objects):
        if name not in objects.keys():
            self.name = name
        
    def changeX(self, x):
        self.canvas.move(self.canvasObject, x - self.x, 0)
        self.x = x
    
    def changeY(self, y):
        self.canvas.move(self.canvasObject, 0, y - self.y)
        self.y = y
    
    def changeScale(self, scale):
        self.scale = scale
        self.width = self.width*self.scale
        self.height = self.height*self.scale
    
    def changeWidth(self, width):
        self.width = width
        
    def changeHeight(self, height):
        self.height = height
    
    def changeColor(self, color):
        self.color = color
        self.canvas.itemconfig(self.canvasObject, fill=self.color)
    
    def createCanvasObject(self):
        self.canvasObject = self.canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill=self.color)
        
    def updateObject(self):
        self.canvas.delete(self.canvasObject)
        self.canvasObject = self.canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill=self.color)
        
    def delete(self):
        self.canvas.delete(self.canvasObject)
        
class Line:
    def __init__(self, id, canvas, x=0, y=0, width=75, height=75, color="#9c9c9c", name="", scale=1, thickness=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.id = id
        self.canvas = canvas
        self.scale = scale
        self.thickness = thickness
        self.type = "line"
        if name != "":
            self.name = name
        else:
            self.name = "line_" + str(id)
        self.code = []
    
    def changeName(self, name, objects):
        if name not in objects.keys():
            self.name = name
        
    def changeX(self, x):
        self.canvas.move(self.canvasObject, x - self.x, 0)
        self.x = x
    
    def changeY(self, y):
        self.canvas.move(self.canvasObject, 0, y - self.y)
        self.y = y
    
    def changeScale(self, scale):
        self.scale = scale
        self.width = self.width*self.scale
        self.height = self.height*self.scale
    
    def changeWidth(self, width):
        self.width = width
        
    def changeHeight(self, height):
        self.height = height
    
    def changeColor(self, color):
        self.color = color
        self.canvas.itemconfig(self.canvasObject, fill=self.color)
    
    def changeThickness(self, thickness):
        self.thickness = thickness
        self.canvas.itemconfig(self.canvasObject, width=self.thickness)
    
    def createCanvasObject(self):
        self.canvasObject = self.canvas.create_line(self.x, self.y, self.x+self.width, self.y+self.height, fill=self.color, width=self.thickness)
        
    def updateObject(self):
        self.canvas.delete(self.canvasObject)
        self.canvasObject = self.canvas.create_line(self.x, self.y, self.x+self.width, self.y+self.height, fill=self.color, width=self.thickness)
        
    def delete(self):
        self.canvas.delete(self.canvasObject)
        
class Text:
    def __init__(self, id, canvas, x=0, y=0, text="Text", 
                 font="Arial", size=12, color="#000000", name=""):
        self.x = x
        self.y = x
        self.color = color
        self.id = id
        self.canvas = canvas
        self.type = "text"
        if name != "":
            self.name = name
        else:
            self.name = "text_" + str(id)
        self.text = text
        self.font = font
        self.size = size
        self.code = []
    
    def changeName(self, name, objects):
        if name not in objects.keys():
            self.name = name
    
    def changeX(self, x):
        self.canvas.move(self.canvasObject, x - self.x, 0)
        self.x = x
    
    def changeY(self, y):
        self.canvas.move(self.canvasObject, 0, y - self.y)
        self.y = y
    
    def changeText(self, text):
        self.text = text
        self.canvas.itemconfig(self.canvasObject, text=self.text)
        
    def changeColor(self, color):
        self.color = color
        self.canvas.itemconfig(self.canvasObject, fill=self.color)
    
    def changeFont(self, font):
        self.font = font
        self.canvas.itemconfig(self.canvasObject, font=(self.font, self.size))
        
    def changeSize(self, size):
        self.size = size
        self.canvas.itemconfig(self.canvasObject, font=(self.font, self.size))
        
    def updateObject(self):
        self.canvas.delete(self.canvasObject)
        self.canvasObject = self.canvas.create_text(self.x, self.y, text=self.text, font=(self.font, self.size), fill=self.color)
    
    def createCanvasObject(self):
        self.canvasObject = self.canvas.create_text(self.x, self.y, text=self.text, font=(self.font, self.size), fill=self.color)
    
    def delete(self):
        self.canvas.delete(self.canvasObject)