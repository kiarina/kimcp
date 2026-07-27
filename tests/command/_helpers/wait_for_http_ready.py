import time

import httpx


def wait_for_http_ready(base_url: str, *, timeout: float = 10.0) -> None:
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            response = httpx.get(f"{base_url}/openapi.json", timeout=0.5)
            if response.status_code == 200:
                return
        except Exception:
            pass

        time.sleep(0.1)

    raise RuntimeError(f"Gateway did not become ready: {base_url}")
