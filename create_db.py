import sqlite3
import json
import os


def create_db():
    if not os.path.exists("Database"):
    	os.mkdir("Database")
		
    conn = sqlite3.connect("Database/sms.db")

    # Creating the "school" table
    conn.execute("""CREATE TABLE IF NOT EXISTS "school" (
	"id"	INTEGER,
	"logo_img"	BLOB,
	"name"	varchar(150),
	"address"	varchar(150),
	"contact_no"	varchar(50),
	"email"	varchar(50),
	PRIMARY KEY("id" AUTOINCREMENT))""")
    conn.commit()

    # Creating the "user" table
    conn.execute("""CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER,
	"username"	varchar(50),
	"password"	varchar(50),
	"question"	varchar(150),
	"answer"	varchar(150),
	"school_id"	INTEGER,
	FOREIGN KEY("school_id") REFERENCES "school"("id"),
	PRIMARY KEY("id" AUTOINCREMENT))""")
    conn.commit()

    # Creating the "session" table
    conn.execute("""CREATE TABLE IF NOT EXISTS "session" (
	"id"	INTEGER,
	"year"	varchar(10),
	"school_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("school_id") REFERENCES "school"("id"))""")
    conn.commit()

    # Creating the "class" table
    conn.execute("""CREATE TABLE IF NOT EXISTS "class" (
	"id"	INTEGER,
	"classname"	varchar(50),
	"session_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
	FOREIGN KEY("session_id") REFERENCES "session"("id"))""")
    conn.commit()

    # Creating the "feetype" table
    conn.execute("""CREATE TABLE IF NOT EXISTS "feetype" (
	"id"	INTEGER,
	"feetypename"	varchar(50),
	"session_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
	FOREIGN KEY("session_id") REFERENCES "session"("id"))""")
    conn.commit()

    # Creating the "classfee" table
    conn.execute("""CREATE TABLE IF NOT EXISTS "fee" (
	"id"	INTEGER,
	"class_id"	INTEGER,
	"feetype_id"	INTEGER,
	"amount"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("class_id") REFERENCES "class"("id") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("feetype_id") REFERENCES "feetype"("id")  ON DELETE CASCADE ON UPDATE CASCADE)""")
    conn.commit()

    # Creating the "student" table
    conn.execute("""CREATE TABLE IF NOT EXISTS "student" (
	"id"	INTEGER,
	"name"	varchar(100),
	"class_id"	INTEGER,
	"gender"	varchar(25),
	"dob"	varchar(20),
	"father"	varchar(100),
	"mother"	varchar(100),
	"phone"	varchar(40),
	"email"	varchar(40),
	"tAddr"	varchar(150),
	"pAddr"	varchar(150),
	"dor"	varchar(20),
	"prev_school"	varchar(150),
	"prev_class"	varchar(50),
	"status"	varchar(20),
	"photo"	BLOB,
	FOREIGN KEY("class_id") REFERENCES "class"("id"),
	PRIMARY KEY("id" AUTOINCREMENT))""")
    conn.commit()

    # Creating the "std_attendance" table
    conn.execute("""CREATE TABLE IF NOT EXISTS "std_attendance" (
	"id"	INTEGER,
	"std_id"	INTEGER,
	"date"	varchar(20),
	"status"	varchar(10),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("std_id") REFERENCES "student"("id"))""")
    conn.commit()
    
	    # ======Face Encodings Data in JSON file=======
    if not os.path.exists("Database/face_encodings.json"):
        IDs = []
        Names = []
        Class = []
        encodelistknown = []

        face_encodings = {"IDs":IDs,"Names":Names,"Class":Class,"Encodings":encodelistknown}

        with open("Database/face_encodings.json","w") as f:
            json.dump(face_encodings,f,indent=2)

if __name__=="__main__":          
	create_db()
