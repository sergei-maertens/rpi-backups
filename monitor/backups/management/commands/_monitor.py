import socket


class Monitor:

    TIMEOUT = 2.0
    BUFFER_SIZE = 16

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._sock = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._sock is not None:
            self._sock.__exit__(*args)
            self._sock = None

    @property
    def server(self):
        if self._sock is None:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self._sock.settimeout(self.TIMEOUT)
            self._sock.connect((self.host, self.port))
        return self._sock

    def send(self, data: bytes, retries=3) -> bool:
        header = f"len:{len(data)};"
        content = bytes(header, "utf-8") + data
        self.server.sendall(content)

    def send_event(self, event: str) -> bool:
        encoded = bytes(event, "utf-8")
        return self.send(encoded)
