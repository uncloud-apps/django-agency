import socket

_HOSTNAME = socket.gethostname()


def server_hostname(request) -> dict[str, str]:
    return {"server_hostname": _HOSTNAME}
