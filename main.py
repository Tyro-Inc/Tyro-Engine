import tkinter as tk
from tkinter import ttk
from objects import *
from tkinter import filedialog
from uuid import uuid4
import random
import json

class App:
    def __init__(self, root):
        #Initialize the root window
        root.title("Tyro Engine")
        width=1440
        height=724
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        self.config = json.load(open("config.json"))
        
        root.configure(background=self.config['background'])
        
        #Initialize the editor frame
        self.editor = tk.Frame(root, width=950, height=620, borderwidth="2", relief="groove", bg=self.config['editor']['background'])
        self.editor.place(x=20, y=80)
        self.objects = {}
        self.root = root
        
        #initialize the canvas
        self.canvas = tk.Canvas(root, width=400, height=400, borderwidth="2", relief="groove")
        self.canvas.place(x=1000, y=20)
        
        #properties variables
        self.propname = tk.StringVar()
        self.propx = tk.StringVar()
        self.propy = tk.StringVar()
        self.propscale = tk.StringVar()
        self.propwidth = tk.StringVar()
        self.propheight = tk.StringVar()
        self.title = tk.StringVar()
        self.currentObject = tk.StringVar()
        
        self.title.set("Untitled")
        
        #Initialize the Top Bar
        self.titleInput = tk.Entry(root, textvariable=self.title, font=(self.config['font'], 20))
        self.titleInput.place(x=225, y=25, width=320, height=35)
        self.objectSelectMenu = ttk.Combobox(root, textvariable=self.currentObject, state="readonly")
        self.objectSelectMenu['values'] = list(self.objects.keys())
        self.objectSelectMenu.place(x=20, y=25, width=200, height=35)    
        self.objectSelectMenu.bind("<<ComboboxSelected>>", self.showObjectDetails)
        
        #Initialize the properties section
        self.propnamelabel = tk.Label(self.root, text="Name:", font=(self.config['font'], 20), bg=self.config['label']['background'])
        self.propnamelabel.place(x=1045, y=432)
        self.propnameinput = tk.Entry(self.root, textvariable=self.propname, font=(self.config['font'], 20), bg=self.config['input']['background'])
        self.propnameinput.place(x=1165, y=432, width=200, height=40)
        
        self.propxlabel = tk.Label(self.root, text="X:", font=(self.config['font'], 20), bg=self.config['label']['background'])
        self.propxlabel.place(x=1110, y=490)
        self.propxinput = tk.Entry(self.root, textvariable=self.propx, font=(self.config['font'], 20), bg=self.config['input']['background'])
        self.propxinput.place(x=1140, y=490, width=60, height=40)
        
        self.propylabel = tk.Label(self.root, text="Y:", font=(self.config['font'], 20), bg=self.config['label']['background'])
        self.propylabel.place(x=1260, y=490)
        self.propyinput = tk.Entry(self.root, textvariable=self.propy, font=(self.config['font'], 20), bg=self.config['input']['background'])
        self.propyinput.place(x=1290, y=490, width=60, height=40)
        
        self.propwidthlabel = tk.Label(self.root, text="Width:", font=(self.config['font'], 18), bg=self.config['label']['background'])
        self.propwidthlabel.place(x=1060, y=540)
        self.propwidthinput = tk.Entry(self.root, textvariable=self.propwidth, font=(self.config['font'], 20), bg=self.config['input']['background'])
        self.propwidthinput.place(x=1140, y=540, width=60, height=40)
        
        self.propheightlabel = tk.Label(self.root, text="Height:", font=(self.config['font'], 18), bg=self.config['label']['background'])
        self.propheightlabel.place(x=1205, y=540)
        self.propheightinput = tk.Entry(self.root, textvariable=self.propheight, font=(self.config['font'], 20), bg=self.config['input']['background'])
        self.propheightinput.place(x=1290, y=540, width=60, height=40)
        
        self.propscalelabel = tk.Label(self.root, text="Scale:", font=(self.config['font'], 18), bg=self.config['label']['background'])
        self.propscalelabel.place(x=1070, y=600)
        self.propscaleinput = tk.Entry(self.root, textvariable=self.propscale, font=(self.config['font'], 20), bg=self.config['input']['background'])
        self.propscaleinput.place(x=1140, y=600, width=60, height=40)
        
        self.propupdatebutton = tk.Button(self.root, text="Update", font=(self.config['font'], 20), command=self.updateObject, bg=self.config['buttons']['background'])
        self.propupdatebutton.place(x=1050, y=650, width=150, height=40)
        
        self.propdeletebutton = tk.Button(self.root, text="Delete", font=(self.config['font'], 20), command=self.deleteObject, bg=self.config['buttons']['background'])
        self.propdeletebutton.place(x=1212, y=650, width=150, height=40)
        
        #Initialize the Menu bar
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Add Object", menu=self.filemenu)
        self.filemenu.add_command(label="Image", command=self.addImage)
        self.filemenu.add_command(label="Rectangle", command=self.addRectangle)
        self.filemenu.add_command(label="Ellipse", command=self.addEllipse)
        self.filemenu.add_command(label="Line", command=self.addLine)
        self.filemenu.add_command(label="Text", command=self.addText)
    
    def create_tab(self, name):
        tab = tk.Frame(self.root)
        tab.place(x=20, y=80, width=950, height=620)
        writingarea = tk.Text(tab, width=60, height=17, font=(self.config['font'], 20), bg=self.config['editor']['background'])
        writingarea.pack(fill="both", expand=True)
        self.objectSelectMenu['values'] = list(self.objects.keys())
        self.currentObject.set(name)
        self.showObjectDetails("")
        return tab
    
        
    def showObjectDetails(self, arg):
        try:
            Gameobject = self.objectSelectMenu.get()
            Gameobject = self.objects[Gameobject]
            self.propname.set(Gameobject.name)
            self.propx.set(Gameobject.x)
            self.propy.set(Gameobject.y)
            if Gameobject.type != "text":
                self.propscale.set(Gameobject.scale)
                self.propwidth.set(Gameobject.width)
                self.propheight.set(Gameobject.height)
            else:
                self.propscale.set("")
                self.propwidth.set("")
                self.propheight.set("")
        except Exception as e:
            self.propname.set("")
            self.propx.set("")
            self.propy.set("")
            self.propscale.set("")
            self.propwidth.set("")
            self.propheight.set("")
        try:
            self.objects[Gameobject.name].tab.lift()
        except:
            pass

    def updateObject(self):
        GameobjectName = self.objectSelectMenu.get()
        Gameobject = self.objects[GameobjectName]
        Gameobject.changeX(float(self.propx.get()))
        Gameobject.changeY(float(self.propy.get()))
        if Gameobject.type != "text":
            Gameobject.changeWidth(float(self.propwidth.get()))
            Gameobject.changeHeight(float(self.propheight.get()))
            Gameobject.changeScale(float(self.propscale.get()))
        Gameobject.changeName(self.propname.get(), self.objects)
        if Gameobject.type == "image":
            self.root.image = Gameobject.file
            Gameobject.createCanvasImage()
        else:
            Gameobject.updateObject()
        del self.objects[GameobjectName]
        self.objects[Gameobject.name] = Gameobject
        self.objectSelectMenu['values'] = list(self.objects.keys())
        self.currentObject.set(Gameobject.name)
        
    def addImage(self):
        image = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("png files","*.png"),("all files","*.*")))
        ID = str(random.randint(1000, 10000))
        imgname = image.split("/")[-1]
        imgname = f"{imgname.split('.')[0]}_{ID}"
        self.objects[imgname] = Image(ID, image, self.canvas)
        self.root.image = self.objects[imgname].file
        self.objects[imgname].createCanvasImage()
        self.objects[imgname].tab = self.create_tab(imgname)
        print(self.objects)
        
    def addRectangle(self):
        ID = str(random.randint(1000, 10000))
        self.objects["rectangle_" + str(ID)] = Rectangle(ID, self.canvas)
        self.objects["rectangle_" + str(ID)].createCanvasObject()
        self.objects["rectangle_" + str(ID)].tab = self.create_tab("rectangle_" + str(ID))
        
    def addEllipse(self):
        ID = str(random.randint(1000, 10000))
        self.objects["ellipse_" + str(ID)] = Ellipse(ID, self.canvas)
        self.objects["ellipse_" + str(ID)].createCanvasObject()
        self.objects["ellipse_" + str(ID)].tab = self.create_tab("ellipse_" + str(ID))
        
    def addLine(self):
        ID = str(random.randint(1000, 10000))
        self.objects["line_" + str(ID)] = Line(ID, self.canvas)
        self.objects["line_" + str(ID)].createCanvasObject()
        self.objects["line_" + str(ID)].tab = self.create_tab("line_" + str(ID))
    
    def addText(self):
        ID = str(random.randint(1000, 10000))
        self.objects["text_" + str(ID)] = Text(ID, self.canvas)
        self.objects["text_" + str(ID)].createCanvasObject()
        self.objects["text_" + str(ID)].tab = self.create_tab("text_" + str(ID))
    
    def deleteObject(self):
        print(self.objects)
        Gameobject = self.objectSelectMenu.get()
        Gameobject = self.objects[Gameobject]
        Gameobject.delete()
        Gameobject.tab.destroy()
        del self.objects[Gameobject.name]
        try:
            self.currentObject.set(self.objects[list(self.objects.keys())[0]].name)
        except:
            self.currentObject.set("")
        self.showObjectDetails("")
        print(self.objects)
        
        
if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()