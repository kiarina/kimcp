import psutil
import rich_click as click

from kimcp.command._decorators.mcp_gateway_server_options import (
    mcp_gateway_server_options,
)
from kimcp.core.mcp_gateway import mcp_gateway_process_info_store


@click.command("shutdown")
@mcp_gateway_server_options
def shutdown(host: str, port: int) -> None:
    """Shutdown the MCP Gateway."""
    process_info = mcp_gateway_process_info_store.read(host=host, port=port)
    if process_info is None:
        raise click.ClickException(f"No MCP Gateway process info found for {host}:{port}.")

    stopped = _stop_process(process_info.pid, process_info.create_time)
    mcp_gateway_process_info_store.delete(host=host, port=port)

    if not stopped:
        raise click.ClickException(f"MCP Gateway process was not running for {host}:{port}.")

    click.echo(f"Stopped MCP Gateway at {host}:{port} (pid={process_info.pid}).")


def _stop_process(pid: int, create_time: float, *, timeout: float = 5.0) -> bool:
    try:
        process = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return False

    try:
        if abs(process.create_time() - create_time) > 1e-6:
            return False
    except psutil.NoSuchProcess:
        return False

    process.terminate()

    try:
        process.wait(timeout=timeout)
    except psutil.TimeoutExpired:
        process.kill()
        process.wait(timeout=timeout)

    return True
