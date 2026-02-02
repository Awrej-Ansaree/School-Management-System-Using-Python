from email import message
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import pandas as pd
import xlsxwriter


class manage_class_Class:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1050x520+300+130")
        self.root.resizable(0, 0)
        self.root.title("Manage Class & Fee")
        self.root.focus_force()
        self.root.grab_set()

        # =========All Variables=======
        self.Classid_var = IntVar()
        self.classname_var = StringVar()
        self.feetypeid_var = StringVar()
        self.feetypename_var = StringVar()
        self.feeid_var = IntVar()
        self.feeClassname_var = StringVar()
        self.feeFeename_var = StringVar()
        self.feeamount_var = StringVar()

        # =================Loading Images=======================
        self.img1 = Image.open("images/class_img2.jpg")
        self.img1 = self.img1.resize((180, 100), Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(self.img1)

        self.img2 = Image.open("images/class_img1.jpg")
        self.img2 = self.img2.resize((180, 100), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(self.img2)

        self.img3 = Image.open("images/class_img7.jpg")
        self.img3 = self.img3.resize((180, 100), Image.ANTIALIAS)
        self.img3 = ImageTk.PhotoImage(self.img3)

        self.img4 = Image.open("images/class_img6.jpg")
        self.img4 = self.img4.resize((180, 100), Image.ANTIALIAS)
        self.img4 = ImageTk.PhotoImage(self.img4)

        self.img5 = Image.open("images/class_img8.jpg")
        self.img5 = self.img5.resize((180, 100), Image.ANTIALIAS)
        self.img5 = ImageTk.PhotoImage(self.img5)

        self.bg_img = Image.open("images/bg/img16.jpg")
        self.bg_img = self.bg_img.resize((1050, 520), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        # ==============================Designing UI=============================
        bg_lbl = Label(self.root, image=self.bg_img).place(
            x=0, y=0, relwidth=1)

        lbl_title = Label(self.root, text="Manage Class & Fee", font=(
            "goudy old style", 25, "bold"), bg="white").pack(side=TOP, fill=X, padx=10, pady=10)

        # ------------------------Images Labels-------------------------------
        # self.lbl_img1 = Label(self.root, image=self.img1, bd=2, relief=RAISED)
        # self.lbl_img1.place(x=15, y=75)

        # self.lbl_img2 = Label(self.root, image=self.img2, bd=2, relief=RAISED)
        # self.lbl_img2.place(x=225, y=75)

        # self.lbl_img3 = Label(self.root, image=self.img3, bd=2, relief=RAISED)
        # self.lbl_img3.place(x=435, y=75)

        self.lbl_img4 = Label(self.root, image=self.img4, bd=2, relief=RAISED)
        self.lbl_img4.place(x=650, y=75)

        self.lbl_img5 = Label(self.root, image=self.img5, bd=2, relief=RAISED)
        self.lbl_img5.place(x=850, y=75)

        # =================================Frame - 1================================
        frame1 = Frame(self.root, bd=0, bg="lightgray", padx=10, pady=15)
        frame1.place(x=10, y=75, width=428, height=438)

        # --------------------------------Class Frame-----------------------------------------
        Class_Frame = LabelFrame(
            frame1, text="Class", bd=1, bg="white", font=("goudy old style", 12))
        Class_Frame.pack(fill=X, padx=5)

        lbl_Class = Label(Class_Frame, text="Class", font=(
            "goudy old style", 18), bg="white")
        lbl_Class.grid(row=0, column=0, pady=10, padx=5, sticky="w")

        self.txt_Class = Entry(Class_Frame, textvariable=self.classname_var, font=(
            "goudy old style", 15), justify=CENTER, width=15, bg="lightyellow")
        self.txt_Class.grid(row=0, column=1, pady=10, padx=5, sticky="w")

        btnsaveclass = Button(Class_Frame, text="Save", command=self.save_Class, font=("goudy old style", 11, "bold"),
                              bg="#2370db", fg="white", cursor="hand2", width=9, bd=0).grid(row=0, column=2, padx=2, sticky="w")
        btndeleteclass = Button(Class_Frame, text="Delete", command=self.deleteClass, font=("goudy old style", 11, "bold"),
                                bg="#f73939", fg="white", cursor="hand2", width=9, bd=0).grid(row=0, column=3, padx=2, sticky="w")

        # -----------------------------Class Table and Scroll Bar----------------------------
        ClassTable_Frame = Frame(frame1, bd=0, bg="white")
        ClassTable_Frame.pack(fill=X, padx=5)
        scroll_y = Scrollbar(ClassTable_Frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.class_table = ttk.Treeview(ClassTable_Frame,
                                        columns=("id", "class"),
                                        yscrollcommand=scroll_y.set, height=5)
        scroll_y.config(command=self.class_table.yview)

        self.class_table.heading("id", text="ID")
        self.class_table.heading("class", text="Class")
        self.class_table["show"] = "headings"

        self.class_table.column("id", width=50, anchor=CENTER)
        self.class_table.column("class", width=125, anchor=CENTER)
        self.class_table.pack(fill=BOTH, expand=1)
        self.class_table.bind("<ButtonRelease-1>", self.getclassData)

        # --------------------------------FeeType Frame--------------------------------------------
        feetype_Frame = LabelFrame(frame1, text="Fee Type", bd=1,
                                   bg="white", font=("goudy old style", 12))
        feetype_Frame.pack(fill=X, padx=5, pady=0)

        lbl_feetype = Label(feetype_Frame, text="Name", font=(
            "goudy old style", 18), bg="white")
        lbl_feetype.grid(row=0, column=0, pady=10, padx=5, sticky="w")

        txt_feetype = Entry(feetype_Frame, textvariable=self.feetypename_var, font=(
            "goudy old style", 15), justify=CENTER, width=14, bg="lightyellow")
        txt_feetype.grid(row=0, column=1, pady=10, padx=5, sticky="w")

        btnsavefee = Button(feetype_Frame, text="Save", command=self.save_feetype, font=("goudy old style", 11, "bold"),
                            bg="#2370db", fg="white", cursor="hand2", width=9, bd=0).grid(row=0, column=2, padx=2, sticky="w")
        btndeletefeetype = Button(feetype_Frame, text="Delete", command=self.deletefeetype, font=("goudy old style", 11, "bold"),
                                  bg="#f73939", fg="white", cursor="hand2", width=9, bd=0).grid(row=0, column=3, padx=2, sticky="w")

        # -----------------------------FeeType Table and Scroll Bar----------------------------
        feeTable_Frame = Frame(frame1, bd=0, bg="white")
        feeTable_Frame.pack(fill=X, padx=5)
        scroll_y = Scrollbar(feeTable_Frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.feetype_table = ttk.Treeview(feeTable_Frame,
                                          columns=("id", "fee"),
                                          yscrollcommand=scroll_y.set, height=5)
        scroll_y.config(command=self.feetype_table.yview)

        self.feetype_table.heading("id", text="ID")
        self.feetype_table.heading("fee", text="Fee")
        self.feetype_table["show"] = "headings"

        self.feetype_table.column("id", width=50, anchor=CENTER)
        self.feetype_table.column("fee", width=125, anchor=CENTER)
        self.feetype_table.pack(fill=BOTH, expand=1)
        self.feetype_table.bind("<ButtonRelease-1>", self.getfeetypeData)

        # =================================Frame - 2================================
        frame2 = Frame(self.root, bd=0, bg="#ded9bf", padx=10, pady=15)
        frame2.place(x=442, y=198, width=598, height=315)

        # --------------------------------Fee Frame----------------------------------
        fee_Frame = LabelFrame(
            frame2, text="Fees", bd=1, bg="white", fg="black", font=("goudy old style", 12), padx=4)
        fee_Frame.pack(fill=X, padx=2)

        self.select_Class = ttk.Combobox(fee_Frame, values=("Select Class",), textvariable=self.feeClassname_var, font=(
            "goudy old style", 15), justify=CENTER, state="readonly", width=13)
        self.select_Class.grid(row=0, column=0, pady=10, padx=2, sticky="w")
        self.select_Class.current(0)

        self.select_feetype = ttk.Combobox(fee_Frame, values=("Select Fee",), textvariable=self.feeFeename_var, font=(
            "goudy old style", 15), justify=CENTER, state="readonly", width=13)
        self.select_feetype.grid(row=0, column=1, pady=10, padx=2, sticky="w")
        self.select_feetype.current(0)

        txt_clfamount = Entry(fee_Frame, textvariable=self.feeamount_var, font=(
            "goudy old style", 16), width=8, bg="lightyellow")
        txt_clfamount.grid(row=0, column=2, pady=10, padx=4, sticky="w")

        saveclassfee = Button(fee_Frame, text="Save", command=self.save_fee, font=("goudy old style", 11, "bold"),
                              bg="#2370db", fg="white", cursor="hand2", width=8, bd=0).grid(row=0, column=3, pady=10, padx=4, sticky="w")
        deletefee = Button(fee_Frame, text="Delete", command=self.deletefee, font=("goudy old style", 11, "bold"),
                           bg="#f73939", fg="white", cursor="hand2", width=8, bd=0).grid(row=0, column=4, pady=10, padx=4, sticky="w")

        # --------------------------------Fee Table-----------------------------------
        # ----------------------First Fee Table-------------------------------
        feeTable_Frame = Frame(frame2, bd=0, bg="white")
        feeTable_Frame.pack(fill=X, padx=2)

        scroll_y = Scrollbar(feeTable_Frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.fee_table = ttk.Treeview(feeTable_Frame,
                                      columns=("id", "class",
                                               "fee", "amount"),
                                      yscrollcommand=scroll_y.set, height=3)
        scroll_y.config(command=self.class_table.yview)

        self.fee_table.heading("id", text="ID")
        self.fee_table.heading("class", text="Class")
        self.fee_table.heading("fee", text="Fee")
        self.fee_table.heading("amount", text="Amount")
        self.fee_table["show"] = "headings"

        self.fee_table.column("id", width=50, anchor=CENTER)
        self.fee_table.column("class", width=115, anchor=CENTER)
        self.fee_table.column("fee", width=100, anchor=CENTER)
        self.fee_table.column("amount", width=80, anchor=CENTER)
        self.fee_table.pack(fill=BOTH, expand=1)
        self.fee_table.bind("<ButtonRelease-1>", self.getfeeData)

        # ----------------------Second Fee Table-------------------------------
        feeTable_Frame2 = Frame(frame2, bd=0, bg="white")
        feeTable_Frame2.pack(fill=X, padx=2)

        scroll_y = Scrollbar(feeTable_Frame2, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.fee_table2 = ttk.Treeview(feeTable_Frame2,
                                       columns=("id", "fee", "amount"),
                                       yscrollcommand=scroll_y.set, height=3)
        scroll_y.config(command=self.class_table.yview)

        self.fee_table2.heading("id", text="ID")
        self.fee_table2.heading("fee", text="Fee")
        self.fee_table2.heading("amount", text="Amount")
        self.fee_table2["show"] = "headings"

        self.fee_table2.column("id", width=50, anchor=CENTER)
        self.fee_table2.column("fee", width=100, anchor=CENTER)
        self.fee_table2.column("amount", width=80, anchor=CENTER)
        self.fee_table2.pack(fill=BOTH, expand=1)
        self.fee_table2.bind("<ButtonRelease-1>", self.getfeeData2)

        clearbtn = Button(frame2, text="Clear", command=self.clearbtn, font=("goudy old style", 11, "bold"),
                          bg="blue", fg="white", cursor="hand2", width=10, bd=0).pack(side="right", padx=10, pady=5)
        exportbtn = Button(frame2, text="Export", command=self.exporttoxls, font=("goudy old style", 11, "bold"),
                           bg="#0cb032", fg="white", cursor="hand2", width=10, bd=0).pack(side="right", padx=10, pady=5)

        # --------Calling the Functions to Load the Data----------
        self.showClass()
        self.showfeetype()
        self.getfeelist()
        self.showfee()
        self.showfee2()

    # --------------------------All Functions/Methods-----------------------
    # -------------Save Functions------------
    def save_Class(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            if len(self.classname_var.get()) <= 0:
                messagebox.showerror(
                    "Error", "Class name is required", parent=self.root)

            else:
                cur.execute("Select id from class where classname=?",
                            (self.classname_var.get(),))
                row = cur.fetchone()
                if row != None:
                    self.Classid_var.set(row[0])
                    op = messagebox.askyesno(
                        "Error", "Class is already present.\nPlease try different or Press 'yes' to update the record", parent=self.root)

                    if op:
                        cur.execute("update class set classname=?,session_id=? where id=?", (
                                    self.classname_var.get(), 1, self.Classid_var.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Success", "Class Updated Successfully", parent=self.root)

                else:
                    cur.execute("Insert into class (classname,session_id) values(?,?)", (
                        self.classname_var.get(),
                        1,
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Class Saved Successfully", parent=self.root)
                    self.classname_var.set("")
            con.close()
            self.showClass()
            self.getfeelist()
            self.clear()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def save_feetype(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            if len(self.feetypename_var.get()) <= 0:
                messagebox.showerror(
                    "Error", "Fee name is required", parent=self.root)

            else:
                cur.execute("Select id from feetype where feetypename=?",
                            (self.feetypename_var.get(),))
                row = cur.fetchone()
                if row != None:
                    self.feetypeid_var.set(row[0])
                    op = messagebox.askyesno(
                        "Error", "Fee Type is already present.\nDo Please try different.", parent=self.root)

                    if op:
                        cur.execute("update fee set classname=?,session_id=? where id=?", (
                                    self.feetypename_var.get(), 1, self.feetypeid_var.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Success", "Class Updated Successfully", parent=self.root)

                else:
                    cur.execute("Insert into feetype (feetypename,session_id) values(?,?)", (
                        self.feetypename_var.get(),
                        1,
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Fee Saved Successfully", parent=self.root)
                    self.feetypename_var.set("")
            con.close()
            self.showfeetype()
            self.getfeelist()
            self.clear()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def save_fee(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            if len(self.feeFeename_var.get()) <= 0 or len(self.feeamount_var.get()) <= 0:
                messagebox.showerror(
                    "Error", "Fee Type & Fee Amount both are required.\n Please try again!", parent=self.root)

            else:
                cur.execute("Select id from class where classname=?",
                            (self.feeClassname_var.get(),))
                idclass = cur.fetchone()

                cur.execute("Select id from feetype where feetypename=?",
                            (self.feeFeename_var.get(),))
                idfee = cur.fetchone()

                if idfee == None:
                    messagebox.showerror(
                        "Error", "Please select Class or Fee Type and try again.", parent=self.root)

                else:
                    if idclass == None:
                        cur.execute("Select id from fee where feetype_id=?",
                                    (idfee[0],))
                        row = cur.fetchone()

                    else:
                        cur.execute("Select id from fee where class_id=? and feetype_id=?",
                                    (idclass[0], idfee[0],))
                        row = cur.fetchone()

                    if row != None:
                        self.feeid_var.set(row[0])
                        op = messagebox.askyesno(
                            "Error", "Fee is already present.\nPlease try different or Press 'yes' to update the record", parent=self.root)

                        if op:
                            if idclass != None:
                                cur.execute("update fee set class_id=?,feetype_id=?,amount=? where id=?", (
                                    idclass[0], idfee[0], self.feeamount_var.get(), self.feeid_var.get(),))
                                con.commit()
                                messagebox.showinfo(
                                    "Success", "Fee Updated Successfully", parent=self.root)
                            else:
                                cur.execute("update fee set feetype_id=?,amount=? where id=?", (
                                    idfee[0], self.feeamount_var.get(), self.feeid_var.get(),))
                                con.commit()
                                messagebox.showinfo(
                                    "Success", "Fee Updated Successfully", parent=self.root)

                    else:
                        if idclass != None:
                            cur.execute("Insert into fee (class_id,feetype_id,amount) values(?,?,?)", (
                                idclass[0],
                                idfee[0],
                                self.feeamount_var.get(),
                            ))
                            con.commit()
                            messagebox.showinfo(
                                "Success", "Fee Saved Successfully", parent=self.root)

                        else:
                            cur.execute("Insert into fee (feetype_id,amount) values(?,?)", (
                                idfee[0],
                                self.feeamount_var.get(),
                            ))
                            con.commit()
                            messagebox.showinfo(
                                "Success", "Fee Saved Successfully", parent=self.root)

            con.close()
            self.getfeelist()
            self.showfee()
            self.showfee2()
            self.clear()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    # -------------Show Functions------------

    def showClass(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            cur.execute(
                "select id, classname from class where session_id=1 ORDER BY id,classname")
            rows = cur.fetchall()
            if len(rows) != 0 or len(rows) == 0:
                self.class_table.delete(*self.class_table.get_children())
                for row in rows:
                    self.class_table.insert("", END, values=row)
                    con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def showfeetype(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            cur.execute(
                "select id, feetypename from feetype where session_id=1 ORDER BY id,feetypename")
            rows = cur.fetchall()
            if len(rows) != 0 or len(rows) == 0:
                self.feetype_table.delete(*self.feetype_table.get_children())
                for row in rows:
                    self.feetype_table.insert("", END, values=row)
                    con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def showfee(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT fee.id, class.classname, feetype.feetypename, fee.amount FROM \
                    fee, feetype, class where fee.feetype_id = feetype.id and fee.class_id = class.id")
            rows = cur.fetchall()
            if len(rows) != 0 or len(rows) == 0:
                self.fee_table.delete(*self.fee_table.get_children())
                for row in rows:
                    self.fee_table.insert("", END, values=row)
                    con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def showfee2(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT fee.id, feetype.feetypename, fee.amount FROM \
                    fee, feetype where fee.class_id IS NULL and fee.feetype_id = feetype.id")
            rows = cur.fetchall()
            if len(rows) != 0 or len(rows) == 0:
                self.fee_table2.delete(
                    *self.fee_table2.get_children())
                for row in rows:
                    self.fee_table2.insert("", END, values=row)
                    con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    # -----------Get Functions----------------

    def getclassData(self, event):
        f = self.class_table.focus()
        content = (self.class_table.item(f))
        row = content["values"]
        if row != "":
            self.Classid_var.set(row[0])
            self.classname_var.set(row[1])

    def getfeetypeData(self, event):
        f = self.feetype_table.focus()
        content = (self.feetype_table.item(f))
        row = content["values"]
        if row != "":
            self.feetypeid_var.set(row[0])
            self.feetypename_var.set(row[1])

    def getfeelist(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            cur.execute(
                "select classname from class where session_id=1 ORDER BY id,classname")
            Classrows = cur.fetchall()
            Classlist = ["Select Class"]
            if len(Classrows) != 0 or len(Classrows) == 0:
                for row in Classrows:
                    Classlist.append(row[0])
            self.select_Class.config(values=Classlist)

            cur.execute(
                "select feetypename from feetype where session_id=1 ORDER BY id,feetypename")
            feerows = cur.fetchall()
            feelist = ["Select Fee"]
            if len(feerows) != 0 or len(feerows) == 0:
                for row in feerows:
                    feelist.append(row[0])
            self.select_feetype.config(values=feelist)

            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def getfeeData(self, event):
        f = self.fee_table.focus()
        content = (self.fee_table.item(f))
        row = content["values"]
        if row != "":
            self.feeid_var.set(row[0])
            self.feeClassname_var.set(row[1])
            self.feeFeename_var.set(row[2])
            self.feeamount_var.set(row[3])

    def getfeeData2(self, event):
        f = self.fee_table2.focus()
        content = (self.fee_table2.item(f))
        row = content["values"]
        if row != "":
            self.feeid_var.set(row[0])
            self.select_Class.current(0)
            self.feeFeename_var.set(row[1])
            self.feeamount_var.set(row[2])

    # ----------Delete Functions---------------
    def deleteClass(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            if self.Classid_var.get() == "":
                messagebox.showerror(
                    "Error", "Please select class from the list", parent=self.root)
            else:
                cur.execute("select * from class where id=?",
                            (self.Classid_var.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Please try again", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do you really want to delete\nif 'yes' all the related record will be deleted?", parent=self.root)
                    if op:
                        cur.execute("delete from class where id=?",
                                    (self.Classid_var.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Success", "Class Deleted Successfully", parent=self.root)
                        self.showClass()
                        self.getfeelist()
                        self.showfee()
                        self.clear()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def deletefeetype(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            if self.feetypeid_var.get() == "":
                messagebox.showerror(
                    "Error", "Please select Fee from the list", parent=self.root)
            else:
                cur.execute("select * from feetype where id=?",
                            (self.feetypeid_var.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Please try again", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do you really want to delete\nif 'yes' all the related record will be deleted?", parent=self.root)
                    if op:
                        cur.execute("delete from feetype where id=?",
                                    (self.feetypeid_var.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Success", "Fee Type Deleted Successfully", parent=self.root)
                        self.showfeetype()
                        self.getfeelist()
                        self.showfee()
                        self.clear()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def deletefee(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            if self.feeid_var.get() == "":
                messagebox.showerror(
                    "Error", "Please select Fee from the list", parent=self.root)
            else:
                cur.execute("select * from fee where id=?",
                            (self.feeid_var.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Please try again", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("delete from fee where id=?",
                                    (self.feeid_var.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Success", "Deleted Successfully", parent=self.root)
                        self.showfeetype()
                        self.getfeelist()
                        self.showfee()
                        self.showfee2()
                        self.clear()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    # --------Clear Functions-------------------
    def clear(self):
        try:
            self.Classid_var.set("")
            self.feetypeid_var.set("")
            self.feeid_var.set("")
            self.classname_var.set("")
            self.feetypename_var.set("")
            self.select_Class.current(0)
            self.select_feetype.current(0)
            self.feeamount_var.set("")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def clearbtn(self):
        op = messagebox.askyesno(
            "Confirm", "Do you really want to clear?", parent=self.root)
        if op:
            self.clear()

    # -----------Export Function---------------
    def exporttoxls(self):
        try:
            op = messagebox.askyesno(
                "Confirm", "Do you really want to Export the Fee Data?", parent=self.root)
            if op:
                files = [('xlsx files', '*.xlsx'), ("All Files", "*.*"), ]

                file = filedialog.asksaveasfilename(
                    title="Save a file", initialdir="/", filetypes=files, defaultextension=files, parent=self.root)

                if file != "":
                    con = sqlite3.connect("Database/sms.db")

                    with pd.ExcelWriter(file, engine="xlsxwriter") as writer:
                        df = pd.read_sql("SELECT fee.id, class.classname, feetype.feetypename, fee.amount FROM \
                            fee, feetype, class where fee.feetype_id = feetype.id and fee.class_id = class.id", con)
                        df.to_excel(writer, sheet_name="Class Fee",
                                    header=True, index=False)

                        df = pd.read_sql("SELECT fee.id, feetype.feetypename, fee.amount FROM \
                           fee, feetype where fee.class_id IS NULL and fee.feetype_id = feetype.id", con)
                        df.to_excel(writer, sheet_name="Other Fee",
                                    header=True, index=False)

                        messagebox.showinfo(
                            "Success", "File Exported Successfully", parent=self.root)

                    con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = manage_class_Class(root)
    root.mainloop()
