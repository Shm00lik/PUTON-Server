# import requests

# url = "http://localhost:3339/register"

# payload = {"username": "testUn", "password": "testPass"}

# r = requests.post(url, data=payload)
# print(r.text)

# from database.database import Database
# import base64

# db = Database.get_instance()

# db.execute(
#     "INSERT INTO wishlists (productID, username) VALUES (?, ?)", (123, "yali1234")
# )