import socketserver

from gpiozero import LED

from .events import event
from .protocol import read_message

# LEDs

BACKUP_IN_PROGRESS = LED("GPIO4", initial_value=False)
LAST_BACKUP_FAILED = LED("GPIO17", initial_value=False)
SERVER_ONLINE = LED("GPIO27", initial_value=False)
LAST_BACKUP_OK = LED("GPIO22", initial_value=False)


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
    def handle(self):
        print(f"Handling connection from {self.client_address}")
        read_message(self.request, event.dispatch)
        print(f"Closing connection with {self.client_address}")


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


def main(host, port):
    with Server((host, port), LEDStateHandler) as server:
        SERVER_ONLINE.on()
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
