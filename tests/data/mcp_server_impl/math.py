import argparse
import os

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Math")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


@mcp.tool()
def pid() -> int:
    """Return the server process id"""
    return os.getpid()


@mcp.tool()
def fail() -> str:
    """Always fail"""
    raise ValueError("boom")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run("stdio")
    else:
        mcp.run(args.transport, host=args.host, port=args.port)
