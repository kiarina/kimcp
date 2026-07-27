from pathlib import Path

from kimcp.core.app import get_user_data_dir

from .._schemas.mcp_gateway_process_info import MCPGatewayProcessInfo


def path(*, host: str, port: int) -> Path:
    safe_host = host.replace("/", "_").replace(":", "_")
    return Path(get_user_data_dir()) / "servers" / f"{safe_host}_{port}.json"


def write(process_info: MCPGatewayProcessInfo) -> MCPGatewayProcessInfo:
    file_path = path(host=process_info.host, port=process_info.port)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(process_info.model_dump_json(indent=2))

    return process_info


def read(*, host: str, port: int) -> MCPGatewayProcessInfo | None:
    file_path = path(host=host, port=port)
    if not file_path.exists():
        return None

    return MCPGatewayProcessInfo.model_validate_json(file_path.read_text())


def delete(*, host: str, port: int) -> None:
    file_path = path(host=host, port=port)
    if file_path.exists():
        file_path.unlink()


def clear() -> None:
    directory = Path(get_user_data_dir()) / "servers"
    if not directory.exists():
        return

    for file_path in directory.glob("*.json"):
        file_path.unlink()
