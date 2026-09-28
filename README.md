# kimcp

`kimcp` is a small MCP gateway for registering MCP servers, listing tools, running tools, and disconnecting servers through a CLI backed by a local FastAPI gateway.

It is built on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) 2.x and talks to servers over stdio, SSE and streamable HTTP. It negotiates the newest protocol a server supports, so servers built on MCP SDK 1.x keep working.

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

Connect an SSE or streamable HTTP MCP server:

```sh
kimcp connect sse --server-name docs --url http://localhost:8001/sse
kimcp connect streamable-http --server-name search --url http://localhost:8002/mcp --header "Authorization=Bearer $TOKEN"
```

List registered MCP servers:

```sh
kimcp list-mcp-servers
```

List tools for a server:

```sh
kimcp list-tools --server-name math
```

Each tool is listed with its MCP definition (`name`, `description`, `inputSchema`, and `outputSchema` or `annotations` when the server provides them), plus the `server_name` it came from.

Run a tool:

```sh
kimcp run-tool --server-name math --tool-name add --tool-args '{"a": 1, "b": 2}'
```

`result` is the MCP `CallToolResult` as the server returned it:

```json
{
  "agent_id": "default",
  "server_name": "math",
  "tool_name": "add",
  "result": {
    "content": [{"type": "text", "text": "3"}],
    "structuredContent": {"result": 3},
    "isError": false
  }
}
```

A tool that fails still returns successfully, with `"isError": true` and the server's message in `content`.

Disconnect a server:

```sh
kimcp disconnect --server-name math
```

Disconnecting a stdio server stops its process. Stopping the gateway disconnects every server.

Stop the gateway:

```sh
kimcp shutdown
```

## Development

```sh
mise run setup
mise run ci
```

Open work lives in [`tasks/`](tasks/), one file per task with its background, steps and
completion condition. Delete the file when the task is done.
