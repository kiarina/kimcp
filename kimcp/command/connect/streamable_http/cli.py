from typing import Any

import rich_click as click

from kimcp.command._decorators.mcp_gateway_client_options import (
    mcp_gateway_client_options,
)
from kimcp.command.connect._operations.register_mcp_server import (
    register_mcp_server,
)
from kimcp.command.connect._utils.load_header_env_vars import load_header_env_vars
from kimcp.command.connect._utils.parse_key_value_pairs import parse_key_value_pairs
from kimcp.core.app import AgentID


@click.command("streamable-http")
@mcp_gateway_client_options
@click.option("--server-name", required=True, type=str)
@click.option("--url", required=True, type=str)
@click.option("--header", "headers", multiple=True, type=str)
@click.option("--header-from-env", "header_from_envs", multiple=True, type=str)
@click.option("--timeout", type=float)
@click.option("--sse-read-timeout", type=float)
@click.option("--terminate-on-close/--no-terminate-on-close", default=None)
def connect_streamable_http(
    gateway_base_url: str,
    agent_id: AgentID,
    server_name: str,
    url: str,
    headers: tuple[str, ...],
    header_from_envs: tuple[str, ...],
    timeout: float | None,
    sse_read_timeout: float | None,
    terminate_on_close: bool | None,
) -> None:
    """Create a streamable HTTP MCP connection."""
    connection: dict[str, Any] = {
        "transport": "streamable_http",
        "url": url,
        "headers": {
            **parse_key_value_pairs(headers, option_name="--header"),
            **load_header_env_vars(header_from_envs),
        },
    }

    if timeout is not None:
        connection["timeout"] = timeout
    if sse_read_timeout is not None:
        connection["sse_read_timeout"] = sse_read_timeout
    if terminate_on_close is not None:
        connection["terminate_on_close"] = terminate_on_close

    register_mcp_server(
        gateway_base_url=gateway_base_url,
        agent_id=agent_id,
        payload={
            "server_name": server_name,
            "connection": connection,
        },
    )
