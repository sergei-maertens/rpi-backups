from django.contrib import admin
from django.template.defaultfilters import filesizeformat

from .models import BackupRun


@admin.register(BackupRun)
class BackupRunAdmin(admin.ModelAdmin):
    list_display = ("state", "started", "ended", "size", "num_files")
    list_filter = ("state", "started", "ended")
    date_hierarchy = "started"
    ordering = ("-started",)

    def size(self, obj) -> str:
        return filesizeformat(obj.size_transferred)
