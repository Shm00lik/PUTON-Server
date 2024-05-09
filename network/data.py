from .protocol import Request
from database.database import Database
from utils.models import User


class Data:
    def __init__(self, request: Request, db: Database, client, server):
        self.request = request
        self.db = db
        self.client = client
        self.server = server
        self.user = User.default()
