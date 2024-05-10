from config import Config
import sqlite3
import threading


class Database(sqlite3.Connection):
    """
    A database class representing a connection to an SQLite database.

    Inherits from sqlite3.Connection.
    """

    __instance = None  # Singleton instance holder

    @classmethod
    def get_instance(cls) -> "Database":
        """
        Returns a singleton instance of the Database class.

        Returns:
        - Database: The singleton instance of the Database class.
        """
        if cls.__instance == None:
            cls.__instance = cls(Config.DATABASE_PATH)

        return cls.__instance

    def __init__(self, database_path: str, *args, **kwargs) -> None:
        """
        Initializes the Database class.

        Args:
        - database_path (str): The path to the SQLite database file.
        """
        if Database.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self

        super().__init__(
            database=database_path, check_same_thread=False, *args, **kwargs
        )

        # Set row_factory and isolation_level for the database
        self.row_factory = sqlite3.Row
        self.isolation_level = None

        # Initialize a lock for thread safety
        self.lock = threading.Lock()

    def execute(self, *args, **kwargs) -> "Cursor":
        """
        Executes an SQL query.

        Args:
        - *args: Positional arguments for the execute method.
        - **kwargs: Keyword arguments for the execute method.

        Returns:
        - Cursor: The cursor object.
        """
        with self.lock:
            return Cursor(super().execute(*args, **kwargs))

    def executemany(self, *args, **kwargs) -> "Cursor":
        """
        Executes multiple SQL queries.

        Args:
        - *args: Positional arguments for the executemany method.
        - **kwargs: Keyword arguments for the executemany method.

        Returns:
        - Cursor: The cursor object.
        """
        with self.lock:
            return Cursor(super().executemany(*args, **kwargs))


class Cursor:
    """
    A cursor class representing a database cursor.

    Wraps around sqlite3.Cursor.
    """

    def __init__(self, cursor: sqlite3.Cursor) -> None:
        """
        Initializes the Cursor class.

        Args:
        - cursor (sqlite3.Cursor): The cursor object.
        """
        self.cursor = cursor

    def fetch_one(self) -> sqlite3.Row | None:
        """
        Fetches one row from the cursor.

        Returns:
        - sqlite3.Row | None: The fetched row, or None if no row is available.
        """
        return self.cursor.fetchone()

    def fetch_many(self, size: int | None = 1) -> list[sqlite3.Row]:
        """
        Fetches multiple rows from the cursor.

        Args:
        - size (int | None): The number of rows to fetch. If None, fetches all rows.

        Returns:
        - list[sqlite3.Row]: The fetched rows.
        """
        return self.cursor.fetchmany(size)

    def fetch_all(self) -> list[sqlite3.Row]:
        """
        Fetches all rows from the cursor.

        Returns:
        - list[sqlite3.Row]: The fetched rows.
        """
        return self.cursor.fetchall()
