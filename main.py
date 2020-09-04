#!/usr/bin/env python

import socket
import socketserver
import time

from gpiozero import LED

# server config
HOST = "0.0.0.0"
PORT = 5555
BUFFER_SIZE = 64
TIMEOUT = 5.0

# LEDs

SERVER_ONLINE = LED("GPIO2", initial_value=False)
LAST_BACKUP_OK = LED("GPIO3", initial_value=False)
BACKUP_IN_PROGRESS = LED("GPIO4", initial_value=False)
LAST_BACKUP_FAILED = LED("GPIO17", initial_value=False)


class event:
    _registry = {}

    def __init__(self, label: str):
        self.label = label

    def __call__(self, func: callable):
        self.__class__._registry[self.label] = func
        return func

    @classmethod
    def dispatch(cls, label: str):
        callback = cls._registry.get(label)
        # exact match
        if callback:
            return callback()

        # prefixed match?
        for _label, callback in cls._registry.items():
            if not label.startswith(_label):
                continue

            args = label[len(_label) :].split(":")
            return callback(*args)

        return None


@event("ping")
def pong() -> str:
    return "ok"


@event("backup:started")
def start_backup() -> str:
    LAST_BACKUP_OK.off()
    LAST_BACKUP_FAILED.off()
    BACKUP_IN_PROGRESS.blink()
    return "ok"


@event("backup:ended:")
def finish_backup(state: str) -> str:
    BACKUP_IN_PROGRESS.off()

    if state == "success":
        LAST_BACKUP_OK.on()
    elif state == "failure":
        LAST_BACKUP_FAILED.on()
    else:
        return "err:unknown state"
    return "ok"


class LEDStateHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.request.settimeout(TIMEOUT)

    def handle(self):
        while True:
            try:
                data: bytes = self.request.recv(BUFFER_SIZE).strip()
            except (socket.timeout, ConnectionResetError):
                print("Connection closed, exiting.")
                return

            if not data:
                time.sleep(0.5)
                continue

            resp = event.dispatch(str(data, "utf-8"))
            if resp:
                self.request.sendall(bytes(resp, "utf-8"))


class Server(socketserver.TCPServer):
    allow_reuse_address = True


def main():
    with Server((HOST, PORT), LEDStateHandler) as server:
        SERVER_ONLINE.on()
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()


if __name__ == "__main__":
    main()
