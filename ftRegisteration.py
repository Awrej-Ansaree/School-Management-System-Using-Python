from tkinter import *
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os


class ftRegisteration_Class:
    def __init__(self, root):
        self.root = root
        x = (root.winfo_screenwidth() - 850) / 2
        y = (root.winfo_screenheight() - 500) / 2
        self.root.geometry(f"850x500+{int(x)}+{int(y)}")
        self.root.resizable(False, False)
        self.root.title(
            "Student Management System | Developed by Awrej Ansaree")
        self.root.config(bg="#ffffff")

        # --------------------------All Variables------------------------------------------------------------
        question_list = ["Select Question", "What's your first pet name?", "What's your favourite movie name?",
                         "Your first school?", "Name of your best friend?", "Place where you born?", "Sports you like most?"]
        self.Path_var = StringVar()
        self.logo_fob = ""
        self.Name_var = StringVar()
        self.Address_var = StringVar()
        self.Contact_var = StringVar()
        self.Email_var = StringVar()
        self.Question_var = StringVar()
        self.Answer_var = StringVar()
        self.User_var = StringVar()
        self.Password_var = StringVar()

        # --------------------------UI Designing-------------------------------------------------------------
        title = Label(self.root, text="First Time Regesteration", font=(
            "goudy old style", 25, "bold"), bg="#001E41", fg="white").pack(side=TOP, fill=X)

        # --------------------------Details Frame-------------------------------------------------------------
        Details_frame = Frame(self.root, bd=0, bg="white", padx=20)
        Details_frame.place(x=40, y=55)

        # ----------------------------------------------------------------------------------------------------
        logo_lbl = Label(Details_frame, text="School Logo",
                         font=("goudy old style", 18), bg="white")
        logo_lbl.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        browse_frame = Frame(Details_frame, bg="white")
        browse_frame.grid(row=0, column=1, sticky="w", padx=10)

        logoPath_txt = Entry(browse_frame, textvariable=self.Path_var, font=(
            "goudy old style", 15), width=37, bd=1, relief=SOLID)
        logoPath_txt.grid(row=0, column=0, sticky="w")

        browse_btn = Button(browse_frame, text="Browse Logo", width=15, bg="#222222", fg="white",
                            bd=0, cursor="hand2", font=("goudy old style", 11), command=self.browseLogo)
        browse_btn.grid(row=0, column=1, sticky="w", padx=2)

        # ----------------------------------------------------------------------------------------------------
        schoolName_lbl = Label(Details_frame, text="School Name",
                               font=("goudy old style", 18), bg="white")
        schoolName_lbl.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        schoolName_txt = Entry(Details_frame, textvariable=self.Name_var, relief=SOLID, font=(
            "goudy old style", 15), width=50)
        schoolName_txt.grid(row=1, column=1, sticky="w", padx=10)

        # ----------------------------------------------------------------------------------------------------
        schoolAddress_lbl = Label(Details_frame, text="Address",
                                  font=("goudy old style", 18), bg="white")
        schoolAddress_lbl.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        schoolAddress_txt = Entry(Details_frame, textvariable=self.Address_var, relief=SOLID, font=(
            "goudy old style", 15), width=50)
        schoolAddress_txt.grid(row=2, column=1, sticky="w", padx=10)

        # ----------------------------------------------------------------------------------------------------
        schoolContact_lbl = Label(Details_frame, text="Contact No.",
                                  font=("goudy old style", 18), bg="white")
        schoolContact_lbl.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        schoolContact_txt = Entry(Details_frame, textvariable=self.Contact_var, relief=SOLID, font=(
            "goudy old style", 15), width=50)
        schoolContact_txt.grid(row=3, column=1, sticky="w", padx=10)

        # ----------------------------------------------------------------------------------------------------
        schoolEmail_lbl = Label(Details_frame, text="E-mail ID",
                                font=("goudy old style", 18), bg="white")
        schoolEmail_lbl.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        schoolEmail_txt = Entry(Details_frame, textvariable=self.Email_var, relief=SOLID, font=(
            "goudy old style", 15), width=50)
        schoolEmail_txt.grid(row=4, column=1, sticky="w", padx=10)

        # ----------------------------------------------------------------------------------------------------
        question_lbl = Label(Details_frame, text="Security Question",
                             font=("goudy old style", 18), bg="white")
        question_lbl.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        select_question = ttk.Combobox(Details_frame, values=question_list, textvariable=self.Question_var, font=(
            "goudy old style", 15), justify=CENTER, state="readonly", width=48)
        select_question.grid(row=5, column=1, sticky="w", padx=10)
        select_question.current(0)

        # ----------------------------------------------------------------------------------------------------
        answer_lbl = Label(Details_frame, text="Answer",
                           font=("goudy old style", 18), bg="white")
        answer_lbl.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        answer_txt = Entry(Details_frame, textvariable=self.Answer_var,
                           relief=SOLID, font=("goudy old style", 15), width=50)
        answer_txt.grid(row=6, column=1, sticky="w", padx=10)

        # ----------------------------------------------------------------------------------------------------
        user_lbl = Label(Details_frame, text="Username",
                         font=("goudy old style", 18), bg="white")
        user_lbl.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        user_txt = Entry(Details_frame, textvariable=self.User_var,
                         relief=SOLID, font=("goudy old style", 15), width=50)
        user_txt.grid(row=7, column=1, sticky="w", padx=10)

        # ----------------------------------------------------------------------------------------------------
        password_lbl = Label(Details_frame, text="Password",
                             font=("goudy old style", 18), bg="white")
        password_lbl.grid(row=8, column=0, padx=10, pady=5, sticky="w")

        password_txt = Entry(Details_frame, textvariable=self.Password_var,
                             show="•", relief=SOLID, font=("goudy old style", 15), width=50)
        password_txt.grid(row=8, column=1, sticky="w", padx=10)

        # ----------------------------------------------------------------------------------------------------
        register_btn = Button(self.root, text="Register", width=20, pady=7,
                              bg="#57a7f8", fg="white", bd=0, cursor="hand2", command=self.register)
        register_btn.place(x=265, y=450)

        reset_btn = Button(self.root, text="Reset", width=20, pady=7,
                           bg="#777777", fg="white", bd=0, cursor="hand2", command=self.reset)
        reset_btn.place(x=420, y=450)

    # ------------------------------All Funtions/Methods------------------------------------------------------
    def browseLogo(self):
        try:
            f_types = [("Images", ("*.png", "*.jpg")), ("PNG Files",
                                                        "*.png"), ("JPG Files", "*.jpg"), ("All Files", "*.*")]
            img_path = filedialog.askopenfilename(
                initialdir="/", title="Select Student Image", filetypes=f_types, parent=self.root)

            if img_path != "":
                self.Path_var.set(img_path)
                self.logo_fob = open(img_path, "rb")
                self.logo_fob = self.logo_fob.read()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def register(self):
        try:
            # Conncecting to the database
            con = sqlite3.connect("Database/sms.db")
            cur = con.cursor()

            if not (self.Path_var.get() == "" and self.Name_var.get() == "" and self.Address_var.get() == "" and self.Contact_var.get() == "" and self.Email_var.get() == "" and
                    self.Question_var.get() == "Select Question" and self.Answer_var.get() == "" and self.User_var.get() == "" and self.Password_var.get() == ""):

                # checking whether the school is already registered or not
                # cur.execute("Select * from school where name=? and address=? and contact_no=? and email=?",(self.Name_var.get(),self.Address_var.get(),self.Contact_var.get(),self.Email_var.get(),))
                cur.execute("Select * from school")
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Registration Failed", "This is for first time registration.\n You can't register for the second time", parent=self.root)

                else:
                    # Inserting the School details
                    cur.execute("Insert into school (logo_img,name,address,contact_no,email) values(?,?,?,?,?)", (
                        self.logo_fob,
                        self.Name_var.get(),
                        self.Address_var.get(),
                        self.Contact_var.get(),
                        self.Email_var.get(),
                    ))
                    con.commit()

                    # Getting the "school id"
                    cur.execute("Select id from school")
                    schoolID = cur.fetchall()[-1][0]

                    # Inserting the Admin user details
                    cur.execute("Insert into user (username,password,question,answer,school_id) values(?,?,?,?,?)", (
                        self.User_var.get(),
                        self.Password_var.get(),
                        self.Question_var.get(),
                        self.Answer_var.get(),
                        schoolID,
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Registered Successfully", parent=self.root)
                    self.root.destroy()
                    os.startfile("login_form.py")
                    # os.system("python login_form.py")
            else:
                messagebox.showerror(
                    "Error", "All the fields are required\nPlease try again", parent=self.root)

            con.close()

        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def reset(self):
        try:
            if not (self.Path_var.get() == "" and self.Name_var.get() == "" and self.Address_var.get() == "" and self.Contact_var.get() == "" and self.Email_var.get() == "" and
                    self.Question_var.get() == "Select Question" and self.Answer_var.get() == "" and self.User_var.get() == "" and self.Password_var.get() == ""):
                op = messagebox.askyesno(
                    "Confirm", "Do you really want to reset?", parent=self.root)
                if op:
                    self.clear()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to : {str(e)}", parent=self.root)

    def clear(self):
        self.Path_var.set("")
        self.Name_var.set("")
        self.Address_var.set("")
        self.Contact_var.set("")
        self.Email_var.set("")
        self.Question_var.set("Select Question")
        self.Answer_var.set("")
        self.User_var.set("")
        self.Password_var.set("")


if __name__ == "__main__":
    root = Tk()
    obj = ftRegisteration_Class(root)
    root.mainloop()
