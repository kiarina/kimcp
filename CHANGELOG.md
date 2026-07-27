# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.1.0] - 2026-07-10

### Added

- Initial release of kimcp, an MCP gateway with a CLI backed by a local FastAPI gateway.
- `kimcp serve` / `kimcp shutdown` to start and stop the gateway.
- `kimcp connect` to register stdio MCP servers and `kimcp disconnect` to remove them.
- `kimcp list-mcp-servers` and `kimcp list-tools` to inspect registered servers and their tools.
- `kimcp run-tool` to invoke a tool on a registered server.
