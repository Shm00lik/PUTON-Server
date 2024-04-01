from config import Config
import sqlite3
import threading


class Database(sqlite3.Connection):
    __instance = None

    @classmethod
    def getInstance(cls) -> "Database":
        if cls.__instance == None:
            cls.__instance = cls(Config.DATABASE_PATH)

        return cls.__instance

    def __init__(self, databasePath: str, *args, **kwargs) -> None:
        if Database.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self

        super().__init__(
            database=databasePath, check_same_thread=False, *args, **kwargs
        )

        self.row_factory = sqlite3.Row
        self.isolation_level = None

        self.lock = threading.Lock()

    def execute(self, *args, **kwargs) -> "Cursor":
        with self.lock:
            return Cursor(super().execute(*args, **kwargs))

    def executemany(self, *args, **kwargs) -> "Cursor":
        with self.lock:
            return Cursor(super().executemany(*args, **kwargs))


class Cursor:
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self.cursor = cursor

    def fetchOne(self) -> sqlite3.Row | None:
        return self.cursor.fetchone()

    def fetchMany(self, size: int | None = 1) -> list[sqlite3.Row]:
        return self.cursor.fetchmany(size)

    def fetchAll(self) -> list[sqlite3.Row]:
        return self.cursor.fetchall()
