from server import Server


def main() -> None:
    server = Server()
    server.start()

    running = True

    while running:
        server.accept()
        running = server.shouldRun()


if __name__ == "__main__":
    main()