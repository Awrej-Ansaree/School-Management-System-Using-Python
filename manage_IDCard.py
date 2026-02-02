from tkinter import *
from tkinter import ttk, messagebox, filedialog, colorchooser
from PIL import Image, ImageTk, ImageFont, ImageDraw
import sqlite3
import os
import entryplaceholder as eph
import getFont


class idCard_Class:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1050x520+300+130")
        self.root.resizable(0, 0)
        self.root.title("ID Card")
        self.root.focus_force()
        self.root.grab_set()

        # -----------------------All Variables-------------------
        self.checkVar1 = IntVar()
        self.checkVar2 = IntVar()
        self.checkVar3 = IntVar()
        self.checkVar4 = IntVar()
        self.checkVar5 = IntVar()
        self.checkVar6 = IntVar()
        self.checkVar7 = IntVar()
        self.selectAllVar = IntVar()
        self.fontSize_Var = IntVar()
        self.fontSize_Var.set(20)

        self.photoFolder_Var = StringVar()
        self.IDCard_Var = StringVar()
        self.outFolder_Var = StringVar()
        self.photoWidth_Var = StringVar()
        self.photoheight_Var = StringVar()
        self.fontName_Var = StringVar()
        self.rgbColor = (0, 0, 0)
        self.fontDict = {}

        self.bg_img = Image.open("images/bg/img1.jpg")
        self.bg_img = self.bg_img.resize((1050, 520), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        self.fieldList = []
        self.fieldDict = {}
        self.fieldLoc = {}
        self.stdlist = []
        self.stdIDList = []
        self.photoList = []
        self.fieldIndex = 0

        # ==============================Designing UI=============================
        bg_lbl = Label(self.root, image=self.bg_img).place(
            x=0, y=0, relwidth=1)

        lbl_title = Label(self.root, text="ID Card", font=(
            "goudy old style", 25, "bold"), bg="white").pack(side=TOP, fill=X, padx=10, pady=7)

        # ================= Frame-1 ==================================
        frame1 = Frame(self.root, bd=0, bg="white", padx=10, pady=15)
        frame1.place(x=20, y=100, width=200, height=400)

        frame1title = Label(frame1, text="Select the Attributes\n You need:", font=(
            "goudy old style", 15, "bold"), bg="white").pack(side=TOP, fill=X, padx=5, pady=5)

        checkBox1 = Checkbutton(frame1, text="Name", variable=self.checkVar1,
                                onvalue=1, offvalue=0, bg="white", font=("goudy old style", 15),
                                activebackground="white").pack(anchor=W, side=TOP, padx=10)

        checkBox2 = Checkbutton(frame1, text="Class", variable=self.checkVar2,
                                onvalue=1, offvalue=0, bg="white", font=("goudy old style", 15),
                                activebackground="white").pack(anchor=W, side=TOP, padx=10)

        checkBox3 = Checkbutton(frame1, text="Gender", variable=self.checkVar3,
                                onvalue=1, offvalue=0, bg="white", font=("goudy old style", 15),
                                activebackground="white").pack(anchor=W, side=TOP, padx=10)

        checkBox4 = Checkbutton(frame1, text="DOB", variable=self.checkVar4,
                                onvalue=1, offvalue=0, bg="white", font=("goudy old style", 15),
                                activebackground="white").pack(anchor=W, side=TOP, padx=10)

        checkBox5 = Checkbutton(frame1, text="Father's Name", variable=self.checkVar5,
                                onvalue=1, offvalue=0, bg="white", font=("goudy old style", 15),
                                activebackground="white").pack(anchor=W, side=TOP, padx=10)

        checkBox6 = Checkbutton(frame1, text="Contact", variable=self.checkVar6,
                                onvalue=1, offvalue=0, bg="white", font=("goudy old style", 15),
                                activebackground="white").pack(anchor=W, side=TOP, padx=10)

        checkBox7 = Checkbutton(frame1, text="Address", variable=self.checkVar7,
                                onvalue=1, offvalue=0, bg="white", font=("goudy old style", 15),
                                activebackground="white").pack(anchor=W, side=TOP, padx=10)

        selectAll = Checkbutton(frame1, text="Select All", variable=self.selectAllVar, onvalue=1, offvalue=0,
                                bg="white", font=("goudy old style", 15, "bold"), activebackground="white",
                                command=self.checkAllBox).pack(anchor=CENTER, side=BOTTOM, padx=10)

        frame2 = Frame(self.root, bd=0, bg="white", padx=10, pady=15)
        frame2.place(x=240, y=100, width=400, height=400)

        # -------------------Select Photo Folder Frame---------------------------
        selectphotoFolderlbl = Label(frame2, text="Select Photo Folder", font=(
            "goudy old style", 18, "bold"), bg="white").pack(side=TOP, fill=X, pady=2)

        photoFolderFrame = Frame(frame2, bg="white")
        photoFolderFrame.pack(pady=10)

        photoFolderPath_txt = Entry(photoFolderFrame, font=(
            "goudy old style", 15), width=25, bd=1, relief=SOLID, textvariable=self.photoFolder_Var)
        photoFolderPath_txt.grid(row=0, column=0, sticky="w")

        photoFolderbtn = Button(photoFolderFrame, text="Photo Folder", width=12, bg="#222222", fg="white",
                                bd=0, cursor="hand2", font=("goudy old style", 11), command=self.getPhotosPath)
        photoFolderbtn.grid(row=0, column=1, sticky="w", padx=2)

        # -------------------Select ID Card Design Frame---------------------------
        selectIDCardlbl = Label(frame2, text="Select ID Card", font=(
            "goudy old style", 18, "bold"), bg="white").pack(side=TOP, fill=X, pady=2)

        selectIDCardFrame = Frame(frame2, bg="white")
        selectIDCardFrame.pack(pady=10)

        IDCardPath_txt = Entry(selectIDCardFrame, font=(
            "goudy old style", 15), width=25, bd=1, relief=SOLID, textvariable=self.IDCard_Var)
        IDCardPath_txt.grid(row=0, column=0, sticky="w")

        selectIDCardbtn = Button(selectIDCardFrame, text="ID Card", width=12, bg="#222222", fg="white",
                                 bd=0, cursor="hand2", font=("goudy old style", 11), command=self.getIDCardPath)
        selectIDCardbtn.grid(row=0, column=1, sticky="w", padx=2)

        # ---------------------Output Folder Frame----------------------------------
        outFolderlbl = Label(frame2, text="Select Output Folder", font=(
            "goudy old style", 18, "bold"), bg="white").pack(side=TOP, fill=X, pady=2)
        outFolderFrame = Frame(frame2, bg="white")
        outFolderFrame.pack(pady=10)

        outFolderbtn = Button(outFolderFrame, text="Out Folder", width=12, bg="#222222", fg="white",
                              bd=0, cursor="hand2", font=("goudy old style", 11), command=self.getOutDirPath)
        outFolderbtn.grid(row=0, column=0, sticky="w", padx=2)

        outFolderPath_txt = Label(outFolderFrame, font=(
            "goudy old style", 15), width=23, textvariable=self.outFolder_Var)
        outFolderPath_txt.grid(row=0, column=1, sticky="w")

        # -------------------Photo Size Frame---------------------------
        photosize_frame = Frame(frame2, bg="white")
        photosize_frame.pack(pady=10)

        photosizelbl = Label(photosize_frame, text="Photo Size", font=(
            "goudy old style", 15, "bold"), bg="white")
        photosizelbl.grid(row=0, column=0, sticky="w")

        self.photowidthtxt = Entry(photosize_frame, font=("goudy old style", 15), width=10, bd=1,
                                   relief=SOLID, fg="#777777", justify=CENTER, textvariable=self.photoWidth_Var)
        self.photowidthtxt.grid(row=0, column=1, sticky="w", padx=5)
        self.photoWidth_Var.set("Width")
        eph.changeOnFocus(self.photowidthtxt, "Width")

        by_lbl = Label(photosize_frame, text="X", font=(
            "Aerial", 15), bg="white").grid(row=0, column=2, sticky="w", padx=5)

        self.photoheighttxt = Entry(photosize_frame, font=(
            "goudy old style", 15,), width=10, bd=1, relief=SOLID, fg="#777777", justify=CENTER, textvariable=self.photoheight_Var)
        self.photoheighttxt.grid(row=0, column=3, sticky="w", padx=5)
        self.photoheight_Var.set("Height")
        eph.changeOnFocus(self.photoheighttxt, "Height")

        # ------------------Set Details Location btn & Generate ID Card btn--------------------
        setTextlocbtn = Button(frame2, text=" Set Location ", bg="#2046b0", fg="white",
                               bd=0, cursor="hand2", font=("goudy old style", 15, "bold"), command=self.setloc)
        setTextlocbtn.place(x=20, y=330)

        self.genIDCardbtn = Button(frame2, text=" Generate ", bg="#179639", fg="white", bd=0, cursor="hand2",
                                   font=("goudy old style", 15, "bold"), command=self.genIDCard)
        self.genIDCardbtn.place(x=250, y=330)

        frame3 = Frame(self.root, bd=0, bg="white", padx=10, pady=15)
        frame3.place(x=670, y=100, width=350, height=400)

        # -------------------Select Font Frame-----------------------------------------
        selectFontlbl = Label(frame3, text="Select Font", font=(
            "goudy old style", 18, "bold"), bg="white").pack(side=TOP, fill=X, pady=2)

        fontFrame = Frame(frame3, bg="white")
        fontFrame.pack(pady=10)

        font_txt = ttk.Combobox(fontFrame, font=(
            "goudy old style", 15, "bold"), width=25, textvariable=self.fontName_Var, state="readonly", justify=CENTER)
        font_txt["values"] = self.getfontName()
        font_txt.grid(row=0, column=0, sticky="w")
        font_txt.current(0)

        # ---------------------Font Size Frame-----------------------------------------
        fontSizeFrame = Frame(frame3, bg="white")
        fontSizeFrame.pack(pady=10)

        fontSizelbl = Label(fontSizeFrame, text="Font Size", bg="white", fg="#222222",
                            bd=0, cursor="hand2", font=("goudy old style", 15, "bold"))
        fontSizelbl.grid(row=0, column=0, sticky="w", padx=5)

        fontSize_num = Spinbox(fontSizeFrame, from_=1, to=100, font=(
            "goudy old style", 15), width=17, textvariable=self.fontSize_Var, justify=CENTER)
        fontSize_num.grid(row=0, column=1, sticky="w", padx=5)

        # -------------------------------select Color Frame-----------------------------
        colorFrame = Frame(frame3, bg="white")
        colorFrame.pack(pady=10)

        colorlbl = Label(colorFrame, text="Text Color", bg="white", fg="#222222",
                         bd=0, cursor="hand2", font=("goudy old style", 15, "bold"))
        colorlbl.grid(row=0, column=0, sticky="w", padx=10)

        colorbtn = Button(colorFrame, text="Select Color", font=(
            "goudy old style", 15), width=14, bg="#222222", fg="white", bd=0, command=self.selectColor)
        colorbtn.grid(row=0, column=1, sticky="w", padx=10)

        # ------------------clear btn--------------------
        self.clearbtn = Button(frame3, text=" Clear ", bg="#179639", fg="white", bd=0, cursor="hand2",
                               font=("goudy old style", 15, "bold"), command=self.clear)
        self.clearbtn.pack(pady=5)

    # ==============All Functions/Methods================
    def getfontName(self):
        self.fontDict = getFont.fontDictonary("C:/windows/fonts")
        fontNameList = list(self.fontDict.keys())
        return fontNameList

    def selectColor(self):
        color_code = colorchooser.askcolor(title="Choose color")[0]
        if color_code != None:
            self.rgbColor = tuple([int(n) for n in color_code])

    def checkAllBox(self):
        try:
            if self.selectAllVar.get() == 1:
                self.checkVar1.set(1)
                self.checkVar2.set(1)
                self.checkVar3.set(1)
                self.checkVar4.set(1)
                self.checkVar5.set(1)
                self.checkVar6.set(1)
                self.checkVar7.set(1)
            else:
                self.checkVar1.set(0)
                self.checkVar2.set(0)
                self.checkVar3.set(0)
                self.checkVar4.set(0)
                self.checkVar5.set(0)
                self.checkVar6.set(0)
                self.checkVar7.set(0)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def checkblank(self):
        try:
            if (self.checkVar1.get() != 1 and self.checkVar2.get() != 1 and self.checkVar3.get() != 1 and
                self.checkVar4.get() != 1 and self.checkVar5.get() != 1 and self.checkVar6.get() != 1 and
                    self.checkVar7.get() != 1):
                messagebox.showerror(
                    "Error", f"Please Select the attributes you need then\nTry again", parent=self.root)
                return 0

            elif len(self.photoFolder_Var.get()) <= 0:
                messagebox.showerror(
                    "Error", f"Please Select the Photo's Folder then\nTry again", parent=self.root)
                return 0

            elif len(self.IDCard_Var.get()) <= 0:
                messagebox.showerror(
                    "Error", f"Please Select the ID Card Design then\nTry again", parent=self.root)
                return 0

            elif len(self.outFolder_Var.get()) <= 0:
                messagebox.showerror(
                    "Error", f"Please Select the Output Folder then\nTry again", parent=self.root)
                return 0

            elif (self.photoWidth_Var.get() == "Width" or len(self.photoWidth_Var.get()) <= 0):
                messagebox.showerror(
                    "Error", f"Please enter photo width value in pixels then\nTry again", parent=self.root)
                return 0

            elif (self.photoheight_Var.get() == "Height" or len(self.photoheight_Var.get()) <= 0):
                messagebox.showerror(
                    "Error", f"Please enter photo height value in pixels then\nTry again", parent=self.root)
                return 0

            return 1
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def getFieldLoc(self, entry, event):
        self.fieldLoc[entry.get()] = (event.x, event.y)

    def getCursorLoc(self, event):
        if self.fieldIndex < len(self.fieldList):
            entry = Entry(self.setlocRoot, bd=1, font=(
                self.fontName_Var.get(), self.fontSize_Var.get()-7), relief=SOLID, width=8)
            entry.place(x=event.x, y=event.y)
            entry.focus_force()
            entry.bind("<Return>", lambda x: self.getFieldLoc(entry, event))
            self.fieldIndex += 1
        self.fieldIndex = 0

    def addField(self):
        if self.checkVar1.get() == 1:
            self.fieldList.append("Name")
            self.fieldDict["Name"] = "student.name"
            self.fieldLoc["Name"] = ""
        if self.checkVar2.get() == 1:
            self.fieldList.append("Class")
            self.fieldDict["Class"] = "class.classname"
            self.fieldLoc["Class"] = ""
        if self.checkVar3.get() == 1:
            self.fieldList.append("Gender")
            self.fieldDict["Gender"] = "student.gender"
            self.fieldLoc["Gender"] = ""
        if self.checkVar4.get() == 1:
            self.fieldList.append("DOB")
            self.fieldDict["DOB"] = "student.dob"
            self.fieldLoc["DOB"] = ""
        if self.checkVar5.get() == 1:
            self.fieldList.append("Father")
            self.fieldDict["Father"] = "student.father"
            self.fieldLoc["Father"] = ""
        if self.checkVar6.get() == 1:
            self.fieldList.append("Contact")
            self.fieldDict["Contact"] = "student.phone"
            self.fieldLoc["Contact"] = ""
        if self.checkVar7.get() == 1:
            self.fieldList.append("Address")
            self.fieldDict["Address"] = "student.pAddr"
            self.fieldLoc["Address"] = ""
        self.fieldList.append("Photo")
        self.fieldLoc["Photo"] = ""

    def setloc(self):
        try:
            self.fieldLoc.clear()
            self.photoList.clear()
            self.stdIDList.clear()
            self.stdlist.clear()
            value = self.checkblank()
            if value == 1:
                self.addField()
                self.fieldIndex = 0
                self.setlocRoot = Toplevel()
                self.setlocRoot.title("Set Attributes Location")
                self.setlocRoot.config(bg="white")
                self.setlocRoot.focus_force()
                self.setlocRoot.grab_set()

                self.IDimg = Image.open(self.IDCard_Var.get())
                width, height = self.IDimg.size
                self.IDimg = ImageTk.PhotoImage(self.IDimg)

                self.setlocRoot.geometry(f"{width}x{height}")
                self.setlocRoot.resizable(0, 0)

                drawing_area = Canvas(self.setlocRoot)
                drawing_area.pack(fill=BOTH, expand=1)
                drawing_area.bind("<ButtonPress-1>", self.getCursorLoc)
                drawing_area.create_image(0, 0, anchor=NW, image=self.IDimg)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def getPhotosPath(self):
        try:
            path = filedialog.askdirectory(
                initialdir="/", title="Select Students Image Folder", parent=self.root)
            if not (len(path) <= 0):
                self.photoFolder_Var.set(path)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def getIDCardPath(self):
        try:
            f_types = [("Images", ("*.png", "*.jpg")), ("PNG Files","*.png"), 
                       ("JPG Files", "*.jpg"), ("All Files", "*.*")]
            path = filedialog.askopenfilename(
                initialdir="/", title="Select Student Image", filetypes=f_types, parent=self.root)
            if not (len(path) <= 0):
                self.IDCard_Var.set(path)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def getOutDirPath(self):
        try:
            path = filedialog.askdirectory(
                initialdir="/", title="Select Output Folder", parent=self.root)
            if not (len(path) <= 0):
                self.outFolder_Var.set(path)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def genIDCard(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            if not (len(self.fieldLoc) <= 0):
                # Getting the Student ID from images name and full path of images
                for dirpath, dirname, files in os.walk(self.photoFolder_Var.get()):
                    for file in files:
                        file = file.lower()
                        if file.endswith(".jpeg") or file.endswith(".png") or file.endswith(".jpg"):
                            self.photoList.append(os.path.join(dirpath, file))
                            f = file.split(".")[0]
                            if f.isnumeric():
                                self.stdIDList.append(int(f))

                # Fetching the student data from the database and adding to self.stdlist
                selectAttribs = ", ".join(list(self.fieldDict.values()))

                for stdID in self.stdIDList:
                    cur.execute(f"Select {selectAttribs} from student, class where student.class_id = class.id and student.id=?",
                                (stdID,))
                    row = cur.fetchone()

                    if row != None:
                        self.stdlist.append(list(row))

                stdIndex = 0
                DataIndex = 0
                stdAttrib = list(self.fieldDict.keys())

                for Data in self.stdlist:
                    cardImg = self.IDCard_Var.get()
                    cardImg = Image.open(cardImg)
                    for i in range(len(Data)):
                        id = ImageDraw.Draw(cardImg)
                        id.text(self.fieldLoc[stdAttrib[i]], Data[i], fill=self.rgbColor,
                                font=ImageFont.truetype(self.fontDict[self.fontName_Var.get()], self.fontSize_Var.get()))

                        cardImg.save(os.path.join(
                            self.outFolder_Var.get(), f"{self.stdIDList[stdIndex]}.png"))
                        DataIndex += 1

                    if DataIndex >= len(stdAttrib):
                        stdimg = Image.open(self.photoList[stdIndex])
                        stdimg = stdimg.resize(
                            (int(self.photoWidth_Var.get()), int(self.photoheight_Var.get())), Image.ANTIALIAS)
                        cardImg.paste(stdimg, self.fieldLoc["Photo"])
                        cardImg.save(os.path.join(
                            self.outFolder_Var.get(), f"{self.stdIDList[stdIndex]}.png"))
                        stdIndex += 1

                self.clear()
                messagebox.showinfo(
                    "Success", "ID Card created successfully", parent=self.root)

            else:
                messagebox.showerror(
                    "Error", "Please set the location for the Fields/Attribute", parent=self.root)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def clear(self):
        # Reseting the List and Dictionary
        self.fieldLoc.clear()
        self.fieldList.clear()
        self.fieldList.append("Photo")
        self.photoList.clear()
        self.stdIDList.clear()
        self.stdlist.clear()
        # Reseting the Int and String variables
        # IntVar
        self.checkVar1.set(0)
        self.checkVar2.set(0)
        self.checkVar3.set(0)
        self.checkVar4.set(0)
        self.checkVar5.set(0)
        self.checkVar6.set(0)
        self.checkVar7.set(0)
        self.selectAllVar.set(0)
        # StringVar
        self.photoFolder_Var.set("")
        self.IDCard_Var.set("")
        self.outFolder_Var.set("")
        self.photoWidth_Var.set("Width")
        eph.changeOnFocus(self.photowidthtxt, "Width")
        self.photoheight_Var.set("Height")
        eph.changeOnFocus(self.photoheighttxt, "Height")


if __name__ == "__main__":
    root = Tk()
    obj = idCard_Class(root)
    root.mainloop()
