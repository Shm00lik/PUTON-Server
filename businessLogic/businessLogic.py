from network.client import Client
from network.protocol import Request, Response
from config import Config
from database.database import Database
from .requestType import RequestType
from .requestValidator import RequestValidator
import base64
import uuid
import time

class BusinessLogic:
    __instance = None

    @staticmethod
    def getInstance() -> "BusinessLogic":
        if BusinessLogic.__instance == None:
            BusinessLogic.__instance = BusinessLogic()

        return BusinessLogic.__instance

    def __init__(self) -> None:
        if BusinessLogic.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            BusinessLogic.__instance = self
            self.initDatabase()

    def initDatabase(self) -> None:
        self.db = Database.getInstance()

    def handleClient(self, request: Request, client: Client):
        print("Client connected from", client.clientAddress)

        requestType = RequestType.fromUrl(request.url)
        response: Response = None

        if (request.method == Request.RequestMethod.OPTIONS):
            response = Response.success("OPTIONS!")
        else:
            response = getattr(self, requestType.value)(request)
        
        # response.setHeader("CTF", Config.CTF_FLAG)
        response.setHeader("Access-Control-Allow-Origin", "*")
        response.setHeader("Access-Control-Allow-Headers", "*")
        response.setHeader("Access-Control-Allow-Methods", "*")

        # print(response)
        client.send(response)

    def unknown(self, request: Request) -> Response:
        return Response.error("Please check your request and try again")
    
    @RequestValidator.authenticated
    def me(self, request: Request) -> Response:
        return Response.success({"username": request.user["username"]})
    
    def register(self, request: Request) -> Response:
        if not RequestValidator.register(request):
            return Response.error("Invalid Request")

        user = self.db.execute(
            "SELECT * FROM users WHERE email = ? OR username = ?",
            (
                request.payload["email"],
                request.payload["username"],
            ),
        ).fetchOne()

        if user is not None:
            return Response.error(
                "Email and/or username already exists!",
                statusCode=Response.StatusCode.OK,
            )

        token = uuid.uuid4().hex

        self.db.execute(
            "INSERT INTO users (email, username, password token) VAlUES (?, ?, ?, ?)",
            (
                request.payload["email"],
                request.payload["username"],
                request.payload["password"],
                token,
            ),
        )

        return Response.success("Registered Successfully").setHeader(
            "Set-Cookie", f"Token={token}"
        )

    def login(self, request: Request) -> Response:
        if not RequestValidator.login(request):
            return Response.error("Invalid Request")

        user = self.db.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (
                request.payload["username"],
                request.payload["password"],
            ),
        ).fetchOne()

        if user is None:
            return Response.error(
                "Username and/or password are incorrect!",
                statusCode=Response.StatusCode.OK,
            )

        return Response.success({"token": user['token']})

    @RequestValidator.authenticated
    def wishlist(self, request: Request) -> Response:
        wishlist = self.db.execute(
            "SELECT productID FROM wishlists WHERE username = ?",
            (request.user["username"],),
        ).fetchAll()

        products = []

        for p in wishlist:
            product = self.db.execute(
                "SELECT * FROM products WHERE productID = ?", (p["productID"],)
            ).fetchOne()

            if product == None:
                self.db.execute(
                    "DELETE FROM wishlists WHERE productID = ?", (p["productID"],)
                )
                continue

            with open(f"./database/images/{product['productID']}.jpg", "rb") as im:
                image = base64.b64encode(im.read()).decode("utf-8")

            product = {
                "productID": product["productID"],
                "title": product["title"],
                "description": product["description"],
                "price": product["price"],
                "image": image,
            }

            products.append(product)

        return Response.success(products)

    @RequestValidator.authenticated
    def product(self, request: Request) -> Response:
        product = self.db.execute(
            "SELECT * FROM products WHERE productID = ?", (request.url[1],)
        ).fetchOne()

        if product == None:
            return Response.error("Product not found!")

        with open(f"./database/images/{product['productID']}.jpg", "rb") as im:
            image = base64.b64encode(im.read()).decode("utf-8")

        product = {
            "productID": product["productID"],
            "title": product["title"],
            "description": product["description"],
            "price": product["price"],
            "image": image,
        }

        return Response.success(product)
