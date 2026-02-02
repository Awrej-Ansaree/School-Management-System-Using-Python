import create_db
import sqlite3
import os
# import ftRegisteration

def main():
    create_db.create_db()
    con = sqlite3.connect("Database/sms.db")
    cur = con.cursor()

    cur.execute("Select * from school")
    row = cur.fetchone()

    if row == None:
        #os.startfile("ftRegisteration.py")
        os.system("python ftRegisteration.py")

    else:
        #os.startfile("login_form.py")
        os.system("python login_form.py")

if __name__=="__main__":
    main()
