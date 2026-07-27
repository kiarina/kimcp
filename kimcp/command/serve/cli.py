import os
import sys

import psutil
import rich_click as click

from kimcp.command._decorators.mcp_gateway_server_options import (
    mcp_gateway_server_options,
)
from kimcp.core.mcp_gateway import MCPGatewayProcessInfo, mcp_gateway_process_info_store


@click.command("serve")
@mcp_gateway_server_options
@click.option("--reload/--no-reload", default=True, show_default=True)
def serve(host: str, port: int, reload: bool) -> None:
    """Start the MCP Gateway."""
    process = psutil.Process()

    mcp_gateway_process_info_store.write(
        MCPGatewayProcessInfo(
            host=host,
            port=port,
            pid=process.pid,
            create_time=process.create_time(),
        )
    )

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "kimcp.api.app:app",
        "--host",
        host,
        "--port",
        str(port),
    ]

    if reload:
        cmd.append("--reload")

    os.execvp(sys.executable, cmd)
