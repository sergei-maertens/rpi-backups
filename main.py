#!/usr/bin/env python

from signal import pause

from gpiozero import LED

SERVER_ONLINE = LED("GPIO2", initial_value=False)
LAST_BACKUP_OK = LED("GPIO3", initial_value=False)
BACKUP_IN_PROGRESS = LED("GPIO4", initial_value=False)
LAST_BACKUP_FAILED = LED("GPIO17", initial_value=False)


def main():
    SERVER_ONLINE.on()

    pause()


if __name__ == "__main__":
    main()
