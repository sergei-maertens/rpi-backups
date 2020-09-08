import re
from dataclasses import dataclass
from pathlib import Path

__all__ = ("BackupStats", "parse_rsync_log")


@dataclass
class BackupStats:
    bytes_received: int
    total_size: int
    num_files: int


def parse_rsync_log(file_path: Path) -> BackupStats:
    last_xfr = None

    with file_path.open("r") as logfile:
        for line in logfile:
            if line.startswith("sent ") and "received" in line:
                received = parse_received(line)
            elif line.startswith("total size is"):
                total_size = parse_total_size(line)
            elif "xfr#" in line:
                last_xfr = line

    num_files = 0
    if last_xfr:
        fileno_match = re.search(r"xfr#(?P<fileno>[0-9]+)", last_xfr)
        if fileno_match:
            num_files = fileno_match.group("fileno")

    return BackupStats(
        bytes_received=received,
        total_size=total_size,
        num_files=num_files,
    )


def parse_received(line: str) -> int:
    recv = line.split("bytes")[1].strip()  # recceived 123,456
    amount_bytes = recv.split()[1]  # 123,456
    return int(amount_bytes.replace(",", ""))


def parse_total_size(line: str) -> int:
    total_size_bytes = line[14:].split()[0]  # 123,456
    return int(total_size_bytes.replace(",", ""))
