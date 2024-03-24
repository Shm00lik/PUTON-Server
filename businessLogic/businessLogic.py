from httpLib.client import Client
from httpLib.protocol import Request, Response
from config import Config
from sqliteLib.database import Database
from sqliteLib.table import Table, FetchType
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
            if requestType == RequestType.WISHLIST:
                response = self.wishlist(request)

            elif requestType == RequestType.PRODUCT:
                response = self.product(request)

            else:
                response = Response.error("Hello, World!")

        if response is None:
            response = Response.error("Please check your request and try again",)

        # response.setHeader("CTF", Config.CTF_FLAG)
        response.setHeader("Access-Control-Allow-Origin", "*")
        response.setHeader("Access-Control-Allow-Headers", "*")
        response.setHeader("Access-Control-Allow-Methods", "*")

        # print(response)
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
                statusCode=Response.StatusCode.OK,
            )

        token = uuid.uuid4().hex

        self.usersTable.insert(
            email=request.payload["email"],
            username=request.payload["username"],
            password=request.payload["password"],
            token=token
        ).execute()

        return Response.success('Registered Successfully').setHeader('Set-Cookie', f"Token={token}")
    
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
                statusCode=Response.StatusCode.OK,
            )

        return Response.success("Logged in successfully!").setHeader('Set-Cookie', f"Token={user['token']}")

    @RequestValidator.authenticated
    def wishlist(self, request: Request) -> Response:
        wishlist = (
            self.wishlistsTable.select("productID")
            .where(
                username=request.user['username']
            )
            .execute(fetchType=FetchType.ALL)
        )

        wishlist = list(map(lambda x: x[0], wishlist))

        time.sleep(10)
        return Response.success(wishlist)
    
    @RequestValidator.authenticated
    def product(self, request: Request) -> Response:
        product = (
            self.productsTable.select("*")
            .where(
                productID=request.url[1]
            )
            .execute(fetchType=FetchType.ONE)
        )

        if product == None:
            return Response.error("Product not found!")
            
        with open(f"./database/images/{product['productID']}.jpg", 'rb') as im:
            image = base64.b64encode(im.read()).decode('utf-8')
        
        product = {
            'productID': product['productID'],
            'title': product['title'],
            'description': product['description'],
            'price': product['price'],
            'image': image,
        }


        return Response.success(product)
