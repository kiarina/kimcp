# kimcp

`kimcp` is a small MCP gateway for registering MCP servers, listing tools, running tools, and disconnecting servers through a CLI backed by a local FastAPI gateway.

## Installation

```sh
pip install kimcp
```

## Usage

Start the gateway:

```sh
kimcp serve
```

Connect a stdio MCP server:

```sh
kimcp connect stdio --server-name math --command python --arg ./server.py
```

List registered MCP servers:

```sh
kimcp list-mcp-servers
```

List tools for a server:

```sh
kimcp list-tools --server-name math
```

Run a tool:

```sh
kimcp run-tool --server-name math --tool-name add --tool-args '{"a": 1, "b": 2}'
```

Disconnect a server:

```sh
kimcp disconnect --server-name math
```

Stop the gateway:

```sh
kimcp shutdown
```

## Development

```sh
mise run setup
mise run ci
```
