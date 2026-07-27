from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any, cast

import rich_click as click

DEFAULT_AGENT_ID = "default"
DEFAULT_GATEWAY_BASE_URL = "http://localhost:8000"


def mcp_gateway_client_options[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    decorated: Callable[..., Any] = click.option(
        "--gateway-base-url",
        default=DEFAULT_GATEWAY_BASE_URL,
        show_default=True,
        type=str,
    )(
        click.option(
            "--agent-id",
            default=DEFAULT_AGENT_ID,
            show_default=True,
            type=str,
        )(wrapper)
    )
    return cast(Callable[P, R], decorated)
