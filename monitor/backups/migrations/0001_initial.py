# Generated by Django 3.1.1 on 2020-09-04 11:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BackupRun",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("running", "Running"),
                            ("finished", "Finished"),
                            ("failed", "Failed"),
                        ],
                        default="running",
                        max_length=50,
                        verbose_name="state",
                    ),
                ),
                (
                    "started",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="started"
                    ),
                ),
                (
                    "ended",
                    models.DateTimeField(blank=True, null=True, verbose_name="started"),
                ),
                (
                    "size_transferred",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="size transferred, in bytes"
                    ),
                ),
                (
                    "num_files",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="number of files"
                    ),
                ),
            ],
        ),
    ]
