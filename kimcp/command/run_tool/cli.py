import json
from typing import Any

import httpx
import rich_click as click

from kimcp.command._decorators.mcp_gateway_client_options import (
    mcp_gateway_client_options,
)
from kimcp.command._utils.echo_json import echo_json
from kimcp.command._utils.handle_response import handle_response
from kimcp.core.app import AgentID


@click.command("run-tool")
@mcp_gateway_client_options
@click.option("--server-name", required=True, type=str)
@click.option("--tool-name", required=True, type=str)
@click.option("--tool-args", default="{}", show_default=True, type=str)
def run_tool(
    gateway_base_url: str,
    agent_id: AgentID,
    server_name: str,
    tool_name: str,
    tool_args: str,
) -> None:
    """Run a tool through the MCP gateway."""
    try:
        parsed_args: Any = json.loads(tool_args)
    except json.JSONDecodeError as exc:
        raise click.ClickException(f"Invalid JSON for --tool-args: {exc}") from exc

    if not isinstance(parsed_args, dict):
        raise click.ClickException("--tool-args must decode to a JSON object.")

    with httpx.Client(
        base_url=gateway_base_url,
        timeout=120.0,
    ) as client:
        response = client.post(
            f"/agents/{agent_id}/mcp-servers/{server_name}/tools/{tool_name}/run",
            json={"args": parsed_args},
        )

    echo_json(handle_response(response))
