from tkinter import *
from tkinter import ttk, messagebox, filedialog
import datetime
from PIL import Image, ImageTk
import face_recognition
import sqlite3
import cv2
import os
import io
import json
import numpy as np
import pandas as pd
import xlsxwriter


class manage_students_Class:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1050x520+300+130")
        self.root.title("Manage Students")
        self.root.resizable(0, 0)
        self.root.focus_force()
        self.root.grab_set()

        # =================All Variables==================
        self.std_id_var = StringVar()
        self.name_var = StringVar()
        self.class_var = StringVar()
        self.email_var = StringVar()
        self.gender_var = StringVar()
        self.father_name = StringVar()
        self.mother_name = StringVar()
        self.phone_var = StringVar()
        self.dob_var = StringVar()
        self.dor_var = StringVar()
        self.pAddr_var = StringVar()
        self.tAddr_var = StringVar()
        self.prevSchool_var = StringVar()
        self.prevClass_var = StringVar()
        self.stdStatus_var = StringVar()
        self.img_filename = ""
        self.std_img = ""
        self.fob = ""

        self.search_by = StringVar()
        self.search_txt = StringVar()
        self.search_class = StringVar()

        # =================loading background image=================
        self.bg_img = Image.open("images/bg/manage_std_bg.jpg")
        self.bg_img = self.bg_img.resize((1050, 520), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        # =====================================Designing UI==================================
        bg_lbl = Label(self.root, image=self.bg_img).place(
            x=0, y=0, relwidth=1)

        lbl_title = Label(self.root, text="Manage Students", font=(
            "goudy old style", 25, "bold"), bg="white").pack(side=TOP, fill=X, padx=10, pady=7)

        # ==================Student Details Frame==================
        std_details_frame = Frame(self.root, bg="white")
        std_details_frame.place(x=25, y=70, width=450, height=440)

        # =======title====
        lbl_title = Label(std_details_frame, text="Student Details", font=(
            "goudy old style", 18, "bold"), bg="#29406b", fg="white").pack(side=TOP, fill=X)

        # =============std image Frame============
        std_img_detail = Frame(std_details_frame, pady=10, padx=10, bg="white")
        std_img_detail.place(y=30, relwidth=1, height=150)

        # ============std image lbl===========
        self.std_img_lbl = Label(std_img_detail, text="Photo", font=(
            "goudy old style", 15), justify=CENTER, bg="white", bd=1, relief=SOLID)
        self.std_img_lbl.place(y=5, width=140, height=130)

        # =========browse image btn===========
        self.browse_std_img = PhotoImage(file="images/browse_std_img.png")
        browse_std_img_btn = Button(std_img_detail, image=self.browse_std_img, command=self.browse_img, font=(
            "goudy old style", 15), bg="lightgray", fg="white", cursor="hand2")
        browse_std_img_btn.place(x=170, y=20)

        lbl_date_format = Label(std_img_detail, text="Note: Date Format Should be\nYYYY-MM-DD (2078-01-01)",
                                font=("times", 11, "italic"), bg="lightyellow", padx=5).place(x=230, y=45)

        # =========click picture btn==========
        self.take_image = PhotoImage(file="images/click_picture1.png")
        click_std_img_btn = Button(std_img_detail, image=self.take_image, command=self.click_pic, font=(
            "goudy old style", 15), bg="lightgray", fg="white", cursor="hand2")
        click_std_img_btn.place(x=170, y=70)

        # ===========================Scrollable Frame=========================
        # =====frame====
        scrollable_frame = Frame(std_details_frame)
        scrollable_frame.place(y=190, relwidth=1, height=230)

        # ====canvas====
        scroll_canvas = Canvas(
            scrollable_frame, bg="white", highlightthickness=0, bd=0)
        scroll_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # ==scrollbar===
        scroll_y_canvas = Scrollbar(
            scrollable_frame, orient=VERTICAL, command=scroll_canvas.yview)
        scroll_y_canvas.pack(side=RIGHT, fill=Y)

        # =====configure the scrollbar=====
        scroll_canvas.configure(yscrollcommand=scroll_y_canvas.set)
        scroll_canvas.bind("<Configure>", lambda e: scroll_canvas.configure(
            scrollregion=scroll_canvas.bbox("all")))

        # =====students details frame======
        self.std_details_menu = Frame(scroll_canvas, bg="white")

        # ======creating a new window======
        scroll_canvas.create_window(
            (0, 0), window=self.std_details_menu, anchor="nw")

        # ============================Adding the Details Fields===============================
        lbl_id = Label(self.std_details_menu, text="ID",
                       font=("goudy old style", 18), bg="white")
        lbl_id.grid(row=0, column=0, pady=6, padx=15, sticky="w")

        txt_id = Entry(self.std_details_menu, textvariable=self.std_id_var,
                       relief=SOLID, font=("goudy old style", 15), state="readonly")
        txt_id.grid(row=0, column=1, sticky="w")

        lbl_name = Label(self.std_details_menu, text="Name",
                         font=("goudy old style", 18), bg="white")
        lbl_name.grid(row=1, column=0, pady=6, padx=15, sticky="w")

        txt_name = Entry(self.std_details_menu, textvariable=self.name_var,
                         relief=SOLID, font=("goudy old style", 15))
        txt_name.grid(row=1, column=1, sticky="w")

        lbl_class = Label(self.std_details_menu, text="Class",
                          font=("goudy old style", 18), bg="white")
        lbl_class.grid(row=3, column=0, pady=6, padx=15, sticky="w")

        self.combo_class = ttk.Combobox(self.std_details_menu, textvariable=self.class_var, font=(
            "goudy old style", 15), state="readonly", width=18, justify=CENTER)
        self.combo_class.grid(row=3, column=1)
        self.combo_class.set("Select")

        lbl_gender = Label(self.std_details_menu, text="Gender",
                           font=("goudy old style", 18), bg="white")
        lbl_gender.grid(row=4, column=0, pady=6, padx=15, sticky="w")

        combo_gender = ttk.Combobox(self.std_details_menu, textvariable=self.gender_var, values=("Select", "Male", "Female", "Other"), font=("goudy old style", 15),
                                    state="readonly", width=18, justify=CENTER)
        combo_gender.grid(row=4, column=1, sticky="w")
        combo_gender.current(0)

        lbl_dob = Label(self.std_details_menu, text="D.O.B",
                        font=("goudy old style", 18), bg="white")
        lbl_dob.grid(row=5, column=0, pady=6, padx=15, sticky="w")

        txt_dob = Entry(self.std_details_menu, textvariable=self.dob_var, relief=SOLID,
                        font=("goudy old style", 15))
        txt_dob.grid(row=5, column=1, sticky="w")

        lbl_father_name = Label(self.std_details_menu, text="Father's Name", font=(
            "goudy old style", 18), bg="white")
        lbl_father_name.grid(row=6, column=0, pady=6, padx=15, sticky="w")

        txt_father_name = Entry(self.std_details_menu, textvariable=self.father_name, relief=SOLID,
                                font=("goudy old style", 15))
        txt_father_name.grid(row=6, column=1, sticky="w")

        lbl_mother_name = Label(self.std_details_menu, text="Mother's Name", font=(
            "goudy old style", 18), bg="white")
        lbl_mother_name.grid(row=7, column=0, pady=6, padx=15, sticky="w")

        txt_mother_name = Entry(
            self.std_details_menu, textvariable=self.mother_name, relief=SOLID, font=("goudy old style", 15))
        txt_mother_name.grid(row=7, column=1, sticky="w")

        lbl_phone = Label(self.std_details_menu, text="Phone", font=(
            "goudy old style", 18), bg="white")
        lbl_phone.grid(row=8, column=0, pady=6, padx=15, sticky="w")

        txt_phone = Entry(self.std_details_menu, textvariable=self.phone_var, relief=SOLID,
                          font=("goudy old style", 15))
        txt_phone.grid(row=8, column=1, sticky="w")

        lbl_email = Label(self.std_details_menu, text="Email",
                          font=("goudy old style", 18), bg="white")
        lbl_email.grid(row=9, column=0, pady=6, padx=15, sticky="w")

        txt_email = Entry(self.std_details_menu, textvariable=self.email_var,
                          relief=SOLID, font=("goudy old style", 15))
        txt_email.grid(row=9, column=1, sticky="w")

        lbl_tAddr = Label(self.std_details_menu, text="Temporary Address", font=(
            "goudy old style", 18), bg="white")
        lbl_tAddr.grid(row=10, column=0, pady=6, padx=15, sticky="w")

        self.txt_tAddr = Entry(self.std_details_menu, textvariable=self.tAddr_var, relief=SOLID,
                               font=("goudy old style", 15))
        self.txt_tAddr.grid(row=10, column=1, sticky="w")

        lbl_pAddr = Label(self.std_details_menu, text="Permanent Address", font=(
            "goudy old style", 18), bg="white")
        lbl_pAddr.grid(row=11, column=0, pady=6, padx=15, sticky="w")

        self.txt_pAddr = Entry(self.std_details_menu, textvariable=self.pAddr_var, relief=SOLID,
                               font=("goudy old style", 15))
        self.txt_pAddr.grid(row=11, column=1, sticky="w")

        lbl_dor = Label(self.std_details_menu, text="D.O.R",
                        font=("goudy old style", 18), bg="white")
        lbl_dor.grid(row=12, column=0, pady=6, padx=15, sticky="w")

        txt_dor = Entry(self.std_details_menu, textvariable=self.dor_var, relief=SOLID,
                        font=("goudy old style", 15))
        txt_dor.grid(row=12, column=1, sticky="w")

        lbl_prevSchool = Label(self.std_details_menu, text="Previous School", font=(
            "goudy old style", 18), bg="white")
        lbl_prevSchool.grid(row=13, column=0, pady=6, padx=15, sticky="w")

        self.txt_prevSchool = Entry(self.std_details_menu, textvariable=self.prevSchool_var, relief=SOLID,
                                    font=("goudy old style", 15))
        self.txt_prevSchool.grid(row=13, column=1, sticky="w")

        lbl_prevClass = Label(self.std_details_menu, text="Previous Class", font=(
            "goudy old style", 18), bg="white")
        lbl_prevClass.grid(row=14, column=0, pady=6, padx=15, sticky="w")

        self.txt_prevClass = Entry(self.std_details_menu, textvariable=self.prevClass_var, relief=SOLID,
                                   font=("goudy old style", 15))
        self.txt_prevClass.grid(row=14, column=1, sticky="w")

        lbl_status = Label(self.std_details_menu, text="Status",
                           font=("goudy old style", 18), bg="white")
        lbl_status.grid(row=15, column=0, pady=6, padx=15, sticky="w")

        combo_status = ttk.Combobox(self.std_details_menu, textvariable=self.stdStatus_var, values=("Select", "Active", "Deactive"), font=("goudy old style", 15),
                                    state="readonly", width=18, justify=CENTER)
        combo_status.grid(row=15, column=1, sticky="w")
        combo_status.current(0)

        # =======================================Student Frame=============================
        frame2 = Frame(self.root, bd=0, bg="white")
        frame2.place(x=475, y=99, height=405, width=550)

        studentTable_Frame = Frame(frame2, bd=0, bg="#29406b")
        studentTable_Frame.place(x=0, y=0, height=350, width=550)

        # =======================Search Frame=======================
        searchFrame = LabelFrame(
            studentTable_Frame, text="Search By", font=("times new roman", 15), bg="#29406b", fg="white", relief=SOLID, bd=0)
        searchFrame.pack(fill=X, padx=5, pady=5)

        # ==========Search by=========
        self.search_by_class = ttk.Combobox(searchFrame, textvariable=self.search_class, values=(
            "Select Class",), font=("goudy old style", 15), state="readonly", width=15, justify=CENTER)
        self.search_by_class.pack(side=LEFT, padx=8, pady=2)
        self.search_by_class.current(0)
        self.search_by_class.bind("<<ComboboxSelected>>", self.search)

        combo_search_by = ttk.Combobox(searchFrame, textvariable=self.search_by, values=(
            "Select", "ID", "Name", "Email", "Phone"), state="readonly", justify=CENTER, font=("goudy old style", 15), width=15)
        combo_search_by.pack(side=LEFT)
        combo_search_by.current(0)

        search_txt = Entry(searchFrame, textvariable=self.search_txt, font=(
            "goudy old style", 15), width=15, relief=SOLID)
        search_txt.pack(side=LEFT, padx=8)
        search_txt.bind("<Return>", self.search)

        # ==================================Student Table Frame=================================
        # X scrollbar
        scroll_x = Scrollbar(studentTable_Frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X, padx=1, pady=1)

        # Y scrollbar
        scroll_y = Scrollbar(studentTable_Frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y, padx=1, pady=1)

        # table
        self.student_table = ttk.Treeview(studentTable_Frame,
                                          columns=("id", "name", "class", "gender", "dob", "father", "mother",
                                                   "phone", "email", "tAddr", "pAddr", "prevSchool", "prevClass", "dor", "status"),
                                          xscrollcommand=scroll_x.set,
                                          yscrollcommand=scroll_y.set)
        # configure Y scrollbar
        scroll_y.config(command=self.student_table.yview)
        scroll_x.config(command=self.student_table.xview)

        # table heading
        self.student_table.heading("id", text="ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("class", text="Class")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="D.O.B")
        self.student_table.heading("father", text="Father")
        self.student_table.heading("mother", text="Mother")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("email", text="E-mail")
        self.student_table.heading("tAddr", text="Temporary Address")
        self.student_table.heading("pAddr", text="Permanent Address")
        self.student_table.heading("prevSchool", text="Previous School")
        self.student_table.heading("prevClass", text="Previous Class")
        self.student_table.heading("dor", text="D.O.R")
        self.student_table.heading("status", text="Status")
        self.student_table["show"] = "headings"

        # table column width
        self.student_table.column("id", width=80, anchor=CENTER)
        self.student_table.column("name", width=150, anchor=CENTER)
        self.student_table.column("class", width=125, anchor=CENTER)
        self.student_table.column("gender", width=100, anchor=CENTER)
        self.student_table.column("dob", width=150, anchor=CENTER)
        self.student_table.column("father", width=150, anchor=CENTER)
        self.student_table.column("mother", width=150, anchor=CENTER)
        self.student_table.column("phone", width=150, anchor=CENTER)
        self.student_table.column("email", width=180, anchor=CENTER)
        self.student_table.column("tAddr", width=180, anchor=CENTER)
        self.student_table.column("pAddr", width=180, anchor=CENTER)
        self.student_table.column("prevSchool", width=180, anchor=CENTER)
        self.student_table.column("prevClass", width=180, anchor=CENTER)
        self.student_table.column("dor", width=150, anchor=CENTER)
        self.student_table.column("status", width=150, anchor=CENTER)
        self.student_table.pack(fill=BOTH, expand=1, padx=1)
        self.student_table.bind("<ButtonRelease-1>", self.get_std_data)

        # ==========buttons=============
        btn_add = Button(self.root, text="ADD", command=self.add, font=(
            "goudy old style", 12, "bold"), bg="#0cb032", fg="white", cursor="hand2", width=10, bd=0).place(x=490, y=460)
        btn_update = Button(self.root, text="Update", command=self.update, font=(
            "goudy old style", 11, "bold"), bg="#2370db", fg="white", cursor="hand2", width=10, bd=0).place(x=600, y=460)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=(
            "goudy old style", 11, "bold"), bg="#f73939", fg="white", cursor="hand2", width=10, bd=0).place(x=700, y=460)
        btn_clear = Button(self.root, text="Clear", command=self.clear_btn, font=(
            "goudy old style", 11, "bold"), bg="#808080", fg="white", cursor="hand2", width=10, bd=0).place(x=800, y=460)
        exportbtn = Button(self.root, text="Export", command=self.exporttoxls, font=(
            "goudy old style", 11, "bold"), bg="#0cb032", fg="white", cursor="hand2", width=10, bd=0).place(x=900, y=460)

        self.get_class()
        self.show()

    # ==============All Functions/Methods================

    def browse_img(self):
        try:
            size = (139, 129)
            f_types = [("Images", ("*.png", "*.jpg")), ("PNG Files",
                                                        "*.png"), ("JPG Files", "*.jpg"), ("All Files", "*.*")]
            self.img_filename = filedialog.askopenfilename(
                initialdir="/", title="Select Student Image", filetypes=f_types, parent=self.root)
            if self.img_filename != "":
                self.std_img = Image.open(self.img_filename)
                self.std_img = self.std_img.resize(size, Image.ANTIALIAS)
                self.std_img = ImageTk.PhotoImage(self.std_img)
                self.std_img_lbl.config(image=self.std_img)
                with open(self.img_filename, "rb") as f:
                    self.fob = f.read()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def click_pic(self):
        try:
            messagebox.showinfo(
                "Info", "Note: Press 'Space' to click picture or press 'ESC' to exit", parent=self.root)
            cap = cv2.VideoCapture(0)
            size = (138, 128)
            while True:
                ret, img = cap.read()
                if ret:
                    img = cv2.resize(cv2.flip(img, 1), (385, 330))
                    img = img[20:280, 70:300]
                    cv2.imshow('Press Space to take photo', img)
                    cv2.moveWindow('Press Space to take photo', 780, 170)
                    k = cv2.waitKey(1)
                    if k % 256 == 27 or k % 256 == ord("q"):
                        break
                    elif k % 256 == 32:
                        cv2.imwrite('std_img.png', img)
                        self.img_filename = "std_img.png"
                        self.std_img = Image.open(self.img_filename)
                        self.std_img = self.std_img.resize(
                            size, Image.ANTIALIAS)
                        self.std_img = ImageTk.PhotoImage(self.std_img)
                        self.std_img_lbl.config(image=self.std_img)
                        self.fob = open(self.img_filename, "rb")
                        self.fob = self.fob.read()
                        os.remove("std_img.png")
                        break
                else:
                    messagebox.showerror(
                        "Error", "Camera failed, Please try again")
                    break
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def match_dateformat(self, date_string):
        try:
            date_format = "%Y-%m-%d"
            datetime.datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False

    def show(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            cur.execute("select student.id,name,class.classname,gender,dob,father,mother, \
                        phone,email,tAddr,pAddr,dor,prev_school,prev_class,status  FROM \
                        student, class where student.class_id = class.id")
            rows = cur.fetchall()
            if len(rows) != 0 or len(rows) == 0:
                self.student_table.delete(*self.student_table.get_children())
                for row in rows:
                    row = list(row)
                    self.student_table.insert("", END, values=row)
                    con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def get_class(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            cur.execute("select classname from class ORDER BY classname")
            rows = cur.fetchall()
            class_names = ["Select Class"]
            for row in rows:
                if row[0] not in class_names:
                    class_names.append(row[0])
            self.combo_class.config(values=class_names)
            self.search_by_class.config(values=class_names)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def get_std_data(self, event):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            f = self.student_table.focus()
            content = (self.student_table.item(f))
            row = content["values"]
            if row != "":
                self.std_id_var.set(row[0])
                self.name_var.set(row[1])
                self.class_var.set(row[2])
                self.gender_var.set(row[3])
                self.dob_var.set(row[4])
                self.father_name.set(row[5])
                self.mother_name.set(row[6])
                self.phone_var.set(row[7])
                self.email_var.set(row[8])
                self.pAddr_var.set(row[9])
                self.tAddr_var.set(row[10])
                self.dor_var.set(row[11])
                self.prevSchool_var.set(row[12])
                self.prevClass_var.set(row[13])
                self.stdStatus_var.set(row[14])
                # print(row[15]+"\n")
                cur.execute("Select photo from student where id=?",
                            (self.std_id_var.get(),))
                img_row = cur.fetchone()
                # print(img_row[0])
                self.fob = img_row[0]
                size = (139, 129)
                self.std_img = io.BytesIO(self.fob)
                self.std_img = Image.open(self.std_img)
                self.std_img = self.std_img.resize(size, Image.ANTIALIAS)
                self.std_img = ImageTk.PhotoImage(self.std_img)
                self.std_img_lbl.config(image=self.std_img)
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def add(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            if (self.name_var.get() == "" or self.class_var.get() == "" or self.gender_var.get() == "" or
                self.phone_var.get() == "" or self.father_name.get() == "" or self.mother_name.get() == "" or
                self.dob_var.get() == "" or self.dor_var.get() == "" or self.prevSchool_var.get() == "" or
                    self.pAddr_var.get() == "" or self.tAddr_var.get() == "" or self.stdStatus_var.get() == ""):
                messagebox.showerror(
                    "Error", "All fields are required.\nExcept E-mail", parent=self.root)

            else:
                if self.std_img == "" or self.fob == "":
                    messagebox.showerror(
                        "Error", "Student Image is required.\nPlease Select Student Image", parent=self.root)

                else:
                    cur.execute("Select id from class where classname=?",
                                (self.class_var.get(),))
                    stdClassid = cur.fetchone()

                    if stdClassid == None:
                        messagebox.showerror(
                            "Error", "Please Select/Enter the Correct Class and try again", parent=self.root)
                    else:
                        match_dob = self.match_dateformat(self.dob_var.get())
                        match_dor = self.match_dateformat(self.dor_var.get())

                        if not match_dob or not match_dor:
                            messagebox.showerror(
                                "Error", "You entered wrong date format.\nPlease enter like DD-MM-YYYY (01-01-2022)")

                        else:
                            cur.execute("Select * from student where (name=? and class_id=? and dob=? and father=? and mother=? and phone=? and email=?) or photo=?",
                                        (
                                            self.name_var.get(),
                                            stdClassid[0],
                                            self.dob_var.get(),
                                            self.father_name.get(),
                                            self.mother_name.get(),
                                            self.phone_var.get(),
                                            self.email_var.get(),
                                            self.fob,
                                        ))
                            std_row = cur.fetchone()

                            if std_row != None:
                                messagebox.showerror(
                                    "Error", "Student or Student Photo is already present.\
                                    \nPlease try again!", parent=self.root)

                            else:
                                cur.execute("Insert into student (name,class_id,gender,dob,father,mother,phone,\
                                            email,tAddr,pAddr,dor,prev_school,prev_class,status,photo) \
                                            values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                            (
                                                self.name_var.get(),
                                                stdClassid[0],
                                                self.gender_var.get(),
                                                self.dob_var.get(),
                                                self.father_name.get(),
                                                self.mother_name.get(),
                                                self.phone_var.get(),
                                                self.email_var.get(),
                                                self.tAddr_var.get(),
                                                self.pAddr_var.get(),
                                                self.dor_var.get(),
                                                self.prevSchool_var.get(),
                                                self.prevClass_var.get(),
                                                self.stdStatus_var.get(),
                                                self.fob,
                                            ))
                                con.commit()

                                face_encode = self.bytes_to_nparr(self.fob)

                                with open("Database/face_encodings.json") as f:
                                    face_encodings = json.load(f)

                                cur.execute(
                                    "select id from student ORDER BY id")
                                rows = cur.fetchall()

                                if len(rows) != 0 or len(rows) == 0:
                                    std_data = list(rows[-1])
                                    IDs = face_encodings["IDs"]
                                    IDs.append(std_data[0])

                                    Names = face_encodings["Names"]
                                    Names.append(self.name_var.get())

                                    Class = face_encodings["Class"]
                                    Class.append(self.class_var.get())

                                    encodelistknown = face_encodings["Encodings"]
                                    encodelistknown.append(face_encode)

                                    face_encodings = {
                                        "IDs": IDs, "Names": Names, "Class": Class, "Encodings": encodelistknown}

                                    with open("Database/face_encodings.json", "w") as f:
                                        json.dump(face_encodings, f, indent=2)

                                messagebox.showinfo(
                                    "Success", "Student Added Successfully", parent=self.root)
                                self.clear()
            con.close()
            self.show()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def update(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            if self.std_id_var.get() == "":
                messagebox.showerror(
                    "Error", "Please select student from the list", parent=self.root)

            else:
                if self.fob == "":
                    messagebox.showerror(
                        "Error", "Student Image is required.\nPlease Select Student Image", parent=self.root)

                else:
                    cur.execute("select * from student where id=?",
                                (self.std_id_var.get(),))
                    row = cur.fetchone()

                    if row == None:
                        messagebox.showerror(
                            "Error", "Please try again", parent=self.root)

                    else:
                        cur.execute(
                            "Select * from student where photo=? and id!=?", (self.fob, self.std_id_var.get(),))
                        photo_row = cur.fetchone()

                        if photo_row != None:
                            messagebox.showerror(
                                "Error", "Photo has been already used, try again", parent=self.root)

                        else:
                            match_dob = self.match_dateformat(
                                self.dob_var.get())
                            match_dor = self.match_dateformat(
                                self.dor_var.get())

                            cur.execute("Select id from class where classname=?",
                                        (self.class_var.get(),))
                            stdClassid = cur.fetchone()

                            if not match_dob or not match_dor:
                                messagebox.showerror(
                                    "Error", "You entered wrong date format.\nPlease enter like DD-MM-YYYY (01-01-2022)")

                            else:
                                op = messagebox.askyesno(
                                    "Confirm", "Do you really want to update?", parent=self.root)

                                if op:

                                    with open("Database/face_encodings.json") as f:
                                        face_encodings = json.load(f)

                                    IDs = face_encodings["IDs"]
                                    Names = face_encodings["Names"]
                                    Class = face_encodings["Class"]
                                    encodelistknown = face_encodings["Encodings"]

                                    std_index = IDs.index(
                                        int(self.std_id_var.get()))
                                    Names[std_index] = self.name_var.get()
                                    Class[std_index] = self.class_var.get()
                                    face_encodings = {"IDs": IDs, "Names": Names, "Class": Class,"Encodings": encodelistknown}

                                    with open("Database/face_encodings.json", "w") as f:
                                        json.dump(face_encodings, f, indent=2)

                                    cur.execute("update student set name=?, class_id=?, gender=?, dob=?, father=?, mother=?, phone=?, email=?, pAddr=?, tAddr=?, dor=?, prev_school=?, prev_class=?, status=?, photo=? where id=?",
                                                (
                                                    self.name_var.get(),
                                                    stdClassid[0],
                                                    self.gender_var.get(),
                                                    self.dob_var.get(),
                                                    self.father_name.get(),
                                                    self.mother_name.get(),
                                                    self.phone_var.get(),
                                                    self.email_var.get(),
                                                    self.tAddr_var.get(),
                                                    self.pAddr_var.get(),
                                                    self.dor_var.get(),
                                                    self.prevSchool_var.get(),
                                                    self.prevClass_var.get(),
                                                    self.stdStatus_var.get(),
                                                    self.fob,
                                                    self.std_id_var.get(),
                                                ))
                                    con.commit()
                                    messagebox.showinfo(
                                        "Success", "Student Record Updated Successfully", parent=self.root)
                                    self.clear()

            con.close()
            self.show()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            if self.std_id_var.get() == "":
                messagebox.showerror(
                    "Error", "Please select student from the list", parent=self.root)
            else:
                cur.execute("select * from student where id=?",
                            (self.std_id_var.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Please try again", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do you really want to delete?", parent=self.root)
                    if op:

                        with open("Database/face_encodings.json") as f:
                            face_encodings = json.load(f)
                        
                        IDs = face_encodings["IDs"]
                        Names = face_encodings["Names"]
                        Class = face_encodings["Class"]
                        encodelistknown = face_encodings["Encodings"]

                        std_index = IDs.index(int(self.std_id_var.get()))

                        del IDs[std_index]
                        del Names[std_index]
                        del Class[std_index]
                        del encodelistknown[std_index]
                        
                        face_encodings = {"IDs":IDs,"Names":Names,"Class":Class,"Encodings":encodelistknown}

                        with open("Database/face_encodings.json","w") as f:
                            json.dump(face_encodings,f,indent=2)

                        cur.execute("delete from student where id=?",
                                    (self.std_id_var.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Success", "Student Deleted Successfully", parent=self.root)

                        self.clear()
                        self.show()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def clear_btn(self):
        try:
            op = messagebox.askyesno(
                "Confirm", "Do you really want to clear?", parent=self.root)
            if op:
                self.clear()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def clear(self):
        try:
            self.std_id_var.set("")
            self.name_var.set("")
            self.class_var.set("Select")
            self.email_var.set("")
            self.gender_var.set("Select")
            self.dob_var.set("")
            self.father_name.set("")
            self.mother_name.set("")
            self.phone_var.set("")
            self.pAddr_var.set("")
            self.tAddr_var.set("")
            self.prevSchool_var.set("")
            self.prevClass_var.set("")
            self.dor_var.set("")
            self.stdStatus_var.set("Select")
            self.search_class.set("Select Class")
            self.search_by.set("Select")
            self.search_txt.set("")
            self.std_img_lbl.config(image="")
            self.img_filename = ""
            self.std_img = ""
            self.fob = ""
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def search(self, event):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            rows = ""
            if self.search_class.get() != "Select Class":
                cur.execute("select id from class where classname=?",
                            (self.search_class.get(),))
                rowClassid = cur.fetchone()
                print(rowClassid)
                if len(rowClassid) == 0:
                    messagebox.showerror(
                        "Error", "No such Class was found, Please try again", parent=self.root)

                if self.search_by.get() != "Select":
                    cur.execute("select student.id,name,class.classname,gender,dob,father,mother, \
                        phone,email,tAddr,pAddr,dor,prev_school,prev_class,status  FROM \
                        student, class where student."+str(self.search_by.get().lower())+" LIKE '%" +
                                str(self.search_txt.get())+"%' and student.class_id LIKE '%"+str(
                        rowClassid[0])+"%'"+" and student.class_id = class.id")

                    rows = cur.fetchall()
                    if len(rows) == 0:
                        messagebox.showerror(
                            "Error", "No such Student's was found", parent=self.root)

                else:
                    cur.execute("select student.id,name,class.classname,gender,dob,father,mother, \
                        phone,email,tAddr,pAddr,dor,prev_school,prev_class,status  FROM \
                        student, class where student.class_id LIKE '%"+str(
                        rowClassid[0])+"%'"+" and student.class_id = class.id")

                    rows = cur.fetchall()
                    if len(rows) == 0:
                        messagebox.showerror(
                            "Error", "No such Student's was found", parent=self.root)

            else:
                if self.search_by.get() != "Select":
                    cur.execute("select student.id,name,class.classname,gender,dob,father,mother, \
                        phone,email,tAddr,pAddr,dor,prev_school,prev_class,status  FROM \
                        student, class where student."+str(self.search_by.get().lower())+" LIKE '%" +
                                str(self.search_txt.get())+"%'"+" and student.class_id = class.id")

                    rows = cur.fetchall()
                    if len(rows) == 0:
                        messagebox.showerror(
                            "Error", "No such Student's was found", parent=self.root)

            if len(rows) != 0:
                self.student_table.delete(*self.student_table.get_children())
                for row in rows:
                    row = list(row)
                    self.student_table.insert('', END, values=row)
                    con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def exporttoxls(self):
        try:
            op = messagebox.askyesno(
                "Confirm", "Do you really want to Export the Students Data?", parent=self.root)
            if op:
                files = [('xlsx files', '*.xlsx'), ("All Files", "*.*"), ]

                file = filedialog.asksaveasfilename(
                    title="Save a file", initialdir="/", filetypes=files, defaultextension=files, parent=self.root)

                if file != "":
                    con = sqlite3.connect("Database/sms.db")

                    with pd.ExcelWriter(file, engine="xlsxwriter") as writer:
                        df = pd.read_sql("select student.id,name,class.classname,gender,dob,father,mother, \
                        phone,email,tAddr,pAddr,dor,prev_school,prev_class,status  FROM \
                        student, class where student.class_id = class.id", con)
                        df.to_excel(writer, sheet_name="Sheet1",
                                    header=True, index=False)

                        messagebox.showinfo(
                            "Success", "File Exported Successfully", parent=self.root)

                    con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def bytes_to_nparr(self,byte_img):
        nparr = np.frombuffer(byte_img, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        return list(face_recognition.face_encodings(img)[0])


if __name__ == "__main__":
    root = Tk()
    obj = manage_students_Class(root)
    root.mainloop()
