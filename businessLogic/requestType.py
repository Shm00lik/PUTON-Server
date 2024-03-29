from enum import Enum


class RequestType(Enum):
    UNKNOWN = "unknown"

    REGISTER = "register"
    LOGIN = "login"
    WISHLIST = "wishlist"
    PRODUCT = "product"
    ME = "me"
    
    @staticmethod
    def fromUrl(url: list[str]) -> "RequestType":
        mapper: dict = {v.value: v for v in RequestType}

        if url[0] == "":
            return RequestType.UNKNOWN

        if url[0] not in mapper:
            return RequestType.UNKNOWN

        return mapper[url[0]]