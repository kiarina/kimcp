import rich_click as click

from .sse import connect_sse
from .stdio import connect_stdio
from .streamable_http import connect_streamable_http


@click.group("connect")
def connect() -> None:
    """Create a new MCP server connection."""


connect.add_command(connect_stdio)
connect.add_command(connect_sse)
connect.add_command(connect_streamable_http)
