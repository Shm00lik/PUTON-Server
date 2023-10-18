import sqlite3
from enum import Enum
from config import Config


class FetchType(Enum):
    NONE = 0
    ALL = 1
    ONE = 2
    MANY = 3


class Table:
    def __init__(self, name: str) -> None:
        self.name = name

        self.query = ""
        self.whereQuery = ""
        self.orderQuery = ""
        self.limitQuery = ""

    @staticmethod
    def getTable(name: str):
        return Table(name)

    def create(self, *columns: str) -> "Table":
        self.query = f"CREATE TABLE IF NOT EXISTS {self.name} ({', '.join(columns)})"
        return self

    def select(self, *columns: str) -> "Table":
        self.query = f"SELECT {', '.join(columns)} FROM {self.name}"
        return self

    def insert(self, **values: str) -> "Table":
        queryKeys = ", ".join(values.keys())
        queryValues = ", ".join([f"'{value}'" for value in values.values()])

        self.query = f"INSERT INTO {self.name} ({queryKeys}) VALUES ({queryValues})"
        return self

    def where(self, **conditions: str) -> "Table":
        self.whereQuery = "WHERE " + " AND ".join(
            [f"{key} = '{value}'" for key, value in conditions.items()]
        )
        return self

    def order(self, column: str, order: str) -> "Table":
        self.orderQuery = f"ORDER BY {column} {order}"
        return self

    def limit(self, limit: int) -> "Table":
        self.limitQuery = f"LIMIT {limit}"
        return self

    def execute(
        self,
        fetchType: FetchType = FetchType.NONE,
        fetchSize: int | None = None,
    ) -> list[tuple] | tuple | None:
        self.query += " " + self.whereQuery
        self.query += " " + self.orderQuery
        self.query += " " + self.limitQuery

        print("Query: ", self.query)
        self.reset()

        match fetchType:
            case FetchType.NONE:
                return Database.getInstance().execute(self.query)
            case FetchType.ALL:
                return Database.getInstance().fetch(self.query)
            case FetchType.ONE:
                return Database.getInstance().fetchOne(self.query)
            case FetchType.MANY:
                return Database.getInstance().fetchMany(self.query, fetchSize)

    def reset(self):
        self.whereQuery = ""
        self.orderQuery = ""
        self.limitQuery = ""


class Database:
    __instance = None

    @staticmethod
    def getInstance() -> "Database":
        if Database.__instance == None:
            Database.__instance = Database()

        return Database.__instance

    def __init__(self) -> None:
        if Database.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self

        self.connection = sqlite3.connect(Config.DATABASE_PATH)
        self.cursor = self.connection.cursor()

    def execute(self, *queris: str) -> None:
        for query in queris:
            self.cursor.execute(query)

        self.connection.commit()

    def fetch(self, query: str) -> list[tuple]:
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetchOne(self, query: str) -> tuple:
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetchMany(self, query: str, size: int | None = None) -> list[tuple]:
        self.cursor.execute(query)
        return self.cursor.fetchmany(size)

    def close(self):
        self.connection.close()
