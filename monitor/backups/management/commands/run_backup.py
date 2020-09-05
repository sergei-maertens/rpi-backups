from django.core.management import BaseCommand
from django.utils import timezone

from ...backup import perform
from ...models import BackupRun, BackupRunStates
from ._monitor import Monitor


class Command(BaseCommand):
    help = "Run a backup"

    def add_arguments(self, parser):
        parser.add_argument("--host", default="alarmpi.home")
        parser.add_argument("--port", default=5555, type=int)

    def handle(self, **options):
        monitor = Monitor(options["host"], options["port"])

        with monitor:
            monitor.send_event("ping")
            self.stdout.write("Monitor online")

            monitor.send_event("backup:started")
            self.stdout.write("Backup reported as in progress")
            run = BackupRun.objects.create()

            try:
                success = perform()
            except Exception as exc:
                success = False
                self.stderr.write(f"Exception happened: {exc}")

            run.ended = timezone.now()
            run.state = BackupRunStates.finished if success else BackupRunStates.failed
            run.save(update_fields=["ended", "state"])

        with monitor:
            result = "success" if success else "failure"
            monitor.send_event(f"backup:ended:{result}")
            out = self.stdout if success else self.stderr
            out.write(f"Backup marked as {result}")
