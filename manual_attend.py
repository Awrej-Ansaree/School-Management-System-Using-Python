from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import nepali_datetime
import time
import io


class manual_attend_Class:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1050x520+300+130")
        self.root.resizable(0, 0)
        self.root.title("Manual Attendance")
        self.root.focus_force()
        self.root.grab_set()

        # =====All Variables=============
        self.date_var = StringVar()
        self.searchBy_var = StringVar()
        self.searchTxt_var = StringVar()
        self.mark_var = StringVar()
        self.date_var.set(nepali_datetime.date.today())

        self.image = ""
        self.id = ""
        self.name = ""
        self.stdclass = ""
        # self.sec = ""
        # self.medium = ""

        # ====Loading Background image====
        self.bg_img = Image.open("images/bg/img7.jpg")
        self.bg_img = self.bg_img.resize((1050, 520), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        # =======Designing UI========
        bg_lbl = Label(self.root, image=self.bg_img).place(
            x=0, y=0, relwidth=1)

        title = Label(self.root, text="Manual Attendance", font=(
            "goudy old style", 25, "bold"), bg="white").pack(side=TOP, fill=X, padx=5, pady=8)

        # ================================Frame - 1 Designing=======================================
        frame1 = Frame(self.root, bd=0)
        frame1.place(x=15, y=70, width=600, height=440)
        title_frame1 = Label(frame1, text="Student Details", font=(
            "goudy old style", 20, "bold"), bg="#001E41", fg="white").pack(fill=X)

        self.img_lbl = Label(frame1, text="Photo", bd=2,
                             relief=SOLID, font=("goudy old style", 15, "bold"))
        self.img_lbl.place(x=50, y=50, width=140, height=130)

        self.id_lbl = Label(frame1, text="ID:", font=("goudy old style", 15))
        self.id_lbl.place(x=50, y=180)

        self.name_lbl = Label(frame1, text="Name:",
                              font=("goudy old style", 15))
        self.name_lbl.place(x=50, y=210)

        self.class_lbl = Label(frame1, text="Class:",
                               font=("goudy old style", 15))
        self.class_lbl.place(x=50, y=240)

        # self.section_lbl = Label(
        #     frame1, text="Section:", font=("goudy old style", 15))
        # self.section_lbl.place(x=50, y=270)

        # self.medium_lbl = Label(frame1, text="Medium:",
        #                         font=("goudy old style", 15))
        # self.medium_lbl.place(x=50, y=300)

        date_lbl = Label(frame1, text="Date:", font=("goudy old style", 15))
        date_lbl.place(x=50, y=270)

        date_entry = Entry(frame1, textvariable=self.date_var, font=(
            "goudy old style", 15), bg="#F5F5F5", fg="black", width=10)
        date_entry.place(x=120, y=270)

        status_lbl = Label(frame1, text="Status:",
                           font=("goudy old style", 15))
        status_lbl.place(x=50, y=300)

        status_lbl = ttk.Combobox(frame1, textvariable=self.mark_var, values=(
            "Select", "Present", "Absent"), justify=CENTER, width=8, font=("goudy old style", 15, "bold"), state="readonly")
        status_lbl.place(x=120, y=300)
        status_lbl.current(0)

        self.btn_mark = Button(frame1, text="Mark", command=self.mark_attend, font=("goudy old style", 15, "bold"),
                               bg="lightgreen", fg="black", cursor="hand2", state=DISABLED)
        self.btn_mark.place(x=50, y=360, width=100, height=30)

        btn_clear = Button(frame1, text="Clear", command=self.clear, font=("goudy old style", 15, "bold"),
                           bg="lightblue", fg="black", cursor="hand2").place(x=160, y=360, width=100, height=30)

        dateFormat_lbl = Label(frame1, text="Note: Date Format Should be YYYY-MM-DD (2078-01-01)",
                               font=("goudy old style", 12), bg="#001E41", fg="lightblue").pack(fill=X, side=BOTTOM)

        # =============================Frame - 2 Designing====================================
        frame2 = Frame(self.root, bd=0, bg="#42587d")
        frame2.place(x=635, y=70, width=400, height=440)
        title_frame2 = Label(frame2, font=(
            "goudy old style", 20, "bold"), bg="#001E41", fg="white").pack(fill=X)

        search_lbl = Label(frame2, text="Search By", font=(
            "goudy old style", 15, "bold"), bg="#001E41", fg="white").place(x=5, y=5)
        search_by = ttk.Combobox(frame2, textvariable=self.searchBy_var, values=(
            "Select", "ID", "Name", "Class"), justify=CENTER, width=8, font=("goudy old style", 15, "bold"), state="readonly")
        search_by.place(x=100, y=5)
        search_by.current(0)
        search_txt = Entry(frame2, textvariable=self.searchTxt_var, font=(
            "goudy old style", 15, "bold"), bg="white", fg="black", relief=SOLID, width=14)
        search_txt.place(x=210, y=5)
        search_txt.bind("<Return>", self.search)

        # ==========================Creating TreeView or Table=============================

        # X scrollbar
        scroll_x = Scrollbar(frame2, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X, padx=1, pady=1)

        # Y scrollbar
        scroll_y = Scrollbar(frame2, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y, padx=1, pady=1)

        # table
        self.student_table = ttk.Treeview(frame2,
                                          columns=("id", "name", "class"),
                                          xscrollcommand=scroll_x.set,
                                          yscrollcommand=scroll_y.set)
        # configure Y scrollbar
        scroll_y.config(command=self.student_table.yview)
        scroll_x.config(command=self.student_table.xview)

        # table heading
        self.student_table.heading("id", text="ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("class", text="Class")
        # self.student_table.heading("status", text="Status")
        # self.student_table.heading("section", text="Section")
        # self.student_table.heading("medium", text="Medium")
        # show table heading
        self.student_table["show"] = "headings"
        # table column width
        self.student_table.column("id", width=50, anchor=CENTER)
        self.student_table.column("name", width=115, anchor=CENTER)
        self.student_table.column("class", width=115, anchor=CENTER)
        # self.student_table.column("status", width=115, anchor=CENTER)
        # self.student_table.column("section", width=80, anchor=CENTER)
        # self.student_table.column("medium", width=80, anchor=CENTER)
        self.student_table.pack(fill=BOTH, expand=1, padx=2, pady=2)
        self.student_table.bind("<ButtonRelease-1>", self.getdata)

        self.show()

    # =======================All Functions/Methods==========================
    def show(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            cur.execute("select student.id,student.name,class.classname from student \
                        INNER JOIN class ON student.class_id=class.id ORDER BY class.id")
            rows = cur.fetchall()
            if len(rows) != 0 or len(rows) == 0:
                self.student_table.delete(*self.student_table.get_children())
                for row in rows:
                    self.student_table.insert("", END, values=row)
                    con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def getdata(self, event):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            f = self.student_table.focus()
            content = (self.student_table.item(f))
            row = content["values"]
            if row != "":
                cur.execute("Select photo from student where id=? and name=?", (
                    row[0],
                    row[1],
                ))
                img = cur.fetchone()
                con.commit()

                size = (140, 130)
                self.image = io.BytesIO(img[0])
                self.image = Image.open(self.image)
                self.image = self.image.resize(size, Image.ANTIALIAS)
                self.image = ImageTk.PhotoImage(self.image)
                self.img_lbl.config(image=self.image)

                self.id_lbl.config(text=f"ID: {row[0]}")
                self.name_lbl.config(text=f"Name: {row[1]}")
                self.class_lbl.config(text=f"Class: {row[2]}")
                # self.section_lbl.config(text=f"Section: {row[3]}")
                # self.medium_lbl.config(text=f"Medium: {row[4]}")

                self.id = row[0]
                self.name = row[1]
                self.stdclass = row[2]
                # self.sec = row[3]
                # self.medium = row[4]

                self.btn_mark.config(state=NORMAL)

            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def clear(self):
        self.img_lbl.config(image="")
        self.id_lbl.config(text="ID:")
        self.name_lbl.config(text="Name:")
        self.class_lbl.config(text="Class:")
        # self.section_lbl.config(text="Section:")
        # self.medium_lbl.config(text="Medium:")
        self.date_var.set(nepali_datetime.date.today())
        self.searchBy_var.set("Select")
        self.mark_var.set("Select")
        self.searchTxt_var.set("")

        self.id = ""
        self.name = ""
        self.stdclass = ""
        # self.sec = ""
        # self.medium = ""

        self.btn_mark.config(state=DISABLED)

    def search(self, event):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            if self.searchBy_var.get() == "Select" or self.searchTxt_var.get() == "":
                self.show()
            else:
                cur.execute(f"Select student.id,name,classname from student INNER JOIN ON student.class_id=class.id where \
                            {self.searchBy_var.get().lower()} LIKE '%"+str(self.searchTxt_var.get())+"%' ORDER BY classname")
                rows = cur.fetchall()
                if len(rows) != 0 or len(rows) == 0:
                    self.student_table.delete(
                        *self.student_table.get_children())
                    for row in rows:
                        self.student_table.insert("", END, values=row)
                        con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def mark_attend(self):
        try:
            if self.mark_var.get() == "Select":
                messagebox.showerror(
                    "Error", "Please select the student attendance status", parent=self.root)

            else:
                if self.id == "" and self.name == "" and self.stdclass == "":
                    messagebox.showerror(
                        "Error", "Please select the Student from the List", parent=self.root)
                else:
                    con = sqlite3.connect("Database/sms.db")
                    cur = con.cursor()

                    currTime = time.strftime("%I:%M:%S %p")

                    cur.execute("Select * from attendance where std_id=? and date=?",
                                (self.id, self.date_var.get(),))
                    row = cur.fetchone()

                    if row == None:

                        cur.execute("Insert into attendance (std_id,date,status) values(?,?,?)", (
                            self.id,
                            self.date_var.get(),
                            self.mark_var.get(),
                        ))
                        con.commit()
                        messagebox.showinfo(
                            "Success", "Attendance was Marked Successfully", parent=self.root)

                    else:
                        op = messagebox.askyesno(
                            "Confirm", f"Do you really want to update the {self.name} attendance?", parent=self.root)
                        if op:
                            cur.execute("update attendance set status=? where id=? and date=?", (
                                self.mark_var.get(),
                                self.id,
                                self.date_var.get(),
                            ))
                            con.commit()
                            messagebox.showinfo(
                                "Success", "Attendance was updated successfully", parent=self.root)

                    con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to: {e}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = manual_attend_Class(root)
    root.mainloop()
