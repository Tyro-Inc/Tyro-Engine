import tkinter as tk
from tkinter import ttk
from objects import *
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import font
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
        self.color_code = None
        self.font = tk.StringVar()
        self.fonts = list(font.families())
        
        self.font.set("Arial")
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
        
        self.propbutton = tk.Button(self.root, text="Properties", command=self.showPropertiesWindow, font=(self.config['font'], 20), bg=self.config['buttons']['background'])
        self.propbutton.place(x=1212, y=600, width=150, height=40)
        
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
        if GameobjectName != "":
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
        if Gameobject != "":
            Gameobject = self.objects[Gameobject]
            Gameobject.delete()
            Gameobject.tab.destroy()
            del self.objects[Gameobject.name]
            try:
                self.currentObject.set(self.objects[list(self.objects.keys())[0]].name)
            except:
                self.currentObject.set("")
            self.objectSelectMenu['values'] = list(self.objects.keys())
            self.showObjectDetails("")
            print(self.objects)
    
    def showPropertiesWindow(self):
        GameobjectName = self.objectSelectMenu.get()
        if GameobjectName != "":
            Gameobject = self.objects[GameobjectName]
            if Gameobject.type == "image":
                return None
            self.propwindow = tk.Toplevel(self.root)
            self.propwindow.title("Properties")
            self.propwindow.geometry("400x300")
            self.propwindow.resizable(0, 0)
            self.propwindow.config(bg=self.config['editor']['background'])
            self.propwindow.transient(self.root)
            self.propwindow.grab_set()
            self.propwindow.focus_set()
            self.propwinupdatebutton = tk.Button(self.propwindow, text="Update", command=self.propWinUpdateObject, bg=self.config['editor']['background'], font=(self.config['font'], 15))
            self.propwintitle = tk.Label(self.propwindow, text=f"{GameobjectName} Properties", font=(self.config['font'], 20), bg=self.config['editor']['background'], justify=tk.CENTER)
            self.propwintitle.place(x=0, y=30, width=400)
            self.colorPicker = tk.Button(self.propwindow, text="Color", command=self.showColorPicker, bg=self.config['editor']['background'], font=(self.config['font'], 15))
            self.colorPicker.place(x=205, y=75, width=100, height=30)
            if Gameobject.type == "rectangle" or Gameobject.type == "ellipse":
                self.propwinupdatebutton.place(x=125, y=135, width=150, height=40)
            if Gameobject.type == "line":
                self.textthicknesslabel = tk.Label(self.propwindow, text="Thickness", bg=self.config['editor']['background'], font=(self.config['font'], 15))
                self.textthicknesslabel.place(x=82, y=132)
                self.textthickness = tk.Entry(self.propwindow, bg=self.config['editor']['background'], font=(self.config['font'], 15))
                self.textthickness.place(x=220, y=130, width=100, height=30)
                self.textthickness.insert(0, Gameobject.thickness)
                self.propwinupdatebutton.place(x=125, y=185, width=150, height=40)
            if Gameobject.type == "text":
                self.textfontlabel = tk.Label(self.propwindow, text="Font", bg=self.config['editor']['background'], font=(self.config['font'], 15))
                self.textfontlabel.place(x=82, y=132)
                self.textfont = ttk.Combobox(self.propwindow, values=self.fonts, state="readonly", textvariable=self.font, font=(self.config['font'], 15))
                self.textfont.place(x=220, y=130, width=100, height=30)
                self.textsize = tk.Entry(self.propwindow, bg=self.config['editor']['background'], font=(self.config['font'], 15))
                self.textsize.place(x=220, y=170, width=100, height=30)
                self.textsize.insert(0, Gameobject.size)
                self.textsizelabel = tk.Label(self.propwindow, text="Size", bg=self.config['editor']['background'], font=(self.config['font'], 15))
                self.textsizelabel.place(x=82, y=170)
                self.textLabel = tk.Label(self.propwindow, text="Text", bg=self.config['editor']['background'], font=(self.config['font'], 15))
                self.textLabel.place(x=82, y=210)
                self.text = tk.Entry(self.propwindow, bg=self.config['editor']['background'], font=(self.config['font'], 15))
                self.text.place(x=220, y=210, width=100, height=30)
                self.propwinupdatebutton.place(x=125, y=285, width=150, height=40)
            
    
    def showColorPicker(self):
        color_code = colorchooser.askcolor(title ="Choose color")
        self.color_code = color_code[1] if color_code[1] != None else None
    
    def propWinUpdateObject(self):
        Gameobject = self.objects[self.objectSelectMenu.get()]
        if Gameobject.type != "image":
            if self.color_code != None:
                Gameobject.changeColor(self.color_code)
                print(self.color_code)
        if Gameobject.type == "line":
            thickness = self.textthickness.get()
            if thickness != "":
                if thickness.isdigit():
                    if int(thickness) > 0:
                        Gameobject.changeThickness(int(self.textthickness.get()))
        if Gameobject.type == "text":
            font = self.font
            size = self.textsize.get()
            text = self.text.get()
            Gameobject.changeText(text)
            Gameobject.changeFont(font)
            if size != "":
                if size.isdigit():
                    if int(size) > 0:
                        Gameobject.changeSize(int(size))
                
        self.propwindow.destroy()
    
if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()