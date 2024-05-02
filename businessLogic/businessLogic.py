from network.client import Client
from network.protocol import Request, Response
from database.database import Database
from .routesHandler import RoutesHandler
from .requestValidator import RequestValidator
import base64
import uuid
import time


class BusinessLogic:
    __instance: "BusinessLogic | None" = None

    @classmethod
    def getInstance(cls) -> "BusinessLogic":
        if cls.__instance == None:
            cls.__instance = cls()

        return cls.__instance

    def __init__(self) -> None:
        if BusinessLogic.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            BusinessLogic.__instance = self

    def handleClient(self, request: Request, client: Client):
        print("Client connected from", client.clientAddress)

        if request.method == Request.RequestMethod.OPTIONS:
            response: Response = Response.success("OPTIONS!")
        else:
            response: Response = RoutesHandler.handle(request)(request)

        response.setHeader("Access-Control-Allow-Origin", "*")
        response.setHeader("Access-Control-Allow-Headers", "*")
        response.setHeader("Access-Control-Allow-Methods", "*")

        # print(response)
        client.send(response)

    @staticmethod
    @RoutesHandler.route("/me", Request.RequestMethod.GET)
    @RequestValidator.authenticated
    def me(request: Request) -> Response:
        return Response.success({"username": request.user["username"]})

    @staticmethod
    @RoutesHandler.route("/register", Request.RequestMethod.POST)
    def register(request: Request) -> Response:
        if not RequestValidator.register(request):
            return Response.error("Invalid Request")

        user = (
            Database.getInstance()
            .execute(
                "SELECT * FROM users WHERE email = ? OR username = ?",
                (
                    request.payload["email"],
                    request.payload["username"],
                ),
            )
            .fetchOne()
        )

        if user is not None:
            return Response.error(
                "Email and/or username already exists!",
                statusCode=Response.StatusCode.OK,
            )

        token = uuid.uuid4().hex

        Database.getInstance().execute(
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

    @staticmethod
    @RoutesHandler.route("/login", Request.RequestMethod.POST)
    def login(request: Request) -> Response:
        if not RequestValidator.login(request):
            return Response.error("Invalid Request")

        user = (
            Database.getInstance()
            .execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (
                    request.payload["username"],
                    request.payload["password"],
                ),
            )
            .fetchOne()
        )

        if user is None:
            return Response.error(
                "Username and/or password are incorrect!",
                statusCode=Response.StatusCode.OK,
            )

        return Response.success({"token": user["token"]})

    @staticmethod
    @RoutesHandler.route("/wishlist", Request.RequestMethod.GET)
    @RequestValidator.authenticated
    def wishlist(request: Request) -> Response:
        wishlist = (
            Database.getInstance()
            .execute(
                "SELECT productID FROM wishlists WHERE username = ?",
                (request.user["username"],),
            )
            .fetchAll()
        )

        products = []

        for p in wishlist:
            product = (
                Database.getInstance()
                .execute(
                    "SELECT * FROM products WHERE productID = ?", (p["productID"],)
                )
                .fetchOne()
            )

            if product == None:
                Database.getInstance().execute(
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

    @staticmethod
    @RoutesHandler.route("/product/:id", Request.RequestMethod.GET)
    @RequestValidator.authenticated
    def product(request: Request) -> Response:
        product = (
            Database.getInstance()
            .execute("SELECT * FROM products WHERE productID = ?", (request.url[1],))
            .fetchOne()
        )

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

    @staticmethod
    @RoutesHandler.route("/", Request.RequestMethod.GET)
    def index(request: Request) -> Response:
        return Response.success("Hello World!")

    @staticmethod
    @RoutesHandler.route("/ping", Request.RequestMethod.POST)
    def ping(request: Request) -> Response:
        return Response.success(str(time.time()))
