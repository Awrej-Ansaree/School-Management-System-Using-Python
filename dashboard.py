from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import nepali_datetime
import sqlite3
import time
import os
from manage_students import manage_students_Class
from manage_ClassFee import manage_class_Class
from auto_attend import auto_attend_Class
from manual_attend import manual_attend_Class
from manage_attend import manage_attend_Class
from manage_IDCard import idCard_Class
import create_db

# ==========function to change properties of button on hover=============


def changeOnHover(button, colorOnHover="#1f55a8", colorOnLeave="#0b3563"):
    button.bind("<Enter>", lambda e: button.config(
        background=colorOnHover))

    button.bind("<Leave>", lambda e: button.config(
        background=colorOnLeave))


class Students_MS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title(
            "Students Management System | Developed by Awrej Ansaree")
        try:
            root.attributes("-zoomed", True)
        except:
            root.state("zoomed")

        # -----Variables-----
        self.slider_text = ""
        self.count = 0
        self.rec_count = 0
        self.text = ""
        self.wel_texts = [
            "Welcome to Students Management System", "Developed By Awrej Ansaree"]

        # -----loading images-----
        self.auto_img = Image.open("images/facial_recognition.jpg")
        self.auto_img = self.auto_img.resize((160, 140), Image.ANTIALIAS)
        self.auto_img = ImageTk.PhotoImage(self.auto_img)

        self.manual_img = Image.open("images/manual_attendance.png")
        self.manual_img = self.manual_img.resize((160, 140), Image.ANTIALIAS)
        self.manual_img = ImageTk.PhotoImage(self.manual_img)

        self.manage_img = Image.open("images/view,manage_attendance.jpg")
        self.manage_img = self.manage_img.resize((160, 140), Image.ANTIALIAS)
        self.manage_img = ImageTk.PhotoImage(self.manage_img)

        # ------title----
        self.icon_title = PhotoImage(file="images/title_img.png")
        title = Label(self.root, text="Students Management System", image=self.icon_title, compound=LEFT, font=(
            "times new roman", 40, "bold"), bg="#ffffff", fg="#1f55a8", anchor="w", padx=20).place(x=302, y=2, relwidth=1, height=70)

        # ------logout btn------
        self.logout_img = PhotoImage(file="images/logout.png")
        logout_btn = Button(self.root, image=self.logout_img, bd=0, bg="#ffffff", activebackground="#ffffff",
                            cursor="hand2", command=self.logout).place(x=1200, y=10, height=50, width=140)

        # ----Welcome------
        self.lbl_wel = Label(self.root, text="Welcome to Students Management System", font=(
            "times new roman", 15), bg="#4d636d", fg="white", anchor="w", padx=90)
        self.lbl_wel.place(x=300, y=70, width=450, height=30)

        # -----clock-----
        self.lbl_clock = Label(self.root, text="Date: DD-MM-YY\t\t Time: HH:MM:SS AM/PM",
                               font=("times new roman", 15), bg="#4d636d", fg="white", anchor="w", padx=90)
        self.lbl_clock.place(x=750, y=70, relwidth=1, height=30)

        # ---left menu---
        self.left_menu = Frame(self.root, bd=0, bg="#0b3563")
        self.left_menu.place(x=0, y=0, width=300, relheight=1)

        self.menu_title_img = PhotoImage(file="images/menu_img.png")
        menu_title = Label(self.left_menu, text="Menu", bg="#1e5bba", fg="#ffffff", image=self.menu_title_img, compound=LEFT, font=(
            "times new roman", 25, "bold"), anchor="center", padx=20, pady=10).pack(side=TOP, fill=X, pady=10, padx=8)

        # -------------------------Menu btn------------------------
        # -------manage btn-----
        self.manage_std_img = PhotoImage(file="images/manage_std_img.png")
        self.manage_std_btn = Button(self.left_menu, text="Manage Students", image=self.manage_std_img, compound=LEFT, command=self.manage_std, font=(
            "times new roman", 15, "bold"), padx=20, bd=0, bg="#0b3563", fg="#ffffff", activebackground="#0b3563", activeforeground="#ffffff", cursor="hand2", anchor="w", pady=5)
        self.manage_std_btn.pack(side=TOP, fill=X, pady=10)
        changeOnHover(self.manage_std_btn)

        self.manage_class_img = PhotoImage(file="images/manage_class_img.png")
        self.manage_class_btn = Button(self.left_menu, text="Class & Fee", image=self.manage_class_img, compound=LEFT, command=self.manage_class, font=(
            "times new roman", 15, "bold"), padx=20, bd=0, bg="#0b3563", fg="#ffffff", activebackground="#0b3563", activeforeground="#ffffff", cursor="hand2", anchor="w", pady=5)
        self.manage_class_btn.pack(side=TOP, fill=X, pady=10)
        changeOnHover(self.manage_class_btn)

        # -------Attendance btn-----
        self.attendance_img = PhotoImage(file="images/attendance_img.png")
        self.attendence_btn = Button(self.left_menu, text="Attendance", image=self.attendance_img, compound=LEFT, command=self.attendance, font=(
            "times new roman", 15, "bold"), padx=20, bd=0, bg="#0b3563", fg="#ffffff", activebackground="#0b3563", activeforeground="#ffffff", cursor="hand2", anchor="w", pady=5)
        self.attendence_btn.pack(side=TOP, fill=X, pady=10)
        changeOnHover(self.attendence_btn)

        # -------Id Card btn-----
        self.id_card_img = PhotoImage(file="images/id_card_img.png")
        self.id_car_btn = Button(self.left_menu, text="ID Card", image=self.id_card_img, compound=LEFT, command=self.id_card, font=("times new roman", 15, "bold"),
                                 padx=20, bd=0, bg="#0b3563", fg="#ffffff", activebackground="#0b3563", activeforeground="#ffffff", cursor="hand2", anchor="w", pady=5)
        self.id_car_btn.pack(side=TOP, fill=X, pady=10)
        changeOnHover(self.id_car_btn)

        # -------Fee btn-----
        self.fee_img = PhotoImage(file="images/fee_img.png")
        self.fee_btn = Button(self.left_menu, text="Fee", image=self.fee_img, compound=LEFT, font=("times new roman", 15, "bold"), padx=20,
                              bd=0, bg="#0b3563", fg="#ffffff", activebackground="#0b3563", activeforeground="#ffffff", cursor="hand2", anchor="w", pady=5)
        self.fee_btn.pack(side=TOP, fill=X, pady=10)
        changeOnHover(self.fee_btn)

        # -------profile btn-----
        self.profile_img = PhotoImage(file="images/profile_img.png")
        self.profile_btn = Button(self.left_menu, text="Profile", image=self.profile_img, compound=LEFT, font=("times new roman", 15, "bold"),
                                  padx=20, bd=0, bg="#0b3563", fg="#ffffff", activebackground="#0b3563", activeforeground="#ffffff", cursor="hand2", anchor="w", pady=5)
        self.profile_btn.pack(side=TOP, fill=X, pady=10)
        changeOnHover(self.profile_btn)

        # -------exit btn-----
        self.exit_img = PhotoImage(file="images/exit_img1.png")
        self.exit_btn = Button(self.left_menu, text="Exit", image=self.exit_img, compound=LEFT, font=("times new roman", 15, "bold"), padx=20, bd=0, bg="#0b3563",
                               fg="#ffffff", activebackground="#0b3563", activeforeground="#ffffff", cursor="hand2", anchor="w", command=lambda: (self.root.destroy()), pady=5)
        self.exit_btn.pack(side=TOP, fill=X, pady=10)
        changeOnHover(self.exit_btn)

        # -------contents-----
        self.lbl_total_std = Label(self.root, text="Total Students\n\0( 0 )", bg="#ffffff", font=(
            "times new roman", 20), anchor=CENTER, padx=20, pady=20)
        self.lbl_total_std.place(x=350, y=120, height=125, width=250)

        self.lbl_total_present = Label(self.root, text="Total Present\n( 0 )", bg="#ffffff", font=(
            "times new roman", 20), anchor=CENTER, padx=20, pady=20)
        self.lbl_total_present.place(x=700, y=120, height=125, width=250)

        self.lbl_total_absent = Label(self.root, text="Total Absent\n( 0 )", bg="#ffffff", font=(
            "times new roman", 20), anchor=CENTER, padx=20, pady=20)
        self.lbl_total_absent.place(x=1050, y=120, height=125, width=250)

        # -----footer-----
        self.lbl_footer = Label(self.root, text="SMS - Students Management System | Developed by Awrej Ansaree\nFor any Technical Issue Contact: 9865200301",
                                font=("times new roman", 12), bg="#4d636d", fg="white", padx=90).pack(side=BOTTOM, fill=X)

        self.update_content()

# ----------------Functions or Methods----------------------

    def manage_std(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = manage_students_Class(self.new_win)

    def manage_class(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = manage_class_Class(self.new_win)

    def attendance(self):
        self.attend_root = Toplevel()
        self.attend_root.geometry("510x200+550+200")
        self.attend_root.resizable(0, 0)
        self.attend_root.title("Attendance")
        self.attend_root.config(bg="white")
        self.attend_root.focus_force()
        self.attend_root.grab_set()

        auto_btn = Button(self.attend_root, text="Auto\nAttendance", image=self.auto_img, compound=TOP, command=self.auto_attend, font=(
            "goudy old style", 15, "bold"), bg="#004275", fg="white", bd=3, relief=RAISED, cursor="hand2").pack(side=LEFT)
        manual_btn = Button(self.attend_root, text="Manual\nAttendance", image=self.manual_img, compound=TOP, command=self.manual_attend, font=(
            "goudy old style", 15, "bold"), bg="#3c965d", fg="white", bd=3, relief=RAISED, cursor="hand2").pack(side=LEFT)
        manage_btn = Button(self.attend_root, text="View/Manage\nAttendance", image=self.manage_img, compound=TOP, command=self.manage_attend,
                            font=("goudy old style", 15, "bold"), bg="#006cbf", fg="white", bd=3, relief=RAISED, cursor="hand2").pack(side=LEFT)

    def auto_attend(self):
        self.attend_root.destroy()
        self.new_win = Toplevel(self.root)
        self.new_obj = auto_attend_Class(self.new_win)

    def manual_attend(self):
        self.attend_root.destroy()
        self.new_win = Toplevel(self.root)
        self.new_obj = manual_attend_Class(self.new_win)

    def manage_attend(self):
        self.attend_root.destroy()
        self.new_win = Toplevel(self.root)
        self.new_obj = manage_attend_Class(self.new_win)

    def id_card(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = idCard_Class(self.new_win)

    def logout(self):
        try:
            self.root.destroy()
            os.system("python login_form.py")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def update_content(self):
        try:
            con = sqlite3.connect("Database/sms.db")
            cur = con.cursor()

            current_time = time.strftime("%I:%M:%S %p")
            current_date = nepali_datetime.date.today()

            cur.execute("Select count(*) from student")
            totalStd = cur.fetchone()

            cur.execute("Select count(*) from std_attendance where status=? and date=?",("Present",str(current_date)))
            presentStd = cur.fetchone()

            if self.count >= len(self.text):
                self.slider_text = ""
                self.count = 0
                if self.rec_count == 0:
                    self.text = self.wel_texts[0]
                    self.rec_count = 1

                else:
                    self.text = self.wel_texts[1]
                    self.rec_count = 0

            self.slider_text += self.text[self.count]
            self.count = self.count+1

            self.lbl_wel.config(text=f"{self.slider_text}")
            self.lbl_clock.config(
                text=f"Date: {current_date}\t\t Time: {current_time}")
            self.lbl_total_std.config(text=f"Total Students\n\0( {totalStd[0]} )")
            self.lbl_total_present.config(text=f"Present Students\n\0( {presentStd[0]} )")
            self.lbl_total_absent.config(text=f"Absent Students\n\0( {totalStd[0]-presentStd[0]} )")
            self.lbl_clock.after(100, self.update_content)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)


if __name__ == "__main__":
    create_db.create_db()
    root = Tk()
    obj = Students_MS(root)
    root.mainloop()
