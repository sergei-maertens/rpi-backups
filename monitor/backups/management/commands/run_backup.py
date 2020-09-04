import socket
import time

from django.core.management import BaseCommand

BUFFER_SIZE = 64


class Command(BaseCommand):
    help = "Run a backup"

    def add_arguments(self, parser):
        parser.add_argument("--host", default="alarmpi.home")
        parser.add_argument("--port", default=5555, type=int)
        parser.add_argument("--sleep", default=10, type=int)

    def handle(self, **options):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # sock.settimeout(2)
            # Connect to server and send data
            sock.connect((options["host"], options["port"]))

            try:
                # ping server
                sock.sendall(b"ping")
                received = sock.recv(BUFFER_SIZE)
                if received == b"ok":
                    self.stdout.write("Server up")

                sock.sendall(b"backup:started")
                received = sock.recv(BUFFER_SIZE)
                if received == b"ok":
                    self.stdout.write("Backup start notified")

                time.sleep(options["sleep"])

                # sock.sendall(b"backup:ended:success")
                sock.sendall(b"backup:ended:failure")
                if received == b"ok":
                    self.stdout.write("Backup state marked")

            except socket.timeout:
                self.stderr.write("Connection timed out")
