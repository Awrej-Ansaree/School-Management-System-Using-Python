from tkinter import *
from tkinter import ttk, messagebox
from unicodedata import name
from PIL import Image, ImageTk
import sqlite3


class manage_class_Class:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1050x520+300+130")
        self.root.resizable(0, 0)
        self.root.title("Billing")
        self.root.focus_force()
        self.root.grab_set()

        # =========All Variables=======
        self.Classid_var = StringVar()
        self.Class_var = StringVar()
        self.Section_var = StringVar()
        self.Section = ""
        self.Medium_var = StringVar()
        self.Medium = ""
        self.Fee_var = IntVar()
        self.NOS_var = IntVar()  # No. of Subject(NOS)
        self.search_txt = StringVar()

        self.bg_img = Image.open("images/bg/img2.jpg")
        self.bg_img = self.bg_img.resize((1050, 520), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        # ==============================Designing UI=============================
        bg_lbl = Label(self.root, image=self.bg_img).place(
            x=0, y=0, relwidth=1)

        lbl_title = Label(self.root, text="Billing", font=(
            "goudy old style", 25, "bold"), bg="white").pack(side=TOP, fill=X, padx=10, pady=7)

        # ================= Frame-1 ==================================
        frame1 = Frame(self.root, bd=0, bg="white", padx=10, pady=15)
        frame1.place(x=20, y=60, width=300, height=450)

        # frame1title = Label(frame1, text="Details", font=(
        #     "goudy old style", 12, "bold"), bg="white").grid(row=0, columnspan=2, sticky=N, pady=0)

        searchby = ttk.Combobox(frame1, font=(
            "goudy old style", 15), width=8, state="readonly", justify=CENTER)
        searchby["values"] = ("Search By", "ID", "Name", "Phone", "Father")
        searchby.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        searchby.current(0)

        searchby_txt = Entry(frame1, font=(
            "goudy old style", 15), width=15, bd=1, relief=SOLID)
        searchby_txt.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        id_lbl = Label(frame1, text="ID", bg="white", font=(
            "goudy old style", 15)).grid(row=2, column=0, padx=5, pady=5, sticky=W)

        id_txt = Entry(frame1, font=(
            "goudy old style", 15), width=15, bd=1, relief=SOLID)
        id_txt.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        name_lbl = Label(frame1, text="Name", bg="white", font=(
            "goudy old style", 15)).grid(row=3, column=0, padx=5, pady=5, sticky=W)

        name_txt = Entry(frame1, font=(
            "goudy old style", 15), width=15, bd=1, relief=SOLID)
        name_txt.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        lblclass = Label(frame1, text="Class", bg="white", font=(
            "goudy old style", 15)).grid(row=4, column=0, padx=5, pady=5, sticky=W)

        txtclass = Entry(frame1, font=(
            "goudy old style", 15), width=15, bd=1, relief=SOLID)
        txtclass.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        lblphone = Label(frame1, text="Phone", bg="white", font=(
            "goudy old style", 15)).grid(row=5, column=0, padx=5, pady=5, sticky=W)

        txtphone = Entry(frame1, font=(
            "goudy old style", 15), width=15, bd=1, relief=SOLID)
        txtphone.grid(row=5, column=1, padx=5, pady=5, sticky=W)

        lblfeetype = Label(frame1, text="FeeType", bg="white", font=(
            "goudy old style", 15)).grid(row=6, column=0, padx=5, pady=5, sticky=W)

        selectFeeType = ttk.Combobox(frame1, font=(
            "goudy old style", 15), width=13, state="readonly", justify=CENTER)
        selectFeeType["values"] = (
            "Select", "Monthly", "Annual", "Bus", "Other")
        selectFeeType.grid(row=6, column=1, padx=5, pady=5, sticky=W)
        selectFeeType.current(0)

        lblMonth = Label(frame1, text="Month", bg="white", font=(
            "goudy old style", 15)).grid(row=7, column=0, padx=5, pady=5, sticky=W)

        selectMonth = ttk.Combobox(frame1, font=(
            "goudy old style", 15), width=13, state="readonly", justify=CENTER)
        selectMonth["values"] = (
            "Select", "Baishakh", "Jestha", "Ashadh", "Shrawan", "Bhadau", "Ashwin", "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra")
        selectMonth.grid(row=7, column=1, padx=5, pady=5, sticky=W)
        selectMonth.current(0)

        lblcharge = Label(frame1, text="Charge", bg="white", font=(
            "goudy old style", 15)).grid(row=8, column=0, padx=5, pady=5, sticky=W)

        txtCharge = Entry(frame1, font=(
            "goudy old style", 15), width=15, bd=1, relief=SOLID)
        txtCharge.grid(row=8, column=1, padx=5, pady=5, sticky=W)

        lblamount = Label(frame1, text="Amount", bg="white", font=(
            "goudy old style", 15)).grid(row=9, column=0, padx=5, pady=5, sticky=W)

        txtAmount = Entry(frame1, font=(
            "goudy old style", 15), width=15, bd=1, relief=SOLID)
        txtAmount.grid(row=9, column=1, padx=5, pady=5, sticky=W)

        lblbalance = Label(frame1, text="Balance", bg="white", font=(
            "goudy old style", 15)).grid(row=10, column=0, padx=5, pady=5, sticky=W)

        txtBalance = Entry(frame1, font=(
            "goudy old style", 15), width=15, bd=1, relief=SOLID)
        txtBalance.grid(row=10, column=1, padx=5, pady=5, sticky=W)

    # ==============All Functions/Methods================

    def add(self):
        con = sqlite3.connect("sms.db")
        cur = con.cursor()
        try:
            if self.Class_var.get() == "":
                messagebox.showerror(
                    "Error", "Class name is required", parent=self.root)

            elif self.NOS_var.get() == 0:
                messagebox.showerror(
                    "Error", "No. of Subjects is required", parent=self.root)

            elif self.Fee_var.get() == 0:
                messagebox.showerror(
                    "Error", "Fee is required", parent=self.root)

            else:
                if self.Medium_var.get() == "Medium":
                    self.Medium = "Null"
                else:
                    self.Medium = self.Medium_var.get()

                if self.Section_var.get() == "Section":
                    self.Section = "Null"
                else:
                    self.Section = self.Section_var.get()

                cur.execute("Select * from class where class=? and section=? and medium=?",
                            (self.Class_var.get(), self.Section, self.Medium,))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "Class is already present, try different", parent=self.root)
                else:
                    cur.execute("Insert into class (class,section,medium,fee,nos) values(?,?,?,?,?)", (
                        self.Class_var.get(),
                        self.Section,
                        self.Medium,
                        self.Fee_var.get(),
                        self.NOS_var.get(),
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Class Added Successfully", parent=self.root)
                    self.clear()
                    self.show()
            con.close()
        except TclError:
            messagebox.showerror(
                "Error", f"Invalid Fee or No. of Subject!", parent=self.root)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def show(self):
        con = sqlite3.connect("sms.db")
        cur = con.cursor()
        try:
            cur.execute("select * from class ORDER BY class,section")
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

    def getdata(self, event):
        f = self.class_table.focus()
        content = (self.class_table.item(f))
        row = content["values"]
        if row != "":
            self.Classid_var.set(row[0])
            self.Class_var.set(row[1])
            if row[2] == "" or row[2] == " " or row[2] == "Null" or row[2] == "None":
                self.Section_var.set("Section")
            else:
                self.Section_var.set(row[2])
            if row[3] == "" or row[3] == " " or row[3] == "Null" or row[3] == "None":
                self.Medium_var.set("Medium")
            else:
                self.Medium_var.set(row[3])
            self.Fee_var.set(row[4])
            self.NOS_var.set(row[5])

    def clear(self):
        self.Classid_var.set("")
        self.Class_var.set("")
        self.Section = ""
        self.Section_var.set("Section")
        self.Medium = ""
        self.Medium_var.set("Medium")
        self.Fee_var.set(0)
        self.NOS_var.set(0)
        self.search_txt.set("")

    def update(self):
        con = sqlite3.connect("sms.db")
        cur = con.cursor()
        try:
            if self.Classid_var.get() == "":
                messagebox.showerror(
                    "Error", "Please select class from the list", parent=self.root)
            else:
                if self.Medium_var.get() == "Medium":
                    self.Medium = "Null"
                else:
                    self.Medium = self.Medium_var.get()

                if self.Section_var.get() == "Section":
                    self.Section = "Null"
                else:
                    self.Section = self.Section_var.get()

                cur.execute("select * from class where id=?",
                            (self.Classid_var.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Please try again", parent=self.root)

                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do you really want to update?", parent=self.root)
                    if op:
                        cur.execute("update class set class=?,section=?,medium=?,fee=?,nos=? where id=?", (self.Class_var.get(
                        ), self.Section, self.Medium, self.Fee_var.get(), self.NOS_var.get(), self.Classid_var.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Success", "Class Updated Successfully", parent=self.root)
                        self.clear()
                        self.show()
            con.close()
        except TclError:
            messagebox.showerror(
                "Error", f"Invalid Fee or of No. of Subject!", parent=self.root)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect("sms.db")
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
                        "Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("delete from class where id=?",
                                    (self.Classid_var.get(),))
                        con.commit()
                        messagebox.showinfo(
                            "Success", "Class Deleted Successfully", parent=self.root)
                        self.clear()
                        self.show()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def search(self):
        con = sqlite3.connect("sms.db")
        cur = con.cursor()
        try:
            cur.execute("select * from class where class LIKE '%" +
                        str(self.search_txt.get())+"%'  ORDER BY class,section")
            rows = cur.fetchall()
            if len(rows) != 0:
                self.class_table.delete(*self.class_table.get_children())
                for row in rows:
                    self.class_table.insert("", END, values=row)
                    con.commit()
            else:
                messagebox.showerror(
                    "Error", "Class wasn't found", parent=self.root)

            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = manage_class_Class(root)
    root.mainloop()
