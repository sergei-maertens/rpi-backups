import time

from django.core.management import BaseCommand

from ._monitor import Monitor


class Command(BaseCommand):
    help = "Run a backup"

    def add_arguments(self, parser):
        parser.add_argument("--host", default="alarmpi.home")
        parser.add_argument("--port", default=5555, type=int)
        parser.add_argument("--sleep", default=10, type=int)

    def handle(self, **options):
        with Monitor(options["host"], options["port"]) as monitor:
            monitor.send_event("ping")
            self.stdout.write("Monitor online")

            monitor.send_event("backup:started")
            self.stdout.write("Backup reported as in progress")

            self.stdout.write("Running backup...")
            time.sleep(options["sleep"])

            monitor.send_event("backup:ended:success")
            self.stdout.write("Backup marked as success")
            # monitor.send_event("backup:ended:failure")
            # self.stdout.write("Backup marked as failure")
