from network.encryption.AES import AES
from network.encryption.diffie_hellman import DiffieHellman, DiffieHellmanState
from network.protocol import Response, HTTPMethod
from network.data import Data
from network.router import Router
from utils.models import Product
from utils.utils import generate_salt
import utils.checks as chekcs
import uuid
import time
import hashlib


@Router.route("/me", HTTPMethod.GET)
@chekcs.authenticated
def me(data: Data) -> Response:
    return Response.success(
        {"username": data.user.username, "email": data.user.email},
    )


@Router.route("/register", HTTPMethod.POST)
def register(data: Data) -> Response:
    if not chekcs.register(data.request):
        return Response.error("Invalid Request")

    user = data.db.execute(
        "SELECT * FROM users WHERE email = ? OR username = ?",
        (
            data.request.payload.get("email"),
            data.request.payload.get("username"),
        ),
    ).fetch_one()

    if user is not None:
        return Response.error(
            "Email and/or username already exists!",
        )

    token = uuid.uuid4().hex
    salt = generate_salt()
    salted_password = str(data.request.payload.get("password")) + salt

    data.db.execute(
        "INSERT INTO users (email, username, password, token, salt) VAlUES (?, ?, ?, ?, ?)",
        (
            data.request.payload.get("email"),
            data.request.payload.get("username"),
            hashlib.sha256(salted_password.encode()).hexdigest(),
            token,
            salt,
        ),
    )

    return Response.success({"message": "Registered successfully!", "token": token})


@Router.route("/login", HTTPMethod.POST)
def login(data: Data) -> Response:
    if not chekcs.login(data.request):
        return Response.error("Invalid Request")

    user = data.db.execute(
        "SELECT * FROM users WHERE username = ?",
        (data.request.payload.get("username"),),
    ).fetch_one()

    if user is None:
        return Response.error(
            "Username and/or password are incorrect!",
        )

    salted_password = str(data.request.payload.get("password")) + str(user["salt"])

    if user["password"] != hashlib.sha256(salted_password.encode()).hexdigest():
        return Response.error(
            "Username and/or password are incorrect!",
        )

    return Response.success(
        {"message": "Logged in successfully!", "token": user["token"]}
    )


@Router.route("/wishlist", HTTPMethod.GET)
@chekcs.authenticated
def wishlist(data: Data) -> Response:
    wishlist = data.db.execute(
        "SELECT productID FROM wishlists WHERE token = ?",
        (data.user.token,),
    ).fetch_all()

    products: list[Product] = []

    for p in wishlist:
        product = data.db.execute(
            "SELECT * FROM products WHERE productID = ?", (p["productID"],)
        ).fetch_one()

        if product == None:
            data.db.execute(
                "DELETE FROM wishlists WHERE productID = ?", (p["productID"],)
            )
            continue

        products.append(Product.from_database(product))

    return Response.success(list(map(lambda p: p.to_dict(False), products)))


@Router.route("/wishlistProduct", HTTPMethod.POST)
@chekcs.authenticated
def wishlist_product(data: Data) -> Response:
    if not chekcs.wishlist_product(data.request):
        return Response.error("Invalid Request")

    isInWishlist = (
        data.db.execute(
            "SELECT * FROM wishlists WHERE token = ? AND productID = ?",
            (data.user.token, data.request.payload.get("id")),
        ).fetch_one()
        != None
    )

    if isInWishlist:
        data.db.execute(
            "DELETE FROM wishlists WHERE token = ? AND  productID = ? ",
            (data.user.token, data.request.payload.get("id")),
        )

    else:
        data.db.execute(
            "INSERT INTO wishlists (token, productID) VALUES (?, ?)",
            (data.user.token, data.request.payload.get("id")),
        )

    return Response.success(
        ("Removed From " if isInWishlist else "Added To") + " Wishlist."
    )


@Router.route("/product/:id", HTTPMethod.GET)
@chekcs.authenticated
def product(data: Data) -> Response:
    if not chekcs.product(data.request):
        return Response.error("Invalid Request")

    product = data.db.execute(
        "SELECT * FROM products WHERE productID = ?",
        (data.request.path_variables[1],),
    ).fetch_one()

    if product == None:
        return Response.error("Product not found!")

    in_wishlist = (
        data.db.execute(
            "SELECT * FROM wishlists WHERE token = ? AND productID = ?",
            (data.user.token, data.request.path_variables[1]),
        ).fetch_one()
        != None
    )

    product = Product.from_database(product, in_wishlist)

    return Response.success(product.to_dict())


@Router.route("/products", HTTPMethod.GET)
@chekcs.authenticated
def products(data: Data) -> Response:
    if not chekcs.products(data.request):
        return Response.error("Invalid Request")

    amount = int(data.request.params.get("amount") or 5)
    page = int(data.request.params.get("page") or 0)
    offset = page * amount

    ps = data.db.execute(
        "SELECT * FROM products ORDER BY productID LIMIT ? OFFSET ?",
        (
            amount,
            offset,
        ),
    ).fetch_all()

    products: list[Product] = []

    for p in ps:
        products.append(Product.from_database(p))

    return Response.success(list(map(lambda p: p.to_dict(), products)))


@Router.route("/", HTTPMethod.GET)
def index(data: Data) -> Response:
    return Response.success("Hello World!")


@Router.route("/ping", HTTPMethod.GET)
def ping(data: Data) -> Response:
    return Response.success({"now": time.time()})


@Router.route("/handshake/init", HTTPMethod.POST, encrypted=False)
def handshake_init(data: Data) -> Response:
    if not chekcs.handshake(data.request, DiffieHellmanState.INITIALIZING):
        return Response.error("Invalid Request")

    return Response.success(DiffieHellman.get_public_params())


@Router.route("/handshake/exchange", HTTPMethod.POST, encrypted=False)
def handshake_exchange(data: Data) -> Response:
    if not chekcs.handshake(data.request, DiffieHellmanState.EXCHANGING_KEYS):
        return Response.error("Invalid Request")

    server_private_key = DiffieHellman.generate_private_key()
    shared_diffie_hellman_key = DiffieHellman.generate_shared_key(
        int(data.request.payload.get("publicKey") or 0), server_private_key
    )

    shared_key = AES.diffie_hellman_key_to_aes_key(shared_diffie_hellman_key)

    data.server.add_encryption(
        int(data.request.payload.get("encryptionToken") or 0), shared_key
    )

    print("Created shared key: " + shared_key)

    return Response.success(
        {"serverPublicKey": DiffieHellman.generate_public_key(server_private_key)}
    )
