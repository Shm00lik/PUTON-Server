import sqlite3
import base64
from config import Config


class User:
    def __init__(self, username: str, email: str, password: str, token: str):
        self.username = username
        self.email = email
        self.password = password
        self.token = token

    @staticmethod
    def from_database(user: sqlite3.Row) -> "User":
        return User(
            username=user["username"],
            email=user["email"],
            password=user["password"],
            token=user["token"],
        )

    @staticmethod
    def default() -> "User":
        return User(username="", email="", password="", token="")


class Product:
    def __init__(
        self,
        product_id: int,
        title: str,
        description: str,
        price: float,
        is_in_wishlist: bool,
        left_eye_data: dict[str, int],
        right_eye_data: dict[str, int],
    ) -> None:
        self.product_id = product_id
        self.title = title
        self.description = description
        self.price = price
        self.is_in_wishlist = is_in_wishlist
        self.left_eye_data = left_eye_data
        self.right_eye_data = right_eye_data

        with open(
            f"{Config.PRODUCT_IMAGES_PATH}/{product_id}.{Config.PRODUCT_IMAGES_SUBFIX}",
            "rb",
        ) as im:
            self.image = base64.b64encode(im.read()).decode("utf-8")

    def to_dict(
        self, with_eyes_data: bool = True
    ) -> dict[str, str | int | float | bool]:
        if with_eyes_data:
            return {
                "productID": self.product_id,
                "title": self.title,
                "description": self.description,
                "price": self.price,
                "image": self.image,
                "inWishlist": self.is_in_wishlist,
                "leftEyeX": self.left_eye_data["x"],
                "leftEyeY": self.left_eye_data["y"],
                "rightEyeX": self.right_eye_data["x"],
                "rightEyeY": self.right_eye_data["y"],
            }

        return {
            "productID": self.product_id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "image": self.image,
            "inWishlist": self.is_in_wishlist,
        }

    @staticmethod
    def from_database(product: sqlite3.Row) -> "Product":
        return Product(
            product_id=product["productID"],
            title=product["title"],
            description=product["description"],
            price=product["price"],
            is_in_wishlist=True,
            left_eye_data={"x": product["leftEyeX"], "y": product["leftEyeY"]},
            right_eye_data={"x": product["rightEyeX"], "y": product["rightEyeY"]},
        )
