from typing import Any

import httpx
import rich_click as click


def handle_response(response: httpx.Response) -> Any:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text
        raise click.ClickException(
            f"Request failed with status {exc.response.status_code}: {detail}"
        ) from exc

    if not response.content:
        return {}

    return response.json()
