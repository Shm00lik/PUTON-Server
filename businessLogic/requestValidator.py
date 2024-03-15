from httpLib.protocol import Request


class RequestValidator:
    @staticmethod
    def register(request: Request) -> bool:
        return "username" in request.payload and "password" in request.payload

    @staticmethod
    def login(request: Request) -> bool:
        return "username" in request.payload and "password" in request.payload

    @staticmethod
    def getWishlist(request: Request) -> bool:
        return "username" in request.params
    
    @staticmethod
    def getProduct(request: Request) -> bool:
        return "productID" in request.params