# import requests

# url = "http://localhost:3339/register"

# payload = {"username": "testUn", "password": "testPass"}

# r = requests.post(url, data=payload)
# print(r.text)

from utils.database import Table, FetchType

table = Table("users")
# table.create("usename TEXT NOT NULL", "password TEXT NOT NULL").execute()

a = (
    table
    .select("usename", "password")
    .where(usename="Yoav", password="1234")
    .execute(fetchType=FetchType.ALL)
)

print(a)

# table.insert(usename="Yoav", password="1234").execute()
# print("ASD")
