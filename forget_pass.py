from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
import sqlite3

class forgetPass_Class:
    def __init__(self, root):
        self.root = root
        x = (root.winfo_screenwidth() - 350) / 2
        y = (root.winfo_screenheight() - 500) / 2
        self.root.geometry(f"350x500+{int(x)}+{int(y)}")
        self.root.resizable(0, 0)
        self.root.title("Change Password")

        # --------------------------All  Variables------------------------------------------------------------
        question_list = ["Select Question","What's your first pet name?","What's your favourite movie name?",
                        "Your first school?","Name of your best friend?","Place where you born?","Sports you like most?"]
        self.check_show = IntVar()
        self.question_var = StringVar()
        self.answer_var = StringVar()
        self.newpass_var = StringVar()

        # --------------------------UI Designing--------------------------------------------------------------
        self.bg_img = Image.open("images/bg/img1.jpg")
        self.bg_img = self.bg_img.resize((350, 500), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        Label(self.root, image=self.bg_img, bg="white").place(x=0, y=0, relwidth=1)

        # ----------------------------------------------------------------------------------------------------
        forget_frame = Frame(self.root,width=250,height=400,bg="white")
        forget_frame.place(x=50,y=50)

        # ----------------------------------------------------------------------------------------------------
        question_lbl = Label(self.root,text="Select Your Question",font=("goudy old style",15,"bold"),bg="white").place(x=80,y=100)
        combo_Section = ttk.Combobox(self.root, values=question_list, textvariable=self.question_var ,font=("goudy old style", 13),state="readonly", justify=CENTER,width=20)
        combo_Section.place(x=72,y=140)
        combo_Section.current(0)

        # ----------------------------------------------------------------------------------------------------
        answer_lbl = Label(self.root,text="Answer", font=("goudy old style",15,"bold"),bg="white").place(x=80,y=180)
        answer_entry = Entry(self.root, font=("goudy old style", 13), textvariable=self.answer_var, width=20, bd=0)
        answer_entry.place(x=80,y=210)
        Frame(self.root,width=180,height=2,bg='#141414').place(x=80,y=232)

        # ----------------------------------------------------------------------------------------------------
        newpass_lbl = Label(self.root,text="New Password", font=("goudy old style",15,"bold"), bg="white").place(x=80,y=260)
        self.newpass_entry = Entry(self.root, font=("goudy old style", 13), textvariable=self.newpass_var, show="•", width=20, bd=0)
        self.newpass_entry.place(x=80,y=290)
        Frame(self.root,width=180,height=2,bg='#141414').place(x=80,y=312)

        # ----------------------------------------------------------------------------------------------------
        self.check = Checkbutton(self.root, text="Show Password", font=("goudy old style",12), bg="white", variable=self.check_show,command=self.show_pass)
        self.check.place(x=100,y=320)

        # ----------------------------------------------------------------------------------------------------
        self.submit_btn = Button(root,text="SUBMIT",width=20,height=2,fg="#f5f5f5",border=0,bg="#4287f5",activeforeground="#4287f5",activebackground="white",font=("goudy old style",10,"bold"),command=self.submit,cursor="hand2")      
        self.submit_btn.bind("<Enter>", self.on_enter)
        self.submit_btn.bind("<Leave>", self.on_leave)
        self.submit_btn.place(x=100,y=375)

    # ------------------------------All Funtions/Methods------------------------------------------------------
    def on_enter(self,event):
        self.submit_btn.config(fg="#4287f5",bg="#f5f5f5")

    def on_leave(self,event):
        self.submit_btn.config(fg="#f5f5f5",bg="#4287f5")

    def show_pass(self):
        if self.check_show.get()==1:
            self.newpass_entry.config(show="")
        else:
            self.newpass_entry.config(show="•")

    def submit(self):
        try:
            # Conncecting to the database
            con = sqlite3.connect("Database/sms.db")
            cur = con.cursor()

            if self.question_var.get()=="Select Question" or self.answer_var.get()=="" or self.newpass_var.get()=="":
                messagebox.showerror("Error", "All fields are required\nPlease try again", parent=self.root)

            else:
                cur.execute("Select * from user where question=? and answer=? and school_id=?",(self.question_var.get(),self.answer_var.get(),1,))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Failed - Change Password", "Wrong Question/Answer\nPlease try again", parent=self.root)

                else:
                    cur.execute("update user set password=? where school_id=?",(self.newpass_var.get(),1))
                    con.commit()
                    messagebox.showinfo("Success", "Your password has been changed successfully", parent=self.root)
                    self.root.destroy()
                    
            con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to : {str(e)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = forgetPass_Class(root)
    root.mainloop()
