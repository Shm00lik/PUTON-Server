from httpLib.protocol import Request, Response
from sqliteLib.table import Table, FetchType


class RequestValidator:
    @staticmethod
    def register(request: Request) -> bool:
        return "username" in request.payload and "password" in request.payload

    @staticmethod
    def login(request: Request) -> bool:
        return "username" in request.payload and "password" in request.payload

    @staticmethod
    def authenticated(func):
        def wrapper(*args, **kwargs):
            request = args[1]

            users = Table('users')
            print(request.headers['Token'])
            user = users.select("*").where(
                token=request.headers['Token']
            ).execute(fetchType=FetchType.ONE)

            if user == None:
                print("NOT AUTHED")
                return Response.error("Not Authenticated")

            request.user = user
            
            return func(*args, **kwargs)
            
        return wrapper 