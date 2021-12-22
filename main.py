import tkinter as tk
from tkinter import ttk
from objects import *
from tkinter import filedialog
from uuid import uuid4
import random

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
        
        # root.configure(background='#264653')
        
        #Initialize the editor frame
        self.editor = tk.Frame(root, width=950, height=620, borderwidth="2", relief="groove")
        self.editor.place(x=20, y=80)
        self.objects = {}
        self.root = root
        
        #Initialize the canvas and IDE
        self.IDE = ttk.Notebook(self.editor)
        self.IDE.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(root, width=400, height=400, borderwidth="2", relief="groove")
        self.canvas.place(x=1000, y=20)
        self.IDE.bind("<<NotebookTabChanged>>", self.showObjectDetails)
        
        #properties variables
        self.propname = tk.StringVar()
        self.propx = tk.StringVar()
        self.propy = tk.StringVar()
        self.propscale = tk.StringVar()
        self.proporigin = tk.StringVar()
        self.propwidth = tk.StringVar()
        self.prophight = tk.StringVar()
        
        self.proporigin.set("nw")
        
        #Initialize the properties section
        self.propnamelabel = tk.Label(self.root, text="Name:", font=("Public Sans", 20))
        self.propnamelabel.place(x=1045, y=432)
        self.propnameinput = tk.Entry(self.root, textvariable=self.propname, font=("Public Sans", 20))
        self.propnameinput.place(x=1165, y=428, width=200, height=40)
        
        self.propxlabel = tk.Label(self.root, text="X:", font=("Public Sans", 20))
        self.propxlabel.place(x=1110, y=490)
        self.propxinput = tk.Entry(self.root, textvariable=self.propx, font=("Public Sans", 20))
        self.propxinput.place(x=1140, y=490, width=60, height=40)
        
        self.propylabel = tk.Label(self.root, text="Y:", font=("Public Sans", 20))
        self.propylabel.place(x=1260, y=490)
        self.propyinput = tk.Entry(self.root, textvariable=self.propy, font=("Public Sans", 20))
        self.propyinput.place(x=1290, y=490, width=60, height=40)
        
        self.propwidthlabel = tk.Label(self.root, text="Width:", font=("Public Sans", 18))
        self.propwidthlabel.place(x=1065, y=540)
        self.propwidthinput = tk.Entry(self.root, textvariable=self.propwidth, font=("Public Sans", 20))
        self.propwidthinput.place(x=1140, y=540, width=60, height=40)
        
        self.propheightlabel = tk.Label(self.root, text="Height:", font=("Public Sans", 18))
        self.propheightlabel.place(x=1205, y=540)
        self.propheightinput = tk.Entry(self.root, textvariable=self.prophight, font=("Public Sans", 20))
        self.propheightinput.place(x=1290, y=540, width=60, height=40)
        
        self.propscalelabel = tk.Label(self.root, text="Scale:", font=("Public Sans", 18))
        self.propscalelabel.place(x=1070, y=600)
        self.propscaleinput = tk.Entry(self.root, textvariable=self.propscale, font=("Public Sans", 20))
        self.propscaleinput.place(x=1140, y=600, width=60, height=40)
        
        self.proporiginlabel = tk.Label(self.root, text="Origin:", font=("Public Sans", 18))
        self.proporiginlabel.place(x=1205, y=600)
        self.proporigininput = tk.OptionMenu(self.root, self.proporigin, "nw", "n", "ne", "e", "se", "s", "sw", "w")
        self.proporigininput.place(x=1290, y=600, width=60, height=40)
        
        self.propupdatebutton = tk.Button(self.root, text="Update", font=("Public Sans", 20), command=self.updateObject)
        self.propupdatebutton.place(x=1050, y=650, width=150, height=40)
        
        self.propdeletebutton = tk.Button(self.root, text="Delete", font=("Public Sans", 20), command=self.deleteObject)
        self.propdeletebutton.place(x=1212, y=650, width=150, height=40)
        
        #Initialize the Menu bar
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Add Object", menu=self.filemenu)
        self.filemenu.add_command(label="Image", command=self.addImage)
        # self.filemenu.add_command(label="Square", command=self.addSquare)
        # self.filemenu.add_command(label="Oval", command=self.addOval)
        # self.filemenu.add_command(label="Triangle", command=self.addTriangle)
    
    def create_tab(self, objects):
        tab = tk.Frame(self.IDE)
        tab.pack(fill="both", expand=True)
        writingarea = tk.Text(tab, width=120, height=40)
        writingarea.pack(fill="both", expand=True)
        return tab
    
    def addImage(self):
        image = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("png files","*.png"),("all files","*.*")))
        ID = str(random.randint(1000, 10000))
        imgname = image.split("/")[-1]
        imgname = f"{imgname.split('.')[0]}_{ID}.{imgname.split('.')[1]}"
        self.objects[imgname] = Image(ID, 0, 0, 1, 0, image, self.canvas)
        self.root.image = self.objects[imgname].file
        self.objects[imgname].creteCanvsImage()
        self.IDE.add(self.create_tab(imgname), text=imgname)
        
    def showObjectDetails(self, arg):
        try:
            Gameobject = self.IDE.tab(self.IDE.select(), "text")
            Gameobject = self.objects[Gameobject]
            self.propname.set(Gameobject.name)
            self.propx.set(Gameobject.x)
            self.propy.set(Gameobject.y)
            self.propscale.set(Gameobject.scale)
            self.proprotation.set(Gameobject.rotation)
        except:
            self.propname.set("")
            self.propx.set("")
            self.propy.set("")
            self.propscale.set("")
            self.proprotation.set("")

    def updateObject(self):
        GameobjectName = self.IDE.tab(self.IDE.select(), "text")
        Gameobject = self.objects[GameobjectName]
        Gameobject.changeScale(float(self.propscale.get()))
        Gameobject.changeX(float(self.propx.get()))
        Gameobject.changeY(float(self.propy.get()))
        Gameobject.changeName(self.propname.get(), self.objects)
        Gameobject.changeRotation(float(self.proprotation.get()))
        self.root.image = Gameobject.file
        Gameobject.creteCanvsImage()
        self.IDE.tab(self.IDE.select(), text=Gameobject.name)
        del self.objects[GameobjectName]
        self.objects[Gameobject.name] = Gameobject
        
    def addSquare(self):
        ID = str(random.randint(1000, 10000))
        self.objects[ID] = Square(ID, 0, 0, 1, 0, self.canvas)
        self.IDE.add(self.create_tab(ID), text=ID)
        
    def addOval(self):
        ID = str(random.randint(1000, 10000))
        self.objects[ID] = Oval(ID, 0, 0, 1, 0, self.canvas)
        self.IDE.add(self.create_tab(ID), text=ID)
        
    def addTriangle(self):
        ID = str(random.randint(1000, 10000))
        self.objects[ID] = Triangle(ID, 0, 0, 1, 0, self.canvas)
        self.IDE.add(self.create_tab(ID), text=ID)
    
    def deleteObject(self):
        print(self.objects)
        Gameobject = self.IDE.tab(self.IDE.select(), "text")
        Gameobject = self.objects[Gameobject]
        Gameobject.delete()
        self.IDE.forget(self.IDE.select())
        del self.objects[Gameobject.filename]
        print(self.objects)
        
        
if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()