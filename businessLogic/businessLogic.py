from httpLib.client import Client
from httpLib.protocol import Request, Response
from config import Config
from sqliteLib.database import Database
from sqliteLib.table import Table, FetchType
from .requestType import RequestType
from .requestValidator import RequestValidator


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
        self.db = Database.getInstance(Config.DATABASE_PATH)
        self.usersTable = Table("users")
        self.wishlistsTable = Table("wishlists")
        self.productsTable = Table("products")

    def handleClient(self, request: Request, client: Client):
        print("Client connected from", client.clientAddress)

        requestType = RequestType.fromUrl(request.url)
        response: Response | None = None

        if request.method == Request.RequestMethod.POST:
            if requestType == RequestType.REGISTER:
                response = self.register(request)

            elif requestType == RequestType.LOGIN:
                response = self.login(request)

        elif request.method == Request.RequestMethod.GET:
            if requestType == RequestType.GET_WISHLIST:
                response = self.getWishlist(request)

            elif requestType == RequestType.GET_PRODUCT:
                response = self.getProduct(request)

            else:
                response = Response(
                    content="Hello, World!",
                    statusCode=Response.StatusCode.OK,
                )

        if response is None:
            response = Response(
                content="Please check your request and try again",
                statusCode=Response.StatusCode.NOT_FOUND,
            )

        # response.setHeader("CTF", Config.CTF_FLAG)
        response.setHeader("Access-Control-Allow-Origin", "*")

        print(response)
        client.send(response)

    def register(self, request: Request) -> Response:
        if not RequestValidator.register(request):
            return Response.error("Invalid request")

        user = (
            self.usersTable.select("*")
            .where(
                operator="OR",
                email=request.payload["email"],
                username=request.payload["username"],
            )
            .execute(fetchType=FetchType.ONE)
        )

        if user is not None:
            return Response.error(
                "Email and/or username already exists!",
                statusCode=Response.StatusCode.CONFLICT,
            )

        self.usersTable.insert(
            email=request.payload["email"],
            username=request.payload["username"],
            password=request.payload["password"],
        ).execute()

        return Response.success("Registered successfully!")

    def login(self, request: Request) -> Response:
        if not RequestValidator.login(request):
            return Response.error("Invalid request")

        user = (
            self.usersTable.select("*")
            .where(
                username=request.payload["username"],
                password=request.payload["password"],
            )
            .execute(fetchType=FetchType.ONE)
        )

        if user is None:
            return Response.error(
                "Username and/or password are incorrect!",
                statusCode=Response.StatusCode.UNAUTHORIZED,
            )

        return Response.success("Logged in successfully!")

    def getWishlist(self, request: Request) -> Response:
        if not RequestValidator.getWishlist(request):
            return Response.error("Invalid request")
        
        wishlist = (
            self.wishlistsTable.select("productID")
            .where(
                username=request.params["username"]
            )
            .execute(fetchType=FetchType.ALL)
        )

        wishlist = list(map(lambda x: x[0], wishlist))

        return Response.success(wishlist)
    
    def getProduct(self, request: Request) -> Response:
        if not RequestValidator.getProduct(request):
            return Response.error("Invalid request")

        product = (
            self.productsTable.select("*")
            .where(
                productID=request.params["productID"]
            )
            .execute(fetchType=FetchType.ONE)
        )
        
        print(type(product[1]))

        return Response.success(product)
