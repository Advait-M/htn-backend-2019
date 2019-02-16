import sqlite3
import urllib.request
import json

with urllib.request.urlopen("https://htn-interviews.firebaseio.com/users.json") as url:
    data = json.loads(url.read().decode())

DB_NAME = "htn.db"
conn = sqlite3.connect(DB_NAME)

c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users
(email text primary key, name text, picture text, company text, phone text, latitude real, longitude real)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS skills
(email text, name text, rating text, foreign key (email) references users(email))
''')

for i in data:
    try:
        c.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
            (i["email"],
             i["name"],
                i["picture"],
                i["company"],
                i["phone"],
                i["latitude"],
                i["longitude"]))
    except sqlite3.IntegrityError:
        print("User already in database:", i["email"])
        continue
    for skill in i["skills"]:
        c.execute("INSERT INTO skills VALUES (?, ?, ?)",
                  (i["email"], skill["name"], skill["rating"]))

conn.commit()

conn.close()
