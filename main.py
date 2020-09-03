#!/usr/bin/env python

import time
from signal import pause

from gpiozero import LED

SERVER_ONLINE = LED("GPIO2")
LAST_BACKUP_OK = LED("GPIO3")
BACKUP_IN_PROGRESS = LED("GPIO4")
LAST_BACKUP_FAILED = LED("GPIO17")


def init():
    # disable all LEDs
    SERVER_ONLINE.off()
    LAST_BACKUP_OK.off()
    BACKUP_IN_PROGRESS.off()
    LAST_BACKUP_FAILED.off()


def main():
    init()
    time.sleep(5)

    SERVER_ONLINE.on()

    pause()


if __name__ == "__main__":
    main()
