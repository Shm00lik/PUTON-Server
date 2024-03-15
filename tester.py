# import requests

# url = "http://localhost:3339/register"

# payload = {"username": "testUn", "password": "testPass"}

# r = requests.post(url, data=payload)
# print(r.text)

from sqliteLib.table import Table, FetchType
from sqliteLib.database import Database
import base64

db = Database.getInstance("./database/database.sqlite")
db.execute("DROP TABLE products")

table = Table("products")

table.create(
    "productID INTEGER NOT NULL UNIQUE",
    "title TEXT NOT NULL",
    "description TEXT NOT NULL",
    "price REAL NOT NULL",
    "image TEXT NOT NULL"
).execute()

# a = table.select("usename", "password").where(usename="Yoav", password="1234")

# print(a.execute(fetchType=FetchType.MANY, fetchSize=4))

with open("71n-oeNV6BL.jpg", "rb") as image_file:
    data = image_file.read()

# print(data)

table.insert(productID="1234", title="Toaster", description="The best toaster in the world!", price=16.90, image=data).execute()
# print("ASD")
