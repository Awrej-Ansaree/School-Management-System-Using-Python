from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import nepali_datetime
import time
import io


class manage_attend_Class:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1050x520+300+130")
        self.root.resizable(0, 0)
        self.root.title("Manage Attendance")
        self.root.focus_force()
        self.root.grab_set()

        # ===============All Variables============
        self.searchtxt_var = StringVar()

        # ====Loading Background image====
        self.bg_img = Image.open("images/bg/img2.jpg")
        self.bg_img = self.bg_img.resize((1050, 520), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        # =======Designing UI========
        bg_lbl = Label(self.root, image=self.bg_img).place(
            x=0, y=0, relwidth=1)

        title = Label(self.root, text="Manage Attendance", font=(
            "goudy old style", 25, "bold"), bg="white").pack(side=TOP, fill=X, padx=5, pady=8)

        # ================================Frame - 1 Designing=======================================
        frame1 = Frame(self.root, bd=0, bg="#42587d")
        frame1.place(x=15, y=70, width=600, height=440)
        title_frame1 = Label(frame1, text="Students Attendance Details", font=(
            "goudy old style", 20, "bold"), bg="#001E41", fg="white").pack(fill=X)

        # =========Students Attendance Table and Scroll Bar=====================
        # X scrollbar
        attend_scroll_x = Scrollbar(frame1, orient=HORIZONTAL)
        attend_scroll_x.pack(side=BOTTOM, fill=X, padx=1, pady=1)

        # Y scrollbar
        attend_scroll_y = Scrollbar(frame1, orient=VERTICAL)
        attend_scroll_y.pack(side=RIGHT, fill=Y, pady=1, padx=1)

        # table
        self.stdAttend_table = ttk.Treeview(frame1,
                                            columns=("id", "name", "date", "status"),
                                            xscrollcommand=attend_scroll_x.set,
                                            yscrollcommand=attend_scroll_y.set)
        # configure Y scrollbar
        attend_scroll_y.config(command=self.stdAttend_table.yview)
        attend_scroll_x.config(command=self.stdAttend_table.xview)

        # table heading
        self.stdAttend_table.heading("id", text="ID")
        self.stdAttend_table.heading("name", text="Name")
        self.stdAttend_table.heading("date", text="Date")
        self.stdAttend_table.heading("status", text="Status")
        # show table heading
        self.stdAttend_table["show"] = "headings"
        # table column width
        self.stdAttend_table.column("id", width=50, anchor=CENTER)
        self.stdAttend_table.column("name", width=150, anchor=CENTER)
        self.stdAttend_table.column("date", width=80, anchor=CENTER)
        self.stdAttend_table.column("status", width=80, anchor=CENTER)

        self.stdAttend_table.pack(fill=BOTH, expand=1, padx=1, pady=1)

        # =============================Frame - 2 Designing====================================
        frame2 = Frame(self.root, bd=0, bg="#42587d")
        frame2.place(x=640, y=70, width=400, height=440)

        # ==========Search by=========
        search_Framelbl = Label(frame2, font=(
            "goudy old style", 20, "bold"), bg="#001E41", fg="white").pack(fill=X)

        search_by = Label(frame2, text="Class", font=(
            "times new roman", 20, "bold"), bg="#001E41", fg="white")
        search_by.place(x=10, y=2)

        self.search_txt = Entry(
            frame2, textvariable=self.searchtxt_var, font=("goudy old style", 13), bd=1)
        self.search_txt.place(x=85, y=8)
        self.search_txt.bind("<Return>", self.search)

        self.btn_search = Button(frame2, text="Search", command=self.search, font=("goudy old style", 15, "bold"),
                                 bg="#0688FC", fg="white", cursor="hand2")
        self.btn_search.place(x=278, y=6, width=110, height=28)
        self.btn_search.bind("<Return>", self.search)

        # =========Class Table and Scroll Bar=====================
        # X scrollbar
        class_scroll_x = Scrollbar(frame2, orient=HORIZONTAL)
        class_scroll_x.pack(side=BOTTOM, fill=X, padx=1, pady=1)

        # Y scrollbar
        class_scroll_y = Scrollbar(frame2, orient=VERTICAL)
        class_scroll_y.pack(side=RIGHT, fill=Y, pady=1, padx=1)

        # table
        self.class_table = ttk.Treeview(frame2,columns=("id", "class"),
                                        xscrollcommand=class_scroll_x.set,
                                        yscrollcommand=class_scroll_y.set)
        # configure Y scrollbar
        class_scroll_y.config(command=self.class_table.yview)
        class_scroll_x.config(command=self.class_table.xview)

        # table heading
        self.class_table.heading("id", text="ID")
        self.class_table.heading("class", text="Class")
        # show table heading
        self.class_table["show"] = "headings"
        # table column width
        self.class_table.column("id", width=50, anchor=CENTER)
        self.class_table.column("class", width=115, anchor=CENTER)
        self.class_table.pack(fill=BOTH, expand=1, padx=1, pady=1)
        self.class_table.bind("<ButtonRelease-1>", self.getdata)

        self.show()

    def show(self):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            cur.execute(
                "Select id,classname from class ORDER BY id and classname")
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

    def search(self, event):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            cur.execute("Select id,classname from class where class LIKE '%" +
                        str(self.search_txt.get())+"%'  ORDER BY classname")
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

    def getdata(self, event):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            f = self.class_table.focus()
            content = (self.class_table.item(f))
            class_row = content["values"]
            # print(class_row[0])
            if class_row != "":
                cur.execute("Select std_id,name,date,std_attendance.status,class_id  from std_attendance \
                            INNER JOIN student ON std_attendance.std_id = student.id where class_id=? ORDER BY date",
                            (class_row[0],))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.stdAttend_table.delete(
                        *self.stdAttend_table.get_children())
                    for row in rows:
                        self.stdAttend_table.insert("", END, values=row)
                        con.commit()
                else:
                    self.stdAttend_table.delete(
                        *self.stdAttend_table.get_children())
                    messagebox.showinfo(
                        "Info", "No Record Found", parent=self.root)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = manage_attend_Class(root)
    root.mainloop()
