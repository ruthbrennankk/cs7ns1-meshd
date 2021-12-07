import socket
from threading import Event

ACCEPT_TIMEOUT = 1

# Primary Class Author : Chao, Secondary: Ruth, Anton
class ProtocolServer:
    def __init__(self, port, accept_timeout: int = ACCEPT_TIMEOUT):
        self.accept_timeout = accept_timeout
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if port:
            self.server.bind(('', port))
        else:
            self.port = self.next_free_port(self.server, port)
            # self.server.bind(('', port))
        self.server.listen(1)

        _, self.port = self.server.getsockname()

    def next_free_port(self, sock, port: int, min_port=33000, max_port=34000):
        if port and port < max_port and port > min_port :
            return port
        p = min_port
        while p <= max_port:
            try:
                sock.bind(('', p))
                return p
            except OSError:
                p += 1
        raise IOError('no free ports')

    def accept_until_stop(self, stop_event: Event):
        self.server.setblocking(False)
        self.server.settimeout(self.accept_timeout)

        while not stop_event.is_set():
            try:
                sock, _ = self.server.accept()
                yield sock
            except socket.timeout:
                pass

    def close(self):
        self.server.close()
