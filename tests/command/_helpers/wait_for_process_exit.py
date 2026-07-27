import subprocess
import time


def wait_for_process_exit(process: subprocess.Popen[str], *, timeout: float = 10.0) -> None:
    deadline = time.time() + timeout

    while time.time() < deadline:
        if process.poll() is not None:
            return
        time.sleep(0.1)

    raise RuntimeError("Gateway process did not exit.")
