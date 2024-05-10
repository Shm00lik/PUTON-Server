class Config:
    """
    Configuration parameters for the application.
    """

    HOST: str = "0.0.0.0"
    """
    The host address for the server to bind to.
    """

    PORT: int = 3339
    """
    The port number for the server to listen on.
    """

    DATABASE_PATH: str = "./database/database.sqlite"
    """
    The path to the SQLite database file.
    """

    PRODUCT_IMAGES_PATH: str = "./database/images"
    """
    The directory path where product images are stored.
    """

    PRODUCT_IMAGES_SUBFIX: str = "png"
    """
    The file extension for product images.
    """

    SOCKET_TIMEOUT: int = 1
    """
    The timeout duration for socket operations, in seconds.
    """
