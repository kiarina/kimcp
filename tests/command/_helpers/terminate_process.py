import subprocess


def terminate_process(process: subprocess.Popen[str], *, timeout: float = 5.0) -> None:
    if process.poll() is not None:
        return

    process.terminate()

    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=timeout)
