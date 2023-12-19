# import requests

# url = "http://localhost:3339/register"

# payload = {"username": "testUn", "password": "testPass"}

# r = requests.post(url, data=payload)
# print(r.text)

from sqliteLib.table import Table, FetchType
from sqliteLib.database import Database

db = Database.getInstance("./database/database.sqlite")

table = Table("users")
table.create("username TEXT NOT NULL", "password TEXT NOT NULL").execute()

# a = table.select("usename", "password").where(usename="Yoav", password="1234")

# print(a.execute(fetchType=FetchType.MANY, fetchSize=4))

# table.insert(usename="Yoav", password="1234").execute()
# print("ASD")
