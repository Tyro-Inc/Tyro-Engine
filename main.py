import tkinter as tk
from tkinter import ttk
from objects import *
from tkinter import filedialog, colorchooser, font, messagebox
from tkinter.messagebox import askyesno
import random
import json
import shutil
from time import sleep
import sys, os
from interpreter import run, close

path = None


class ProjectManager:
    def __init__(self, root):
        root.title("Project Manager | Tyro Engine")
        width = 1000
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        self.path = None
        self.config = json.load(open("config.json"))
        root.configure(background=self.config["background"])
        self.root = root
        self.projects = json.load(open("projects.json"))
        self.projects = [f"{i['name']} |/| {i['path']}" for i in self.projects]
        self.titleLabel = tk.Label(
            root,
            text="Tyro Engine",
            font=(self.config["font"], 72),
            bg=self.config["label"]["background"],
        )
        self.titleLabel.place(x=0, y=0, width=1000, height=120)
        self.descriptionLabel = tk.Label(
            root,
            text="The Place to start your game dev journey",
            font=(self.config["font"], 24),
            bg=self.config["label"]["background"],
        )
        self.descriptionLabel.place(x=0, y=120, width=1000, height=40)
        self.newProjectButton = tk.Button(
            root,
            text="Start New Project",
            font=(self.config["font"], 12),
            command=self.newproject,
            bg=self.config["buttons"]["background"],
        )
        self.newProjectButton.place(x=276, y=200, width=161, height=25)
        self.newProjectName = tk.StringVar()
        self.newProjectName.set("New Project")
        self.newProjectNameEntry = tk.Entry(
            root,
            textvariable=self.newProjectName,
            font=(self.config["font"], 12),
            bg=self.config["input"]["background"],
        )
        self.newProjectNameEntry.place(x=445, y=200, width=460, height=25)
        self.openProjectButton = tk.Button(
            root,
            text="Open Project",
            font=(self.config["font"], 12),
            bg=self.config["buttons"]["background"],
            command=self.openProject,
        )
        self.openProjectButton.place(x=90, y=200, width=161, height=25)
        self.projectList = tk.Listbox(
            root,
            font=(self.config["font"], 12),
            bg=self.config["buttons"]["background"],
        )
        self.projectList.place(x=55, y=245, width=890, height=200)
        self.projectList.insert(tk.END, *self.projects)

    def newproject(self):
        directory = filedialog.askdirectory(
            initialdir="/",
            title="Select directory",
            mustexist=True,
        )
        if directory != "":
            global path
            os.mkdir(directory + "/" + self.newProjectName.get())
            path = directory + "/" + self.newProjectName.get()
            self.path = path
            os.mkdir(path + "/assets")
            os.mkdir(path + "/assets/edited")
            project = {"name": self.newProjectName.get(), "objects": []}
            json.dump(project, open(path + "/project.tyro", "w"))
            proj = {"name": self.newProjectName.get(), "path": path}

            projs = json.load(open("projects.json"))
            projs.append(proj)
            json.dump(projs, open("projects.json", "w"))
            open(path + "/main.ty", "w").close()

            root.destroy()

    def openProject(self):
        proj = self.projectList.get(self.projectList.curselection())
        self.path = proj.split(" |/| ")[1]
        if os.path.isdir(self.path):
            root.destroy()


class App:
    def __init__(self, root, path):
        # Initialize the root window
        root.title("Tyro Engine")
        width = 1440
        height = 724
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        self.path = path

        self.config = json.load(open("config.json"))

        root.configure(background=self.config["background"])

        # Initialize the editor frame
        self.editor = tk.Frame(
            root,
            width=950,
            height=620,
            borderwidth="2",
            relief="groove",
            bg=self.config["editor"]["background"],
        )
        self.editor.place(x=20, y=80)
        self.objects = {}
        self.root = root

        # initialize the canvas
        self.canvas = tk.Canvas(
            root, width=400, height=400, borderwidth="2", relief="groove"
        )
        self.canvas.place(x=1000, y=20)

        # properties variables
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

        # Initialize the Top Bar
        self.titleInput = tk.Entry(
            root, textvariable=self.title, font=(self.config["font"], 20)
        )
        self.titleInput.place(x=225, y=25, width=320, height=35)
        self.objectSelectMenu = ttk.Combobox(
            root, textvariable=self.currentObject, state="readonly"
        )
        self.objectSelectMenu["values"] = list(self.objects.keys())
        self.objectSelectMenu.place(x=20, y=25, width=200, height=35)
        self.objectSelectMenu.bind("<<ComboboxSelected>>", self.showObjectDetails)

        self.runButton = tk.Button(
            self.root,
            text="Run",
            font=(self.config["font"], 20),
            bg=self.config["buttons"]["background"],
            command=self.execute,
        )
        self.runButton.place(x=580, y=25, width=135, height=35)

        # Initialize the properties section
        self.propnamelabel = tk.Label(
            self.root,
            text="Name:",
            font=(self.config["font"], 20),
            bg=self.config["label"]["background"],
        )
        self.propnamelabel.place(x=1045, y=432)
        self.propnameinput = tk.Entry(
            self.root,
            textvariable=self.propname,
            font=(self.config["font"], 20),
            bg=self.config["input"]["background"],
        )
        self.propnameinput.place(x=1165, y=432, width=200, height=40)

        self.propxlabel = tk.Label(
            self.root,
            text="X:",
            font=(self.config["font"], 20),
            bg=self.config["label"]["background"],
        )
        self.propxlabel.place(x=1110, y=490)
        self.propxinput = tk.Entry(
            self.root,
            textvariable=self.propx,
            font=(self.config["font"], 20),
            bg=self.config["input"]["background"],
        )
        self.propxinput.place(x=1140, y=490, width=60, height=40)

        self.propylabel = tk.Label(
            self.root,
            text="Y:",
            font=(self.config["font"], 20),
            bg=self.config["label"]["background"],
        )
        self.propylabel.place(x=1260, y=490)
        self.propyinput = tk.Entry(
            self.root,
            textvariable=self.propy,
            font=(self.config["font"], 20),
            bg=self.config["input"]["background"],
        )
        self.propyinput.place(x=1290, y=490, width=60, height=40)

        self.propwidthlabel = tk.Label(
            self.root,
            text="Width:",
            font=(self.config["font"], 18),
            bg=self.config["label"]["background"],
        )
        self.propwidthlabel.place(x=1060, y=540)
        self.propwidthinput = tk.Entry(
            self.root,
            textvariable=self.propwidth,
            font=(self.config["font"], 20),
            bg=self.config["input"]["background"],
        )
        self.propwidthinput.place(x=1140, y=540, width=60, height=40)

        self.propheightlabel = tk.Label(
            self.root,
            text="Height:",
            font=(self.config["font"], 18),
            bg=self.config["label"]["background"],
        )
        self.propheightlabel.place(x=1205, y=540)
        self.propheightinput = tk.Entry(
            self.root,
            textvariable=self.propheight,
            font=(self.config["font"], 20),
            bg=self.config["input"]["background"],
        )
        self.propheightinput.place(x=1290, y=540, width=60, height=40)

        self.propscalelabel = tk.Label(
            self.root,
            text="Scale:",
            font=(self.config["font"], 18),
            bg=self.config["label"]["background"],
        )
        self.propscalelabel.place(x=1070, y=600)
        self.propscaleinput = tk.Entry(
            self.root,
            textvariable=self.propscale,
            font=(self.config["font"], 20),
            bg=self.config["input"]["background"],
        )
        self.propscaleinput.place(x=1140, y=600, width=60, height=40)

        self.propbutton = tk.Button(
            self.root,
            text="Properties",
            command=self.showPropertiesWindow,
            font=(self.config["font"], 20),
            bg=self.config["buttons"]["background"],
        )
        self.propbutton.place(x=1212, y=600, width=150, height=40)

        self.propupdatebutton = tk.Button(
            self.root,
            text="Update",
            font=(self.config["font"], 20),
            command=self.updateObject,
            bg=self.config["buttons"]["background"],
        )
        self.propupdatebutton.place(x=1050, y=650, width=150, height=40)

        self.propdeletebutton = tk.Button(
            self.root,
            text="Delete",
            font=(self.config["font"], 20),
            command=self.deleteObject,
            bg=self.config["buttons"]["background"],
        )
        self.propdeletebutton.place(x=1212, y=650, width=150, height=40)

        # Initialize the Menu bar
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        self.addobjectmenu = tk.Menu(self.menu)
        self.filemenu = tk.Menu(self.menu)

        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.menu.add_cascade(label="Add Object", menu=self.addobjectmenu)

        self.filemenu.add_command(label="Open", command=self.loadProject)
        self.filemenu.add_command(label="Save", command=self.saveProject)
        self.addobjectmenu.add_command(label="Image", command=self.addImage)
        self.addobjectmenu.add_command(label="Rectangle", command=self.addRectangle)
        self.addobjectmenu.add_command(label="Ellipse", command=self.addEllipse)
        self.addobjectmenu.add_command(label="Line", command=self.addLine)
        self.addobjectmenu.add_command(label="Text", command=self.addText)

    def execute(self):
        try:
            self.saveProject()
            code = open(self.path + "/code.ty", "r").read()
            run(self.objects, code)
            close()
        except Exception as e:
            messagebox.showerror(
                message=f"Error during execution, \nError: {e}",
                title="Error",
            )
            close()

    def create_tab(self):
        """
        Creates a new tk.Text Object and appends it to the object
        """
        tab = tk.Text(
            self.root,
            width=950,
            height=620,
            font=("consolas", 20),
            bg=self.config["editor"]["background"],
        )
        tab.place(x=20, y=80, width=950, height=620)
        return tab

    def newObject(self, name):
        self.currentObject.set(name)
        self.objectSelectMenu["values"] = list(self.objects.keys())
        self.showObjectDetails("")

    def showObjectDetails(self, arg):
        """
        Shows the details of the selected object.
        different properties are shown depending on the object type
        """
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

    def updateObject(self):
        """
        Takes the properties from the inputs of properties window and updates the selected object
        the previous object is deleted and then added again with the new properties
        """
        GameobjectName = self.objectSelectMenu.get()
        if GameobjectName != "":
            Gameobject = self.objects[GameobjectName]
            Gameobject.changeX(float(self.propx.get()))
            Gameobject.changeY(float(self.propy.get()))
            if Gameobject.type != "text":
                Gameobject.changeWidth(float(self.propwidth.get()))
                Gameobject.changeHeight(float(self.propheight.get()))
                Gameobject.changeScale(float(self.propscale.get()))
            Gameobject.changeName(self.propname.get().replace(" ", ""), self.objects)
            if Gameobject.type == "image":
                self.root.image = Gameobject.file
                Gameobject.createCanvasImage()
            else:
                Gameobject.updateObject()
            del self.objects[GameobjectName]
            self.objects[Gameobject.name] = Gameobject
            self.objectSelectMenu["values"] = list(self.objects.keys())
            self.currentObject.set(Gameobject.name)

    def addImage(self):
        """
        Ask the user to select an image and then adds it to the project
        also adds the image to the objectSelectMenu and creates a new tab for the image
        """
        image = filedialog.askopenfilename(
            initialdir="/",
            title="Select file",
            filetypes=(("png files", "*.png"), ("all files", "*.*")),
        )
        if image != "":
            ID = str(random.randint(1000, 10000))
            imgname = image.split("/")[-1]
            imgname = f"{imgname.split('.')[0]}_{ID}"
            self.objects[imgname] = Image(ID, image, self.canvas, path=self.path)
            self.root.image = self.objects[imgname].file
            self.objects[imgname].createCanvasImage()
            self.newObject(imgname)

    def addRectangle(self):
        """
        Creates a new rectangle object and adds it to the project
        also adds the Rectangle to the objectSelectMenu and creates a new tab for the Rectangle
        """
        ID = str(random.randint(1000, 10000))
        self.objects["rectangle_" + str(ID)] = Rectangle(ID, self.canvas)
        self.objects["rectangle_" + str(ID)].createCanvasObject()
        self.newObject("rectangle_" + str(ID))

    def addEllipse(self):
        """
        Creates a new Ellipse object and adds it to the project
        also adds the Ellipse to the objectSelectMenu and creates a new tab for the Ellipse
        """
        ID = str(random.randint(1000, 10000))
        self.objects["ellipse_" + str(ID)] = Ellipse(ID, self.canvas)
        self.objects["ellipse_" + str(ID)].createCanvasObject()
        self.newObject("ellipse_" + str(ID))

    def addLine(self):
        """
        Creates a new Line object and adds it to the project
        also adds the Line to the objectSelectMenu and creates a new tab for the Line
        """
        ID = str(random.randint(1000, 10000))
        self.objects["line_" + str(ID)] = Line(ID, self.canvas)
        self.objects["line_" + str(ID)].createCanvasObject()
        self.newObject("line_" + str(ID))

    def addText(self):
        """
        Creates a new Text object and adds it to the project
        also adds the Text to the objectSelectMenu and creates a new tab for the Text
        """
        ID = str(random.randint(1000, 10000))
        self.objects["text_" + str(ID)] = Text(ID, self.canvas)
        self.objects["text_" + str(ID)].createCanvasObject()
        self.newObject("text_" + str(ID))

    def deleteObject(self):
        """
        Removes the selected object from self.objects and deletes the tab
        """
        Gameobject = self.objectSelectMenu.get()
        if Gameobject != "":
            Gameobject = self.objects[Gameobject]
            Gameobject.delete()
            del self.objects[Gameobject.name]
            try:
                self.currentObject.set(self.objects[list(self.objects.keys())[0]].name)
            except:
                self.currentObject.set("")
            self.objectSelectMenu["values"] = list(self.objects.keys())
            self.showObjectDetails("")

    def showPropertiesWindow(self):
        """
        Opens a Toplevel window for showing extra properties of the selected object
        different properties are shown depending on the object type
        """
        GameobjectName = self.objectSelectMenu.get()
        if GameobjectName != "":
            Gameobject = self.objects[GameobjectName]
            if Gameobject.type == "image":
                return None
            self.propwindow = tk.Toplevel(self.root)
            self.propwindow.title("Properties")
            self.propwindow.geometry("400x300")
            self.propwindow.resizable(0, 0)
            self.propwindow.config(bg=self.config["editor"]["background"])
            self.propwindow.transient(self.root)
            self.propwindow.grab_set()
            self.propwindow.focus_set()
            self.propwinupdatebutton = tk.Button(
                self.propwindow,
                text="Update",
                command=self.propWinUpdateObject,
                bg=self.config["editor"]["background"],
                font=(self.config["font"], 15),
            )
            self.propwintitle = tk.Label(
                self.propwindow,
                text=f"{GameobjectName} Properties",
                font=(self.config["font"], 20),
                bg=self.config["editor"]["background"],
                justify=tk.CENTER,
            )
            self.propwintitle.place(x=0, y=30, width=400)
            self.colorPicker = tk.Button(
                self.propwindow,
                text="Color",
                command=self.showColorPicker,
                bg=self.config["editor"]["background"],
                font=(self.config["font"], 15),
            )
            self.colorPicker.place(x=205, y=75, width=100, height=30)
            if Gameobject.type == "rectangle" or Gameobject.type == "ellipse":
                self.propwinupdatebutton.place(x=125, y=135, width=150, height=40)
            if Gameobject.type == "line":
                self.textthicknesslabel = tk.Label(
                    self.propwindow,
                    text="Thickness",
                    bg=self.config["editor"]["background"],
                    font=(self.config["font"], 15),
                )
                self.textthicknesslabel.place(x=82, y=132)
                self.textthickness = tk.Entry(
                    self.propwindow,
                    bg=self.config["editor"]["background"],
                    font=(self.config["font"], 15),
                )
                self.textthickness.place(x=220, y=130, width=100, height=30)
                self.textthickness.insert(0, Gameobject.thickness)
                self.propwinupdatebutton.place(x=125, y=185, width=150, height=40)
            if Gameobject.type == "text":
                self.textfontlabel = tk.Label(
                    self.propwindow,
                    text="Font",
                    bg=self.config["editor"]["background"],
                    font=(self.config["font"], 15),
                )
                self.textfontlabel.place(x=82, y=132)
                self.textfont = ttk.Combobox(
                    self.propwindow,
                    values=self.fonts,
                    state="readonly",
                    textvariable=self.font,
                    font=(self.config["font"], 15),
                )
                self.textfont.place(x=220, y=130, width=100, height=30)
                self.textsize = tk.Entry(
                    self.propwindow,
                    bg=self.config["editor"]["background"],
                    font=(self.config["font"], 15),
                )
                self.textsize.place(x=220, y=170, width=100, height=30)
                self.textsize.insert(0, Gameobject.size)
                self.textsizelabel = tk.Label(
                    self.propwindow,
                    text="Size",
                    bg=self.config["editor"]["background"],
                    font=(self.config["font"], 15),
                )
                self.textsizelabel.place(x=82, y=170)
                self.textLabel = tk.Label(
                    self.propwindow,
                    text="Text",
                    bg=self.config["editor"]["background"],
                    font=(self.config["font"], 15),
                )
                self.textLabel.place(x=82, y=210)
                self.text = tk.Entry(
                    self.propwindow,
                    bg=self.config["editor"]["background"],
                    font=(self.config["font"], 15),
                )
                self.text.place(x=220, y=210, width=100, height=30)
                self.propwinupdatebutton.place(x=125, y=285, width=150, height=40)

    def showColorPicker(self):
        """
        Opens the color picker window
        """
        color_code = colorchooser.askcolor(title="Choose color")
        self.color_code = color_code[1] if color_code[1] != None else None

    def propWinUpdateObject(self):
        """
        Updates the selected object with the new properties given in the properties window
        """
        Gameobject = self.objects[self.objectSelectMenu.get()]
        if Gameobject.type != "image":
            if self.color_code != None:
                Gameobject.changeColor(self.color_code)
        if Gameobject.type == "line":
            thickness = self.textthickness.get()
            if thickness != "":
                if thickness.isdigit():
                    if int(thickness) > 0:
                        Gameobject.changeThickness(int(self.textthickness.get()))
        if Gameobject.type == "text":
            font = self.font.get()
            size = self.textsize.get()
            text = self.text.get()
            Gameobject.changeText(text)
            Gameobject.changeFont(font)
            if size != "":
                if size.isdigit():
                    if int(size) > 0:
                        Gameobject.changeSize(int(size))

        self.propwindow.destroy()

    def loadProject(self):
        """
        Loads a project from a folder
        """
        confirm = messagebox.askyesno(
            message="all the contents of the current project will be deleted",
            title="Are you sure?",
        )
        if confirm:
            self.path = filedialog.askdirectory(title="Select Project Folder")
            if self.path != "":
                self.loadProjectFunc(self.path)

    def loadProjectFunc(self, path):
        self.path = path
        try:
            self.projectfile = json.load(open(self.path + "/project.tyro", "r"))
            for obj in self.projectfile["objects"]:
                if obj["type"] == "rectangle":
                    self.objects[obj["name"]] = Rectangle(
                        id=obj["id"],
                        x=obj["x"],
                        y=obj["y"],
                        width=obj["width"],
                        height=obj["height"],
                        scale=obj["scale"],
                        color=obj["color"],
                        name=obj["name"],
                        canvas=self.canvas,
                    )
                if obj["type"] == "ellipse":
                    self.objects[obj["name"]] = Ellipse(
                        id=obj["id"],
                        x=obj["x"],
                        y=obj["y"],
                        width=obj["width"],
                        height=obj["height"],
                        scale=obj["scale"],
                        color=obj["color"],
                        name=obj["name"],
                        canvas=self.canvas,
                    )

                if obj["type"] == "line":
                    self.objects[obj["name"]] = Line(
                        id=obj["id"],
                        x=obj["x"],
                        y=obj["y"],
                        width=obj["width"],
                        height=obj["height"],
                        scale=obj["scale"],
                        color=obj["color"],
                        name=obj["name"],
                        canvas=self.canvas,
                        thickness=obj["thickness"],
                    )

                if obj["type"] == "text":
                    self.objects[obj["name"]] = Text(
                        id=obj["id"],
                        name=obj["name"],
                        x=obj["x"],
                        y=obj["y"],
                        text=obj["text"],
                        color=obj["color"],
                        font=obj["font"],
                        size=obj["size"],
                        canvas=self.canvas,
                    )

                if obj["type"] == "image":
                    self.objects[obj["name"]] = Image(
                        id=obj["id"],
                        x=obj["x"],
                        y=obj["y"],
                        image=obj["orignal"],
                        width=obj["width"],
                        height=obj["height"],
                        scale=obj["scale"],
                        canvas=self.canvas,
                        loaded=True,
                        path=self.path + "/assets",
                    )
            for obj in self.objects.keys():
                Gameobject = self.objects[obj]
                if Gameobject.type == "image":
                    self.root.image = Gameobject.file
                    Gameobject.createCanvasImage()
                else:
                    Gameobject.updateObject()
            self.tab = self.create_tab()
            code = open(self.path + "/code.ty", "r").read()
            self.tab.insert(tk.INSERT, code)
            self.objectSelectMenu["values"] = list(self.objects.keys())
            try:
                self.currentObject.set(list(self.objects.keys())[0])
            except:
                pass
            self.title.set(self.projectfile["name"])
            self.showObjectDetails("")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            messagebox.showerror(
                message=f"Project Could not be open, \nError: {e} \nOn Line: {exc_tb.tb_lineno}",
                title="Error",
            )
            root.destroy()

    def saveProject(self):
        """
        saves loaded projects
        """
        if self.path != None:
            project = {"name": self.title.get(), "objects": []}
            projectfile = self.path + "/project.tyro"
            for obj in self.objects.keys():
                Gameobject = self.objects[obj]
                varbs = list(vars(Gameobject).items())
                if Gameobject.type == "image":
                    project["objects"].append(
                        {
                            "name": Gameobject.name,
                            "type": Gameobject.type,
                            "id": Gameobject.id,
                            "x": Gameobject.x,
                            "y": Gameobject.y,
                            "width": Gameobject.width,
                            "height": Gameobject.height,
                            "scale": Gameobject.scale,
                            "orignal": Gameobject.unedited,
                            "edited": Gameobject.edited,
                        }
                    )
                elif Gameobject.type == "text":
                    project["objects"].append(
                        {
                            "name": Gameobject.name,
                            "type": Gameobject.type,
                            "id": Gameobject.id,
                            "x": Gameobject.x,
                            "y": Gameobject.y,
                            "color": Gameobject.color,
                            "text": Gameobject.text,
                            "font": Gameobject.font,
                            "size": Gameobject.size,
                        }
                    )
                elif Gameobject.type == "line":
                    project["objects"].append(
                        {
                            "name": Gameobject.name,
                            "type": Gameobject.type,
                            "id": Gameobject.id,
                            "x": Gameobject.x,
                            "y": Gameobject.y,
                            "width": Gameobject.width,
                            "height": Gameobject.height,
                            "scale": Gameobject.scale,
                            "color": Gameobject.color,
                            "thickness": Gameobject.thickness,
                        }
                    )
                else:
                    project["objects"].append(
                        {
                            "name": Gameobject.name,
                            "type": Gameobject.type,
                            "id": Gameobject.id,
                            "x": Gameobject.x,
                            "y": Gameobject.y,
                            "width": Gameobject.width,
                            "height": Gameobject.height,
                            "scale": Gameobject.scale,
                            "color": Gameobject.color,
                        }
                    )
            script = self.path + "/code.ty"
            script = open(script, "w")
            code = self.tab.get("1.0", tk.END)
            script.write(code)
            script.close()
            json.dump(project, open(projectfile, "w"), indent=4)
            proj = json.load(open("projects.json"))
            for i in proj:
                if i["path"] == self.path:
                    proj.remove(i)
                    i = {"name": self.title.get(), "path": self.path}
                    proj.append(i)
            json.dump(proj, open("projects.json", "w"), indent=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectManager(root)
    root.mainloop()
    if app.path != None:
        path = app.path
        root = tk.Tk()
        app = App(root, path)
        app.loadProjectFunc(path)
        root.mainloop()
