from .protocol import Request
from database.database import Database
from utils.models import User


class Data:
    """
    A class representing data associated with a request.
    """

    def __init__(self, request: Request, db: Database, client, server):
        """
        Initializes the Data instance.

        Args:
        - request (Request): The request associated with the data.
        - db (Database): The database instance.
        - client: The client associated with the request.
        - server: The server handling the request.
        """
        self.request = request
        self.db = db
        self.client = client
        self.server = server
        self.user = User.default()
