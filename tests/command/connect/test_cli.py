from click.testing import CliRunner

from kimcp.command.connect import connect


def test_connect_lists_subcommands() -> None:
    result = CliRunner().invoke(connect, ["--help"])

    assert result.exit_code == 0
    assert "stdio" in result.output
    assert "sse" in result.output
    assert "streamable-http" in result.output
