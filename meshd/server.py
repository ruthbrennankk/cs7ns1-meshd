import socket


class Protocol:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 0))
        self.server.listen()

        _, self.port = self.server.getsockname()

    def close(self):
        self.server.close()
