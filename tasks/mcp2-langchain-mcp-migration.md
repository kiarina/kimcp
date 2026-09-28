# Move from langchain-mcp-adapters to `langchain.mcp` to reach MCP 2

Status: investigated (2026-09-29); waiting for a go / no-go decision. See Findings.

## Background

kimcp cannot move to the MCP Python SDK 2.x while it depends on
`langchain-mcp-adapters`.

- `langchain-mcp-adapters` 0.3.2 (latest on PyPI, 2026-08-06) requires
  `mcp>=1.24.0,<2.0.0`. Resolving it together with `mcp>=2` fails. Removing
  the cap falls back to 0.3.1, which fails at import with
  `ImportError: cannot import name 'RequestContext' from 'mcp.shared.context'`.
- Upstream issue langchain-ai/langchain-mcp-adapters#578 ("Support for
  upcoming Python MCP SDK v2.0.0") was closed as completed on 2026-09-16
  without a linked fix, and no release lifts the cap.
- Since 2026-09-11 the upstream README says the repository is no longer
  actively maintained. MCP support moved into LangChain as the `langchain.mcp`
  namespace, installed with `langchain[mcp]`.
- `langchain` 1.4.2 declares `fastmcp>=4.0.1,<5.0.0` for the `mcp` extra.
  `fastmcp` 4.0.10 goes through `fastmcp-slim`, which requires
  `mcp>=2.0.0,<3.0.0`. The new path therefore puts kimcp on MCP 2.
- As of 2026-09-28 the lockfile resolves `mcp` 1.30.0, the newest 1.x.

## Findings (2026-09-29)

Measured in
[labs/2026/09/29/kimcp-mcp2-migration](https://github.com/kiarina/labs/tree/main/2026/09/29/kimcp-mcp2-migration):
old client (kimcp's current flow) and new client (`fastmcp.Client` + `as_langchain_tool`) against
an MCP 1 and an MCP 2 server over stdio, SSE and streamable HTTP.

Unchanged:

- All three transports work on the new stack, SSE included (SSE stays on the 2025-11-25 handshake).
- The new client still reaches MCP 1 servers; it falls back to 2025-11-25 automatically.
- `tool.ainvoke` returns the same LangChain content blocks, and `isError=True` still comes back as
  error text rather than an exception, so `run-tool` output keeps its shape.

Needs work in kimcp:

- `StdioTransport` defaults to `keep_alive=True`: leaving the client context leaves the server
  subprocess running. `disconnect` must also `await client.transport.close()`.
- Connection fields with no fastmcp equivalent: SSE `timeout`, streamable HTTP `timeout`,
  `sse_read_timeout`, `terminate_on_close`, stdio `encoding`, and `session_kwargs`. Request timeout
  moves to `Client(timeout=...)`, auth to `Client(auth=...)`. Dropping fields is a breaking change
  for the API and CLI.
- On the 2026-07-28 protocol over streamable HTTP, one request timeout leaves the client
  disconnected and closing it raises `httpx2.ReadTimeout` (3 of 3 runs). `mode="legacy"` avoids it.
  Either pin `legacy`, or reconnect after a timeout.
- Use `fastmcp.Client` directly, not `MCPAdapter`: its interrupt-based elicitation raises
  `KeyError: '__pregel_scratchpad'` outside a LangGraph run.
- `langchain.mcp` is beta, and the install grows from 52 to 91 packages. Alternatives:
  `fastmcp-slim[client]` alone is 51 packages, `mcp` 2.2.0 alone 28, but dropping LangChain changes
  the `run-tool` output format.

Also found (independent of the migration): today's kimcp, talking to an MCP 2 stdio server, fails
to disconnect after a request timeout (`anyio.BrokenResourceError`), which `disconnect` logs as a
warning.

Decisions for the owner: whether to migrate now, which connection fields may be dropped, whether to
keep LangChain (`langchain[mcp]`) or depend on `fastmcp-slim` / `mcp` directly, and whether to
publish a new version.

## What to do

1. Read the upstream migration guide
   (https://docs.langchain.com/oss/python/migrate/langchain-mcp-adapters) and
   the `langchain.mcp` source, and map each import kimcp uses to its
   replacement.
2. Replace the dependency in `pyproject.toml`: drop `langchain-mcp-adapters`,
   add `langchain[mcp]`, raise `mcp` to `>=2`, and refresh `uv.lock`.
3. Port the call sites listed below. Keep kimcp's own connection models and
   config format unchanged unless the new API makes that impossible. If it
   does, record the breaking change in `CHANGELOG.md`.
4. Port the MCP 1 test server (`tests/data/mcp_server_impl/math.py` uses
   `mcp.server.fastmcp.FastMCP`) to the MCP 2 / fastmcp API.
5. Run `mise run ci` on Python 3.12 and 3.13, then smoke-test `connect`,
   tool listing, a tool call and `disconnect` against real stdio,
   SSE and streamable HTTP servers.

## Scope of impact

- `kimcp/core/mcp_client/_models/mcp_client.py`: `MultiServerMCPClient`,
  `load_mcp_tools`
- `kimcp/core/mcp_server/_models/base_connection.py`: `Connection`,
  `SSEConnection`, `StdioConnection`, `StreamableHttpConnection`
- `kimcp/core/mcp_server/_types/lc_connection.py`: `Connection`
- Tests under `tests/core/mcp_client/`, `tests/core/mcp_server/`,
  `tests/api/connect/`, `tests/api/disconnect/` and `tests/data/mcp_server_impl/`
- Whether SSE is still supported under MCP 2 needs checking. Dropping a
  transport is a user-facing change.
- Publishing a new version to PyPI is a separate decision. See
  `docs/how_to_release.md`.

## Done when

kimcp no longer depends on `langchain-mcp-adapters`, `uv.lock` resolves
`mcp` 2.x, `mise run ci` and the CI workflow pass, and the real-server smoke
test covers every supported transport.
