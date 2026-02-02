from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
import time
import os
import entryplaceholder as eph


class Login_Class:
    def __init__(self, root):
        self.root = root
        x = (root.winfo_screenwidth() - 925) / 2
        y = (root.winfo_screenheight() - 500) / 2
        self.root.geometry(f"925x500+{int(x)}+{int(y)}")
        self.root.config(bg="#ffffff")
        self.root.resizable(False, False)
        self.root.title(
            "Login - Student Management System | Developed by Awrej Ansaree")

        # --------------------------All Variables------------------------------------------------------------
        self.username_var = StringVar()
        self.password_var = StringVar()

        # --------------------------UI Designing-------------------------------------------------------------
        self.bg_img = Image.open("images/login_img2.jpg")
        self.bg_img = self.bg_img.resize((450, 350), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        Label(self.root, image=self.bg_img, bg="white").place(x=50, y=50)

        # ----------------------------------------------------------------------------------------------------
        login_frame = Frame(self.root, width=350, height=350, bg="white")
        login_frame.place(x=480, y=70)

        # ----------------------------------------------------------------------------------------------------
        signin_heading = Label(login_frame, text="Sign in", fg="#57a1f8", bg="white", font=(
            "Microsoft YaHei UI Light", 23, "bold"))
        signin_heading.place(x=100, y=5)

        # ----------------------------------------------------------------------------------------------------
        user = Entry(login_frame, textvariable=self.username_var, width=35,
                     bg="white", bd=0, font=("Microsoft YaHei UI Light", 11), fg="#777777")
        user.place(x=30, y=80)
        user.insert(0, "Username")
        eph.changeOnFocus(user, "Username")
        Frame(login_frame, width=295, height=2, bg="black").place(x=25, y=107)

        # ----------------------------------------------------------------------------------------------------
        password = Entry(login_frame, textvariable=self.password_var, width=35,
                         bg="white", bd=0, font=("Microsoft YaHei UI Light", 11), fg="#777777")
        password.place(x=30, y=150)
        password.insert(0, "Password")
        eph.changeOnFocus(password, "Password", "•")
        Frame(login_frame, width=295, height=2, bg="black").place(x=25, y=177)

        # ----------------------------------------------------------------------------------------------------
        # check_pass = Checkbutton(login_frame, text="Show Password", font=("goudy old style",12), bg="white", bd=0, relief=FLAT, activebackground="white", cursor="hand2")
        # check_pass.place(x=35,y=200)

        # ----------------------------------------------------------------------------------------------------
        # select_session = ttk.Combobox(login_frame, values=("Session"), font=("Microsoft YaHei UI Light", 11,"bold"), justify=CENTER, state="readonly")
        # select_session.place(x=70, y=210)
        # select_session.current(0)

        # ----------------------------------------------------------------------------------------------------
        login_btn = Button(login_frame, text="Sign in", command=self.login,
                           width=39, pady=7, bg="#57a1f8", fg="white", bd=0, cursor="hand2")
        login_btn.place(x=35, y=205)

        # ----------------------------------------------------------------------------------------------------
        Label(login_frame, text="Don't Remember Password?", bg="white",
              font=("Microsoft YaHei UI Light", 9)).place(x=45, y=255)
        forget_pass = Button(login_frame, text="Forget Password", command=self.forget_pass,
                             bg="white", bd=0, cursor="hand2", fg="#57a1f8", activebackground="white")
        forget_pass.place(x=208, y=255)

    # ------------------------------All Funtions/Methods------------------------------------------------------
    def login(self):
        try:
            # Conncecting to the database
            con = sqlite3.connect("Database/sms.db")
            cur = con.cursor()

            if self.username_var.get() == "Username" or self.password_var.get() == "Password":
                messagebox.showerror(
                    "Error", "All fields are required\nPlease try again", parent=self.root)

            else:
                cur.execute("Select * from user where username=? and password=? and school_id=?",
                            (self.username_var.get(), self.password_var.get(), 1,))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Login Failed", "Wrong Username/Password\nPlease try again", parent=self.root)

                else:
                    messagebox.showinfo(
                        "Success", "You have successfully logged in", parent=self.root)
                    self.root.destroy()
                    os.system("python dashboard.py")

            con.close()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def forget_pass(self):
        try:

            os.system("python forget_pass.py")

        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Login_Class(root)
    root.mainloop()
