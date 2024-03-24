# import requests

# url = "http://localhost:3339/register"

# payload = {"username": "testUn", "password": "testPass"}

# r = requests.post(url, data=payload)
# print(r.text)

from sqliteLib.table import Table, FetchType
from sqliteLib.database import Database
import base64

db = Database.getInstance("./database/database.sqlite")
# db.execute("DROP TABLE users")

table = Table("wishlists")

# table.create(
#     'id INTEGER PRIMARY KEY',
#     'email TEXT NOT NULL',
#     'username TEXT NOT NULL',
#     'password TEXT NOT NULL',
#     'token TEXT NOT NULL',
# ).execute()

# a = table.select("usename", "password").where(usename="Yoav", password="1234")

# print(a.execute(fetchType=FetchType.MANY, fetchSize=4))

table.insert(username="yali1234", productID=123).execute()

# table.insert(productID="123", title="Toaster", description="The best toaster in the world!", price=16.90).execute()
# table.insert(productID="123", title="Toaster", description="The best toaster in the world!", price=16.90).execute()
# db.execute('ALTER TABLE users ADD COLUMN token TEXT')
# table.delete().where(username="yali1234").execute()
# print("ASD")
