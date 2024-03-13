# import requests

# url = "http://localhost:3339/register"

# payload = {"username": "testUn", "password": "testPass"}

# r = requests.post(url, data=payload)
# print(r.text)

from sqliteLib.table import Table, FetchType
from sqliteLib.database import Database

db = Database.getInstance("./database/database.sqlite")

table = Table("wishlists")

table.create(
    "productID INTEGER NOT NULL",
    "username TEXT NOT NULL",
).execute()

# db.execute("DROP TABLE users")
# a = table.select("usename", "password").where(usename="Yoav", password="1234")

# print(a.execute(fetchType=FetchType.MANY, fetchSize=4))

table.insert(username="yali1234", productID="1234").execute()
# print("ASD")
