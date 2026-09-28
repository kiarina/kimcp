# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.2.0] - 2026-09-29

### Changed

- **Breaking:** kimcp now runs on the MCP Python SDK 2.x (`mcp>=2.2.0,<3`) directly and no longer depends on LangChain (`langchain-core`, `langchain-mcp-adapters`). It negotiates the 2026-07-28 protocol with servers that support it and falls back to the initialize handshake for MCP 1.x servers.
- **Breaking:** `run-tool` returns the MCP `CallToolResult` as-is (`content`, `structuredContent`, `isError`, `_meta`) instead of LangChain content blocks. Tool failures are reported with `"isError": true`.
- **Breaking:** `list-tools` returns each tool's MCP definition (`name`, `description`, `inputSchema`, `outputSchema`, `annotations`, ...) plus `server_name`, instead of `args_schema`. The input schema is no longer rewritten.
- `session_kwargs` on a connection are passed to `mcp.Client` (for example `read_timeout_seconds`).
- A failed `connect` returns HTTP 502 and leaves the server unregistered.

### Fixed

- `disconnect` no longer fails with "Attempted to exit cancel scope in a different task". Each session is owned by one task, so connecting, running tools and disconnecting from separate requests works, and a stdio server process stops on disconnect.
- Stopping the gateway closes every open session.

## [0.1.0] - 2026-07-10

### Added

- Initial release of kimcp, an MCP gateway with a CLI backed by a local FastAPI gateway.
- `kimcp serve` / `kimcp shutdown` to start and stop the gateway.
- `kimcp connect` to register stdio MCP servers and `kimcp disconnect` to remove them.
- `kimcp list-mcp-servers` and `kimcp list-tools` to inspect registered servers and their tools.
- `kimcp run-tool` to invoke a tool on a registered server.
