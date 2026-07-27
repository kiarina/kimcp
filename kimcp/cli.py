import rich_click as click

from kimcp.command.connect import connect
from kimcp.command.disconnect import disconnect
from kimcp.command.list_mcp_servers import list_mcp_servers
from kimcp.command.list_tools import list_tools
from kimcp.command.run_tool import run_tool
from kimcp.command.serve import serve
from kimcp.command.shutdown import shutdown


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.rich_config({"theme": "dracula-modern"})
def kimcp() -> None:
    """CLI for the kimcp MCP gateway."""


kimcp.add_command(serve)
kimcp.add_command(connect)
kimcp.add_command(list_mcp_servers)
kimcp.add_command(list_tools)
kimcp.add_command(run_tool)
kimcp.add_command(disconnect)
kimcp.add_command(shutdown)


def main() -> None:
    kimcp()
