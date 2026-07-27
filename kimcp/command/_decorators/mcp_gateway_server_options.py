from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any, cast

import rich_click as click

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8000


def mcp_gateway_server_options[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    decorated: Callable[..., Any] = click.option(
        "--host",
        default=DEFAULT_HOST,
        show_default=True,
        type=str,
    )(
        click.option(
            "--port",
            default=DEFAULT_PORT,
            show_default=True,
            type=int,
        )(wrapper)
    )
    return cast(Callable[P, R], decorated)
