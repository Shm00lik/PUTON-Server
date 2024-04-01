from typing import Callable
from network.protocol import Request, Response


class RoutesHandler:
    routes: dict[tuple[str, Request.RequestMethod], Callable[[Request], Response]] = {}

    @classmethod
    def route(cls, pattern: str, method: Request.RequestMethod):
        def decorator(
            func: Callable[[Request], Response]
        ) -> Callable[[Request], Response]:
            if pattern.startswith("/"):
                cls.routes[(pattern[1:], method)] = func
            else:
                cls.routes[(pattern, method)] = func

            return func

        return decorator

    @classmethod
    def handle(cls, request: Request) -> Callable[[Request], Response]:
        filteredRoutes = list(
            filter(lambda x: x[0][1] == request.method, cls.routes.items())
        )
        routes = list(map(lambda x: (x[0][0], x[1]), filteredRoutes))

        for pattern, handler in routes:
            patternsParts = pattern.split("/")

            if len(patternsParts) == len(request.url):
                for i in range(len(patternsParts)):
                    if patternsParts[i].startswith(":"):
                        continue

                    elif patternsParts[i] != request.url[i]:
                        handler = cls.defaultRoute
                        break
                else:
                    return handler

        return cls.defaultRoute

    @staticmethod
    def defaultRoute(request: Request):
        return Response.error("Please check your request and try again")
