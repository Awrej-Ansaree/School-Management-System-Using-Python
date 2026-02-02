from tkinter import *
from tkinter import messagebox
from tokenize import String
from PIL import Image, ImageTk
import numpy as np
import face_recognition
import cv2
import os
import json
import sqlite3
import time, nepali_datetime
from datetime import timedelta
# import pyttsx3

class auto_attend_Class:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1050x520+300+130")
        self.root.resizable(0, 0)
        self.root.title("Auto Attendance")
        self.root.focus_force()
        # self.root.grab_set()
        # self.engine = pyttsx3.init()

        # ========All Variables==========
        self.cam_on = False
        self.cap = None
        self.count = 0
        self.face_img_list = os.listdir("images/face recognition")
        self.total_len = len(self.face_img_list)
        self.date_var = StringVar()
        self.Timer_var = IntVar()
        self.date_var.set(str(nepali_datetime.date.today()))

        # ==========Loading Face Encodings and Details===========
        with open("Database/face_encodings.json") as f:
            face_encodings = json.load(f)

        self.IDs = face_encodings["IDs"]
        self.Names = face_encodings["Names"]
        self.stdClass = face_encodings["Class"]
        # self.Section = face_encodings["Section"]
        # self.Medium = face_encodings["Medium"]
        self.encodelistknown = face_encodings["Encodings"]

        # =======Loading Background Image==============
        self.bg_img = Image.open("images/bg/auto_attend_bg.jpg")
        self.bg_img = self.bg_img.resize((1050, 520), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        # ===================================Designing UI============================================
        bg_lbl = Label(self.root, image=self.bg_img).place(
            x=0, y=0, relwidth=1)

        title = Label(self.root, text="Auto Attendance System", font=(
            "goudy old style", 25, "bold"), bg="white").pack(side=TOP, fill=X, padx=5, pady=8)

        # ==============Designing Frame1=================
        frame1 = Frame(self.root, bd=0, bg="#42587d")
        frame1.place(x=15, y=70, width=600, height=434)

        frame1_title = Label(frame1, text="Facial Recognition", bg="#001E41", fg="white", font=(
            "goudy old style", 20, "bold")).pack(fill=X)

        self.img_lbl = Label(frame1, bd=1, relief=SOLID,
                             font=("goudy old style", 20, "bold"))
        self.img_lbl.place(x=0, y=38, relwidth=1, height=396)

        # ============Designing Frame2====================
        frame2 = Frame(self.root, bd=0, bg="#42587d")
        frame2.place(x=635, y=70, width=400, height=434)

        frame2_title = Label(frame2, text="Details", bg="#001E41", fg="white", font=(
            "goudy old style", 20, "bold")).pack(fill=X)

        stdDetails_frame = LabelFrame(frame2,text="Student Details",bg="#42587d",padx=5)
        stdDetails_frame.pack(padx=20, pady=20, fill=X)

        self.id_lbl = Label(stdDetails_frame, text="ID:", font=(
            "goudy old style", 15,"bold"), compound=RIGHT,bg="#42587d")
        self.id_lbl.grid(row=0, column=0, sticky=W)

        self.name_lbl = Label(stdDetails_frame, text="Name:", font=(
            "goudy old style", 15,"bold"), compound=RIGHT,bg="#42587d")
        self.name_lbl.grid(row=1, column=0, sticky=W)

        self.class_lbl = Label(stdDetails_frame, text="Class:", font=(
            "goudy old style", 15,"bold"), compound=RIGHT,bg="#42587d")
        self.class_lbl.grid(row=2, column=0, sticky=W)

        # self.sec_lbl = Label(stdDetails_frame, text="Section:", font=(
        #     "goudy old style", 15,"bold"), compound=RIGHT,bg="#42587d")
        # self.sec_lbl.grid(row=3, column=0, sticky=W)

        # self.medium_lbl = Label(stdDetails_frame, text="Medium:", font=(
        #     "goudy old style", 15,"bold"), compound=RIGHT,bg="#42587d")
        # self.medium_lbl.grid(row=4, column=0, sticky=W)

        attendDetails_frame = LabelFrame(frame2,text="Attendance Details",bg="#42587d")
        attendDetails_frame.pack(padx=20, pady=10, fill=X)

        attendDate_lbl = Label(attendDetails_frame,text="Date",font=("goudy old style", 17,"bold"),bg="#42587d").grid(row=0,column=0,sticky=W,padx=5)
        self.attendDate_txt = Entry(attendDetails_frame,textvariable=self.date_var,font=("goudy old style", 15),width=10)
        self.attendDate_txt.grid(row=0,column=1,sticky=W)

        attendTimer_lbl = Label(attendDetails_frame,text="Timer",font=("goudy old style", 17,"bold"),bg="#42587d").grid(row=1,column=0,sticky=W,padx=5)
        self.attendTimer_txt = Entry(attendDetails_frame,textvariable=self.Timer_var,font=("goudy old style", 15),width=10)
        self.attendTimer_txt.grid(row=1,column=1,sticky=W)

        noteDateTime_lbl = Label(attendDetails_frame,text="Note: Date Format\nYYYY-MM-DD (2078-01-01)\n Timer should be in Minutes",font=("goudy old style", 10),bg="lightyellow").grid(row=0,column=2,rowspan=2,padx=7)

        self.startAttend_btn = Button(frame2, text="Take Attendance", command=self.start_attendance, font=(
            "goudy old style", 15, "bold"), bg="#0ba13b", fg="white", cursor="hand2")
        self.startAttend_btn.place(x=40,y=370)

        self.stopAttend_btn = Button(frame2, text="Stop Attendance", command=self.stop_attendance, state=DISABLED, font=(
            "goudy old style", 15, "bold"), bg="#c72210", fg="white", cursor="hand2")
        self.stopAttend_btn.place(x=210,y=370)

        self.slide_img()

    # ===========All Functions/Methods=============

    def start_attendance(self):
        try:
            if self.match_dateformat(self.date_var.get()):
                if self.date_var.get()=="" or self.Timer_var.get()<=0:
                    messagebox.showerror("Error","Date and Timer both fields are required")
                    
                else:
                    currTime = nepali_datetime.datetime.strptime(time.strftime("%I:%M %p"),"%I:%M %p")
                    self.timerTime = currTime+timedelta(minutes=self.Timer_var.get())
                    self.timerTime = str(self.timerTime).split(" ")[1].split("+")[0]

                    self.img_lbl.after_cancel(self.slide)
                    self.attendDate_txt.config(state=DISABLED)
                    self.attendTimer_txt.config(state=DISABLED)
                    self.startAttend_btn.config(state=DISABLED)
                    self.stopAttend_btn.config(state=NORMAL)
                    self.cam_on = True
                    self.cap = cv2.VideoCapture(0)
                    self.show_frame()
            else:
                messagebox.showerror("Error","Provide the Date in Correct Format")

        except Exception as e:
            messagebox.showerror("Error",f"Error due to: {e}",parent=self.root)

    def mark_attendance(self, sid
                        # , name, stdclass, sec, medium
                        ):
        con = sqlite3.connect("Database/sms.db")
        cur = con.cursor()
        try:
            currDate = self.date_var.get()
            currTime = time.strftime("%I:%M:%S %p")
            cur.execute("Select * from std_attendance where std_id=? and date=?",(sid,currDate))
            row = cur.fetchone()

            if row==None:
                cur.execute("Insert into std_attendance (std_id,date,status) values(?,?,?)",(
                    sid,
                    currDate,
                    "Present",
                ))
                con.commit()
                # self.speak("Your Attendance is Marked")

            con.close()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to: {e}",parent=self.root)

    def stop_attendance(self):
        self.cam_on = False
        if self.cap:
            self.cap.release()
        self.img_lbl.after_cancel(self.start_attend)
        self.attendDate_txt.config(state=NORMAL)
        self.attendTimer_txt.config(state=NORMAL)
        self.startAttend_btn.config(state=NORMAL)
        self.stopAttend_btn.config(state=DISABLED)
        self.slide_img()

    def show_frame(self):
        try:
            currTime = time.strftime("%I:%M:00")
            if self.timerTime!=currTime:
                if self.cam_on:

                    ret, img = self.cap.read()

                    if ret:
                        self.id_lbl.config(text="ID:")
                        self.name_lbl.config(text="Name:")
                        self.class_lbl.config(text="Class:")
                        # self.sec_lbl.config(text="Section:")
                        # self.medium_lbl.config(text="Medium:")

                        img = cv2.flip(img, 1)
                        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                        facesCurFrame = face_recognition.face_locations(imgS)
                        encodeCurFrame = face_recognition.face_encodings(
                            imgS, facesCurFrame)

                        for encodeface, faceloc in zip(encodeCurFrame, facesCurFrame):
                            matches = face_recognition.compare_faces(
                                self.encodelistknown, encodeface)
                            facedis = face_recognition.face_distance(
                                self.encodelistknown, encodeface)
                            matchIndex = np.argmin(facedis)

                            if matches[matchIndex]:
                                sid = self.IDs[matchIndex]
                                name = self.Names[matchIndex]
                                sclass = self.stdClass[matchIndex]
                                # sec = self.Section[matchIndex]
                                # medium = self.Medium[matchIndex]

                                self.id_lbl.config(
                                    text=f"ID: {sid}")
                                self.name_lbl.config(text=f"Name: {name}")
                                self.class_lbl.config(
                                    text=f"Class: {sclass}")
                                # self.sec_lbl.config(
                                #     text=f"Section: {sec}")
                                # self.medium_lbl.config(
                                #     text=f"Medium: {medium}")

                                y1, x2, y2, x1 = faceloc
                                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                                cv2.rectangle(
                                    img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(
                                    img, f"{name}", (x1-20, y2+30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)
                                self.mark_attendance(sid)

                        # Showing Image in tkinter window
                        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(cv2image).resize((600, 396))
                        imgtk = ImageTk.PhotoImage(image=img)
                        self.img_lbl.imgtk = imgtk
                        self.img_lbl.configure(image=imgtk)

                    self.start_attend = self.img_lbl.after(10, self.show_frame)
            else:
                self.stop_attendance()
                messagebox.showinfo("Info","Attendance Timeout", parent=self.root)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error due to: {e}", parent=self.root)

    def slide_img(self):

        if self.count == self.total_len:
            self.count = 0

        if self.count < self.total_len:
            self.img = Image.open(
                "images/face recognition/"+self.face_img_list[self.count])
            self.img = self.img.resize((600, 396), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
            self.img_lbl.config(image=self.img)
            self.count += 1

        self.slide = self.img_lbl.after(1500, self.slide_img)

    def match_dateformat(self,date_string):
        try:
            date_format = "%Y-%m-%d" 
            nepali_datetime.datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False

    # def speak(self,text):
    #     self.engine.say(text)
    #     self.engine.runAndWait()

if __name__ == "__main__":
    root = Tk()
    obj = auto_attend_Class(root)
    root.mainloop()
