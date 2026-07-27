import socket
import time


def wait_for_socket(host: str, port: int, *, timeout: float = 10.0) -> None:
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return
        except OSError:
            time.sleep(0.1)

    raise RuntimeError(f"Socket did not become ready: {host}:{port}")
