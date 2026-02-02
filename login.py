from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from forget_pass import forgetPass_Class
#import sqlite3

class login_Class:
    def __init__(self, root):
        self.root = root
        x = (root.winfo_screenwidth() - 350) / 2
        y = (root.winfo_screenheight() - 500) / 2
        self.root.geometry(f"350x500+{int(x)}+{int(y)}")
        self.root.resizable(0, 0)
        self.root.title("Login")

        self.show_pass = IntVar()

        # =======Designing UI========
        self.gradient_bg(self.root,244444)

        Frame(self.root,width=250,height=400).place(x=50,y=50)

        self.img = Image.open("images/log2.png")
        self.img = ImageTk.PhotoImage(self.img)

        img_lbl = Label(image=self.img,border=0,justify=CENTER)
        img_lbl.place(x=110, y=60)

        user_lbl = Label(self.root,text="Username", font=("goudy old style",15,"bold")).place(x=80,y=200)
        self.user_entry = Entry(self.root,width=20,border=0, font=("goudy old style",13),bg="#f0f0f0")
        self.user_entry.place(x=80,y=230)
        Frame(self.root,width=180,height=2,bg='#141414').place(x=80,y=252)

        pass_lbl = Label(self.root,text="Password", font=("goudy old style",15,"bold")).place(x=80,y=280)
        self.pass_entry = Entry(self.root,width=20,border=0, font=("goudy old style",13) ,show="•" ,bg="#f0f0f0")
        self.pass_entry.place(x=80,y=310)
        Frame(self.root,width=180,height=2,bg='#141414').place(x=80,y=332)
        
        check_pass = Checkbutton(self.root,text="Show Password", font=("goudy old style",12), variable=self.show_pass,command=self.check_showpass)
        check_pass.place(x=100,y=340)

        self.login_btn = Button(root,text="LOGIN",width=20,height=2,fg="white",border=0,bg="#4287f5",activeforeground="#4287f5",activebackground="white",font=("goudy old style",10,"bold"),command=self.login,cursor="hand2")      
        self.login_btn.bind("<Enter>", self.on_enter)
        self.login_btn.bind("<Leave>", self.on_leave)
        self.login_btn.place(x=100,y=375)

        forget_lbl = Label(self.root,text="Forget Password", font=("goudy old style",12,"underline"), fg="#4287f5",cursor="hand2")
        forget_lbl.bind("<Enter>",lambda x:forget_lbl.config(font=("goudy old style",12)))
        forget_lbl.bind("<Leave>",lambda x:forget_lbl.config(font=("goudy old style",12,"underline")))
        forget_lbl.bind("<Button-1>",self.forget_pass)
        forget_lbl.place(x=115,y=420)
        
    # Gradient Background
    def gradient_bg(self,root,start_color):
        j=0
        r=0
        for i in range(100):
            c = str(start_color+r)
            Frame(root,width=10,height=500,bg="#"+c).place(x=j,y=0)
            j+=10
            r+=1

    # Hover Effect on Button
    def on_enter(self,event):
        self.login_btn.config(fg="#4287f5",bg="white")

    def on_leave(self,event):
        self.login_btn.config(fg="white",bg="#4287f5")

    # Check to Show Password or not
    def check_showpass(self):
        if self.show_pass.get():
            self.pass_entry.config(show="")
            self.root.update()
        else:
            self.pass_entry.config(show="•")
            self.root.update()

    # Login if password and username is matched
    def login(self):
        print(self.user_entry.get())
        print(self.pass_entry.get())
        if self.user_entry.get()=='admin' and self.pass_entry.get()=='admin':
            messagebox.showinfo("LOGIN SUCCESSFULLY", "Welcome",parent=self.root)
        else:
            messagebox.showwarning("LOGIN FAILED","PLEASE TRY AGAIN",parent=self.root)

    def forget_pass(self,event):
        self.new_win = Toplevel(self.root)
        self.new_obj = forgetPass_Class(self.new_win)

if __name__ == "__main__":
    root = Tk()
    obj = login_Class(root)
    root.mainloop()
