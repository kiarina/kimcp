import rich_click as click

from kimcp.command._decorators.mcp_gateway_client_options import (
    mcp_gateway_client_options,
)
from kimcp.command.connect._operations.register_mcp_server import (
    register_mcp_server,
)
from kimcp.command.connect._utils.load_env_vars import load_env_vars
from kimcp.command.connect._utils.parse_key_value_pairs import parse_key_value_pairs
from kimcp.core.app import AgentID


@click.command("stdio")
@mcp_gateway_client_options
@click.option("--server-name", required=True, type=str)
@click.option("--command", required=True, type=str)
@click.option("--arg", "args", multiple=True, type=str)
@click.option("--env", "envs", multiple=True, type=str)
@click.option("--env-from", "env_froms", multiple=True, type=str)
@click.option("--cwd", type=str)
@click.option("--encoding", type=str)
def connect_stdio(
    gateway_base_url: str,
    agent_id: AgentID,
    server_name: str,
    command: str,
    args: tuple[str, ...],
    envs: tuple[str, ...],
    env_froms: tuple[str, ...],
    cwd: str | None,
    encoding: str | None,
) -> None:
    """Create a stdio MCP connection."""
    register_mcp_server(
        gateway_base_url=gateway_base_url,
        agent_id=agent_id,
        payload={
            "server_name": server_name,
            "connection": {
                "transport": "stdio",
                "command": command,
                "args": list(args),
                "env": {
                    **parse_key_value_pairs(envs, option_name="--env"),
                    **load_env_vars(env_froms),
                },
                **({"cwd": cwd} if cwd is not None else {}),
                **({"encoding": encoding} if encoding is not None else {}),
            },
        },
    )
