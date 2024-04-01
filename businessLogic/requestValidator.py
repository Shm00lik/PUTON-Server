from network.protocol import Request, Response
from database.database import Database


class RequestValidator:
    @staticmethod
    def register(request: Request) -> bool:
        return "username" in request.payload and "password" in request.payload

    @staticmethod
    def login(request: Request) -> bool:
        return "username" in request.payload and "password" in request.payload

    @staticmethod
    def authenticated(func):
        def wrapper(request: Request):
            if "token" not in request.headers:
                return Response.error("Not Authenticated")

            user = (
                Database.getInstance()
                .execute(
                    "SELECT * FROM users WHERE token = ?", (request.headers["token"],)
                )
                .fetchOne()
            )

            if user == None:
                return Response.error("Not Authenticated")

            request.user = user

            return func(request)

        return wrapper
