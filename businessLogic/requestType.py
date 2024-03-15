from enum import Enum


class RequestType(Enum):
    UNKNOWN = "unknown"

    REGISTER = "register"
    LOGIN = "login"
    GET_WISHLIST = "getWishlist"
    GET_PRODUCT = "getProduct"
    
    @staticmethod
    def fromUrl(url: str) -> "RequestType":
        mapper: dict = {v.value: v for v in RequestType}

        if "/" not in url:
            return RequestType.UNKNOWN

        if url.split("/")[1] not in mapper:
            return RequestType.UNKNOWN

        return mapper[url.split("/")[1]]