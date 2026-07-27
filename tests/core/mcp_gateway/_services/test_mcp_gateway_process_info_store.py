from pathlib import Path

from kimcp.core.mcp_gateway import MCPGatewayProcessInfo, mcp_gateway_process_info_store


def test_write_read_delete_and_clear(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        mcp_gateway_process_info_store,
        "get_user_data_dir",
        lambda: str(tmp_path),
    )

    process_info = mcp_gateway_process_info_store.write(
        MCPGatewayProcessInfo(
            host="local/host:1",
            port=8000,
            pid=12345,
            create_time=123.456,
        )
    )

    expected_path = tmp_path / "servers" / "local_host_1_8000.json"
    assert process_info.pid == 12345
    assert process_info.create_time == 123.456
    assert expected_path.exists()
    assert mcp_gateway_process_info_store.read(host="local/host:1", port=8000) == process_info

    mcp_gateway_process_info_store.write(
        MCPGatewayProcessInfo(
            host="other",
            port=9000,
            pid=54321,
            create_time=654.321,
        )
    )
    assert (tmp_path / "servers" / "other_9000.json").exists()

    mcp_gateway_process_info_store.delete(host="local/host:1", port=8000)
    assert not expected_path.exists()

    mcp_gateway_process_info_store.clear()
    assert list((tmp_path / "servers").glob("*.json")) == []
