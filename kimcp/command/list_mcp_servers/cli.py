import httpx
import rich_click as click

from kimcp.command._decorators.mcp_gateway_client_options import (
    mcp_gateway_client_options,
)
from kimcp.command._utils.echo_json import echo_json
from kimcp.command._utils.handle_response import handle_response
from kimcp.core.app import AgentID


@click.command("list-mcp-servers")
@mcp_gateway_client_options
def list_mcp_servers(gateway_base_url: str, agent_id: AgentID) -> None:
    """List MCP servers for an agent."""
    with httpx.Client(
        base_url=gateway_base_url,
        timeout=30.0,
    ) as client:
        response = client.get(f"/agents/{agent_id}/mcp-servers")

    echo_json(handle_response(response))
