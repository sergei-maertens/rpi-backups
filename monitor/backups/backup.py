import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from subprocess import call

from django.conf import settings

ISO_8601 = re.compile(r"^20[0-9]{2}-[0-9]{2}-[0-3][0-9]")


@dataclass
class BackupResult:
    directory: Path
    log_file: Path
    success: bool

    def __bool__(self):
        return self.success


def perform() -> BackupResult:
    """
    Perform an incremental backup.

    1. Determine the target directory of this backup
    2. Determine the most recent backup
    3. Build the rsync command
    4. Perform the backup using rsync
    5. Process the result
    """
    today = date.today().isoformat()
    target_dir = (settings.BACKUP_BASE_DIR / today).resolve()
    target_dir.mkdir(exist_ok=True)

    # find the previous backup
    prev_backup_dir = None
    existing_backups = sorted(settings.BACKUP_BASE_DIR.iterdir(), reverse=True)
    for path in existing_backups:
        if not path.is_dir():
            continue

        # we just created it
        if path == target_dir:
            continue

        # not a date-labelled directory
        if not ISO_8601.match(path.name):
            continue

        prev_backup_dir = path / settings.BACKUP_SOURCE_DIR.name

        # ensure that the directory actually exists
        if not prev_backup_dir.is_dir():
            continue
        else:
            break

    # build the rsync command
    # -r: recurse
    # -v: verbose
    # -L: copy symlinks as actual files
    # -t: preserve modification times
    # -S: sparse
    # -h: human readable numbers (disabled for post-processing)
    # -P: keep partially transferred and show progress
    excludes = [f"--exclude={exclude}" for exclude in settings.BACKUP_EXCLUDE]
    link_dest = [f"--link-dest={str(prev_backup_dir)}"] if prev_backup_dir else []
    source_dir = str(settings.BACKUP_SOURCE_DIR.resolve())
    dest_dir = target_dir / f"{settings.BACKUP_SOURCE_DIR.name}.tmp"

    log = target_dir / "rsync_inc.log"

    rsync_args = [
        "rsync",
        "-rvLtSP",
        *excludes,
        *link_dest,
        "-e ssh",
        f"{settings.BACKUP_SSH_USER}:{source_dir}/",
        str(dest_dir),
    ]

    with open(log, "w") as logfile:
        call(rsync_args, stdout=logfile)

    new_name = target_dir / settings.BACKUP_SOURCE_DIR.name
    dest_dir.rename(new_name)

    return check_integrity(target_dir, log)


def check_integrity(backup_dir: Path, log_file: Path) -> BackupResult:
    expected = backup_dir / settings.BACKUP_SOURCE_DIR.name
    tmp_dir = backup_dir / f"{settings.BACKUP_SOURCE_DIR.name}.tmp"
    success = expected in backup_dir.iterdir() and tmp_dir not in backup_dir.iterdir()
    return BackupResult(
        directory=backup_dir,
        log_file=log_file,
        success=success,
    )
