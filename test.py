import sqlite3

con = sqlite3.connect("Database/sms.db")
cur = con.cursor()
cur.execute("Select count(*) from student")
rows = cur.fetchone()
print(rows[0])