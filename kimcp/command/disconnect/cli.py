import httpx
import rich_click as click

from kimcp.command._decorators.mcp_gateway_client_options import (
    mcp_gateway_client_options,
)
from kimcp.command._utils.echo_json import echo_json
from kimcp.command._utils.handle_response import handle_response
from kimcp.core.app import AgentID


@click.command("disconnect")
@mcp_gateway_client_options
@click.option("--server-name", required=True, type=str)
def disconnect(
    gateway_base_url: str,
    agent_id: AgentID,
    server_name: str,
) -> None:
    """Disconnect an MCP server."""
    with httpx.Client(
        base_url=gateway_base_url,
        timeout=30.0,
    ) as client:
        response = client.delete(f"/agents/{agent_id}/mcp-servers/{server_name}")

    echo_json(handle_response(response))
