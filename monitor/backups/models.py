from datetime import timedelta
from typing import Optional

from django.db import models
from django.template.defaultfilters import timesince
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BackupRunStates(models.TextChoices):
    running = "running", _("Running")
    finished = "finished", _("Finished")
    failed = "failed", _("Failed")


class BackupRun(models.Model):
    state = models.CharField(
        _("state"),
        max_length=50,
        choices=BackupRunStates.choices,
        default=BackupRunStates.running,
    )
    started = models.DateTimeField(_("started"), default=timezone.now)
    ended = models.DateTimeField(
        _("started"),
        blank=True,
        null=True,
    )

    size_transferred = models.IntegerField(
        _("size transferred, in bytes"), blank=True, null=True
    )
    num_files = models.IntegerField(_("number of files"), blank=True, null=True)

    def __str__(self) -> str:
        return timesince(self.started)

    @property
    def duration(self) -> Optional[timedelta]:
        if not self.ended:
            return None
        return self.ended - self.started
