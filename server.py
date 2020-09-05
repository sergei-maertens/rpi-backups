#!/usr/bin/env python

from daemon import main

# server config
HOST = "0.0.0.0"
PORT = 5555


if __name__ == "__main__":
    main(HOST, PORT)
