import httpx

from kimcp.command._utils.echo_json import echo_json
from kimcp.command._utils.handle_response import handle_response
from kimcp.core.app import AgentID


def register_mcp_server(
    *,
    gateway_base_url: str,
    agent_id: AgentID,
    payload: dict,
) -> None:
    with httpx.Client(
        base_url=gateway_base_url,
        timeout=30.0,
    ) as client:
        response = client.post(
            f"/agents/{agent_id}/mcp-servers",
            json=payload,
        )

    echo_json(handle_response(response))
