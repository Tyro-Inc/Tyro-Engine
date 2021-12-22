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

class Image:
    def __init__(self, id, x, y, scale, rotation, image, canvas):
        self.x = x
        self.y = y
        self.scale = scale
        self.rotation = rotation
        self.id = id
        imageName = image.split("/")[-1]
        imageName = f"{imageName.split('.')[0]}_{self.id}.{imageName.split('.')[1]}"
        self.name = imageName.split('.')[0]
        self.filename = imageName
        shutil.copy(image, f"local/{currentDir}/{imageName}")
        self.image = img.open(f"local/{currentDir}/{imageName}")
        self.width, self.height = self.image.size
        self.image = self.image.resize((self.width*scale, self.height*scale))
        self.image = self.image.rotate(rotation, PIL.Image.NEAREST, expand = 1)
        self.image.save(f"local/{currentDir}/{imageName}")
        self.image = r"local/{currentDir}/{imageName}".format(currentDir = currentDir, imageName = imageName)
        self.file = tk.PhotoImage(file = self.image)
        self.pygameObject = pygame.image.load(image)
        self.pygameObject = pygame.transform.scale(self.pygameObject, (self.width*scale, self.height*scale))
        self.pygameObject = pygame.transform.rotate(self.pygameObject, self.rotation)
        self.canvas = canvas
        
    def changeX(self, x):
        self.x = x
        self.canvas.move(self.canvasObject, self.x, self.y)
        
    def changeY(self, y):
        self.y = y
        self.canvas.move(self.canvasObject, self.x, self.y)
        
    def changeScale(self, scale):
        self.scale = scale
        imagePath = self.image
        image = img.open(imagePath)
        image = image.resize((int(self.width*scale), int(self.height*scale)))
        image.save(imagePath)
        self.pygameObject = pygame.image.load(imagePath)
        self.file = tk.PhotoImage(file = imagePath)
        
    def changeName(self, name, objects):
        if name not in objects.keys():
            self.name = name
            os.rename(self.image, r"local/{currentDir}/{name}.{ext}".format(currentDir = currentDir, name = name, ext = self.image.split("/")[-1].split(".")[-1]))
            self.image = r"local/{currentDir}/{name}.{ext}".format(currentDir = currentDir, name = name, ext = self.image.split("/")[-1].split(".")[-1])
        
    def changeRotation(self, rotation):
        imagePath = self.image
        image = img.open(imagePath)
        image = image.rotate(int((360-self.rotation)+rotation), PIL.Image.NEAREST, expand = 1)
        image.save(imagePath)
        self.pygameObject = pygame.image.load(imagePath)
        self.file = tk.PhotoImage(file = imagePath)
        self.rotation = rotation
        
    def creteCanvsImage(self):
        self.canvasObject = self.canvas.create_image((self.x, self.y), anchor='nw', image=self.file)
        
    def delete(self):
        self.canvas.delete(self.canvasObject)