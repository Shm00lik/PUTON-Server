# import requests

# url = "http://localhost:3339/register"

# payload = {"username": "testUn", "password": "testPass"}

# r = requests.post(url, data=payload)
# print(r.text)

from sqliteLib.table import Table, FetchType
from sqliteLib.database import Database

db = Database.getInstance("./database/database.sqlite")

table = Table("users")
table.create(
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "username TEXT NOT NULL UNIQUE",
    "email TEXT NOT NULL UNIQUE",
    "password TEXT NOT NULL",
).execute()
# db.execute("DROP TABLE users")
# a = table.select("usename", "password").where(usename="Yoav", password="1234")

# print(a.execute(fetchType=FetchType.MANY, fetchSize=4))

# table.insert(usename="Yoav", password="1234").execute()
# print("ASD")
