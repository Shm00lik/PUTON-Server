import sqlite3
import base64
from config import Config


class User:
    """
    A class representing a user in the system.
    """

    def __init__(self, username: str, email: str, password: str, token: str, salt: str):
        """
        Initializes the User object.

        Args:
        - username (str): The username of the user.
        - email (str): The email address of the user.
        - password (str): The hashed password of the user.
        - token (str): The authentication token of the user.
        """
        self.username = username
        self.email = email
        self.password = password
        self.token = token
        self.salt = salt

    @staticmethod
    def from_database(user: sqlite3.Row) -> "User":
        """
        Creates a User object from a database row.

        Args:
        - user (sqlite3.Row): The database row representing the user.

        Returns:
        - User: The User object created from the database row.
        """
        return User(
            username=user["username"],
            email=user["email"],
            password=user["password"],
            token=user["token"],
            salt=user["salt"],
        )

    @staticmethod
    def default() -> "User":
        """
        Creates a default User object with empty attributes.

        Returns:
        - User: The default User object.
        """
        return User(username="", email="", password="", token="", salt="")


class Product:
    """
    A class representing a product in the system.
    """

    def __init__(
        self,
        product_id: int,
        title: str,
        description: str,
        price: float,
        in_wishlist: bool,
        left_eye_data: dict[str, int],
        right_eye_data: dict[str, int],
    ) -> None:
        """
        Initializes the Product object.

        Args:
        - product_id (int): The ID of the product.
        - title (str): The title of the product.
        - description (str): The description of the product.
        - price (float): The price of the product.
        - left_eye_data (dict[str, int]): The data related to the left eye of the product.
        - right_eye_data (dict[str, int]): The data related to the right eye of the product.
        """
        self.product_id = product_id
        self.title = title
        self.description = description
        self.price = price
        self.in_wishlist = in_wishlist
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
        """
        Converts the Product object to a dictionary.

        Args:
        - with_eyes_data (bool): Whether to include eye data in the dictionary.

        Returns:
        - dict: The dictionary representation of the Product object.
        """
        if with_eyes_data:
            return {
                "productID": self.product_id,
                "title": self.title,
                "description": self.description,
                "price": self.price,
                "image": self.image,
                "inWishlist": self.in_wishlist,
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
            "inWishlist": self.in_wishlist,
        }

    @staticmethod
    def from_database(product: sqlite3.Row, in_wishlist: bool = True) -> "Product":
        """
        Creates a Product object from a database row.

        Args:
        - product (sqlite3.Row): The database row representing the product.

        Returns:
        - Product: The Product object created from the database row.
        """
        return Product(
            product_id=product["productID"],
            title=product["title"],
            description=product["description"],
            price=product["price"],
            in_wishlist=in_wishlist,
            left_eye_data={"x": product["leftEyeX"], "y": product["leftEyeY"]},
            right_eye_data={"x": product["rightEyeX"], "y": product["rightEyeY"]},
        )
