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
        def wrapper(self, request):
            user = (
                Database.getInstance()
                .execute(
                    "SELECT * FROM users WHERE token = ?", (request.headers["Token"],)
                )
                .fetchOne()
            )

            if user == None:
                return Response.error("Not Authenticated")

            request.user = user

            return func(self, request)

        return wrapper
