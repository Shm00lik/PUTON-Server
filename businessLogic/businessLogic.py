from network.client import Client
from network.encryption.diffieHellman import DiffieHellman, DiffieHellmanState
from network.protocol import Request, Response
from network.encryption.AES import AES
from database.database import Database
from .routesHandler import RoutesHandler
from .requestValidator import RequestValidator
import base64
import uuid
import time
import hashlib


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
            print(request.url)
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
        sharedKey = (
            Database.getInstance()
            .execute(
                "SELECT sharedKey FROM encryption WHERE encryptionToken = ?",
                (request.headers["encryptionToken"],),
            )
            .fetchOne()
        )

        if sharedKey is None:
            return Response.error("Invalid Request")

        return Response.success(
            {"username": request.user["username"], "email": request.user["email"]},
            key=sharedKey["sharedKey"],
        )

    @staticmethod
    @RoutesHandler.route("/register", Request.RequestMethod.POST)
    def register(request: Request) -> Response:
        if not RequestValidator.register(request):
            return Response.error("Invalid Request")

        user = (
            Database.getInstance()
            .execute(
                "SELECT * FROM users WHERE email = ? OR username = ?",
                (request.payload["email"], request.payload["username"]),
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
            "INSERT INTO users (email, username, password, token) VAlUES (?, ?, ?, ?)",
            (
                request.payload["email"],
                request.payload["username"],
                request.payload["password"],
                token,
            ),
        )

        return Response.success({"token": token})

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

            with open(f"./database/images/{product['productID']}.png", "rb") as im:
                image = base64.b64encode(im.read()).decode("utf-8")

            product = {
                "productID": product["productID"],
                "title": product["title"],
                "description": product["description"],
                "price": product["price"],
                "image": image,
                "inWishlist": True,
            }

            products.append(product)

        return Response.success(products)

    @staticmethod
    @RoutesHandler.route("/wishlistProduct", Request.RequestMethod.POST)
    @RequestValidator.authenticated
    def wishlistProduct(request: Request) -> Response:
        if not RequestValidator.wishlistProduct(request):
            return Response.error("Invalid Request")

        isInWishlist = (
            Database.getInstance()
            .execute(
                "SELECT * FROM wishlists WHERE username = ? AND productID = ?",
                (request.user["username"], request.payload["id"]),
            )
            .fetchOne()
            != None
        )

        if isInWishlist:
            Database.getInstance().execute(
                "DELETE FROM wishlists WHERE username = ? AND productID = ?",
                (request.user["username"], request.payload["id"]),
            )

        else:
            Database.getInstance().execute(
                "INSERT INTO wishlists (productID, username) VALUES (?, ?)",
                (request.payload["id"], request.user["username"]),
            )

        return Response.success(
            ("Removed From " if isInWishlist else "Added To") + " Wishlist."
        )

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

        isInWishlist = (
            Database.getInstance()
            .execute(
                "SELECT * FROM wishlists WHERE username = ? AND productID = ?",
                (request.user["username"], request.url[1]),
            )
            .fetchOne()
            != None
        )

        with open(f"./database/images/{product['productID']}.png", "rb") as im:
            image = base64.b64encode(im.read()).decode("utf-8")

        product = {
            "productID": product["productID"],
            "title": product["title"],
            "description": product["description"],
            "price": product["price"],
            "image": image,
            "inWishlist": isInWishlist,
            "leftEyeX": product["leftEyeX"],
            "leftEyeY": product["leftEyeY"],
            "rightEyeX": product["rightEyeX"],
            "rightEyeY": product["rightEyeY"],
        }

        return Response.success(product)

    @staticmethod
    @RoutesHandler.route("/products", Request.RequestMethod.GET)
    @RequestValidator.authenticated
    def products(request: Request) -> Response:
        if not RequestValidator.products(request):
            return Response.error("Invalid Request")

        ps = (
            Database.getInstance()
            .execute(
                "SELECT * FROM products ORDER BY productID LIMIT ? OFFSET ?",
                (
                    request.params["amount"],
                    int(request.params["page"]) * int(request.params["amount"]),
                ),
            )
            .fetchAll()
        )

        products = []

        for p in ps:
            with open(f"./database/images/{p['productID']}.png", "rb") as im:
                image = base64.b64encode(im.read()).decode("utf-8")

            product = {
                "productID": p["productID"],
                "title": p["title"],
                "description": p["description"],
                "price": p["price"],
                "image": image,
                "inWishlist": False,
                "leftEyeX": p["leftEyeX"],
                "leftEyeY": p["leftEyeY"],
                "rightEyeX": p["rightEyeX"],
                "rightEyeY": p["rightEyeY"],
            }

            products.append(product)

        return Response.success(products)

    @staticmethod
    @RoutesHandler.route("/", Request.RequestMethod.GET)
    def index(request: Request) -> Response:
        return Response.success("Hello World!")

    @staticmethod
    @RoutesHandler.route("/ping", Request.RequestMethod.POST)
    def ping(request: Request) -> Response:
        return Response.success(str(time.time()))

    @staticmethod
    @RoutesHandler.route("/handshake/init", Request.RequestMethod.POST)
    def handshakeInit(request: Request) -> Response:
        if not RequestValidator.handshake(request, DiffieHellmanState.INITIALIZING):
            return Response.error("Invalid Request")

        print(DiffieHellman.get_public_params())

        return Response.success(DiffieHellman.get_public_params())

    @staticmethod
    @RoutesHandler.route("/handshake/exchange", Request.RequestMethod.POST)
    def handshakeExchange(request: Request) -> Response:
        if not RequestValidator.handshake(request, DiffieHellmanState.EXCHANGING_KEYS):
            return Response.error("Invalid Request")

        serverPrivateKey = DiffieHellman.generate_private_key()
        sharedDiffieHellmanKey = DiffieHellman.generate_shared_key(
            int(request.payload["publicKey"]), serverPrivateKey
        )

        sharedKey = hashlib.sha256(str(sharedDiffieHellmanKey).encode()).hexdigest()

        Database.getInstance().execute(
            "INSERT INTO encryption (encryptionToken, serverPrivateKey, sharedKey) VALUES (?, ?, ?)",
            (request.payload["encryptionToken"], serverPrivateKey, sharedKey),
        )

        print("Created shared key: " + sharedKey)

        return Response.success(
            {"serverPublicKey": DiffieHellman.generate_public_key(serverPrivateKey)}
        )
