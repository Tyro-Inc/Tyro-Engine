import pygame
from random import randint as random
from time import sleep as delay
import keyboard
WIDTH = 400
HEIGHT = 400
FPS = 60
WHITE = (255, 255, 255)


class Object:
    def __init__(self, **kwargs):
        args = kwargs
        args.pop("canvas")
        args.pop('canvasObject')
        self.__dict__.update(args)
        if self.type != "text":
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.__screen = self.screen
        self.screen = None
        
    def __repr__(self):
        return str(self.__dict__)

    def move_x(self, x):
        self.x += x

    def move_y(self, y):
        self.y += y

    def change_Width(self, w):
        if self.type != "text":
            self.width = w
        else:
            raise Exception("Can't change width of text")

    def change_Height(self, h):
        if self.type != "text":
            self.height = h
        else:
            raise Exception("Can't change height of text")

    def change_Color(self, color):
        if self.type != "image":
            self.color = color
        else:
            raise Exception("Can't change color of image")

    def change_Thickness(self, thickness):
        if self.type == "line":
            self.thickness = thickness
        else:
            raise Exception("Can't change thickness of non-line")

    def change_Text(self, text):
        if self.type == "text":
            self.text = text
        else:
            raise Exception("Can't change text of non-text")

    def change_Scale(self, scale):
        if self.type != "text":
            self.scale = scale
        else:
            raise Exception("Can't change scale of text")

    def goto(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        if self.type != "text":
            self.rect = pygame.Rect(
                self.x, self.y, self.width * self.scale, self.height * self.scale
            )
            if self.type == "rectangle":
                self.obj = pygame.draw.rect(self.__screen, self.color, self.rect)
            elif self.type == "ellipse":
                self.obj = pygame.draw.ellipse(self.__screen, self.color, self.rect)
            elif self.type == "line":
                self.obj = pygame.draw.line(
                    self.__screen,
                    self.color,
                    (int(self.x), int(self.y)),
                    (
                        int((self.x + self.width) * self.scale),
                        int((self.y + self.height) * self.scale),
                    ),
                    int(self.thickness * self.scale),
                )
            elif self.type == "image":
                self.obj = pygame.image.load(self.path)
                self.obj = pygame.transform.scale(
                    self.obj, (self.width * self.scale, self.height * self.scale)
                )
                self.__screen.blit(self.obj, (self.x, self.y))
        else:
            self.font_ = pygame.font.SysFont(self.font, self.size)
            text = self.font_.render(self.text, True, self.color)
            rect = text.get_rect()
            rect.center = (self.x, self.y)
            self.__screen.blit(text, rect)


def isKey(key):
    return keyboard.is_pressed(key)


def isColliding(obj1, obj2):
    return obj1.rect.colliderect(obj2.rect)

def mousePos():
    return list(pygame.mouse.get_pos())

glob = {"isKey": isKey, "isColliding": isColliding, "random": random, 
        "delay": delay, "mousePos": mousePos}

def run(objects, code):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tyro Game Engine Preview")
    clock = pygame.time.Clock()
    running = True
    init = True
    
    
    for obj in objects.keys():
        objects[obj].screen = screen
        exec(f"{obj} = Object(**objects[obj].__dict__)")
    objects = list(objects.keys())
    
    global glob
    for i in dir():
        exec(f"glob['{i}'] = {i}") if i not in ["clock", "obj", "screen", "code", 
                                            "objects", "objs", "running"] else None
    print(glob.keys())
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(WHITE)
        if not init:
            glob['init'] = False
        exec(code, glob)
        if init:
            init = False
        for obj in objects:
            exec(f"{obj}.update()")
        pygame.display.flip()
    pygame.quit()

