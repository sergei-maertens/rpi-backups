import socket

BUFFER_SIZE = 4


def read_message(sock: socket.socket, on_message: callable, buff=BUFFER_SIZE) -> None:
    """
    Read one or more mesasges from a blocking socket.

    Nessages should be utf-8 encoded.
    """
    content = b""
    msg_len = 0
    msg = b""

    while True:
        data: bytes = sock.recv(buff)
        if not data:  # stream ends -> connection closed
            break

        content += data

        # determine message length
        if not msg_len and b";" in content and content.startswith(b"len:"):
            idx = content.index(b";")
            msg_len = int(content[4:idx])

            msg_start = 4 + len(content[4:idx]) + 1
            content = content[msg_start:]

        if msg_len and len(content) >= msg_len:
            msg = content[:msg_len]

            on_message(str(msg, "utf-8"))

            # reset after message read and handling
            if len(content) > msg_len:
                content = content[msg_len:]
            else:
                content = b""
            msg_len = 0
            msg = b""

    return
