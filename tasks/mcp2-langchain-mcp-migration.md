# Move kimcp to MCP 2, dropping LangChain

Status: implemented and tagged v0.2.0 (2026-09-29); only the PyPI upload is left. The owner approved
the plan, the output change and a PyPI release. The file name predates the LangChain-free plan.

## Progress (2026-09-29)

- `7542167` moves kimcp onto `mcp` 2.2 with no LangChain. CI passed on Python 3.12 and 3.13.
- Smoke test with a local gateway: stdio, SSE and streamable HTTP against an MCP 1 and an MCP 2
  server; connect, list-tools, run-tool (`isError` for failures), disconnect. A stdio server stops on
  disconnect and on `kimcp shutdown`. No cancel-scope error in the gateway log.
- `364a9dc` releases v0.2.0 and the tag is pushed. The Release workflow
  (run 36451557070) created the GitHub Release but the PyPI step failed with `invalid-publisher`:
  PyPI has no trusted publisher for kimcp. 0.1.0 was uploaded by hand (no provenance on PyPI).

Next: the owner adds the trusted publisher on PyPI (project `kimcp` → Publishing → GitHub: owner
`kiarina`, repository `kimcp`, workflow `release-pypi.yml`, environment `pypi`), then re-run the
failed job with `gh run rerun 36451557070 --failed`. `skip-existing` is on, so a re-run is safe.
Alternatively publish `dist/` by hand with `mise run publish`. When `pip install kimcp==0.2.0` works,
delete this file.

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
  namespace (`langchain[mcp]`, built on fastmcp 4, beta).
- kimcp only uses LangChain to hold sessions (`MultiServerMCPClient`), list
  tools (`load_mcp_tools`) and call them (`BaseTool.ainvoke`). It was carved
  out of a LangChain-centred toolkit; a gateway needs nothing beyond an MCP
  client.

## Findings (2026-09-29)

Measured in
[labs/2026/09/29/kimcp-mcp2-migration](https://github.com/kiarina/labs/tree/main/2026/09/29/kimcp-mcp2-migration):
today's client, `langchain.mcp`, `mcp` alone and `fastmcp-slim[client]` alone, against an MCP 1 and
an MCP 2 server over stdio, SSE and streamable HTTP (36 combinations), plus the published kimcp 0.1.0
driven end to end.

`mcp` 2.2.0 alone is the best fit:

- 28 packages (`langchain[mcp]` 91, `fastmcp-slim[client]` 51, today 52).
- All three transports work against MCP 1 and MCP 2 servers; SSE even reaches the 2026-07-28 protocol.
- Every connection field kimcp 0.1.0 exposes still maps: stdio `command`/`args`/`env`/`cwd`/`encoding`,
  SSE `url`/`headers`/`timeout`/`sse_read_timeout` (`sse_client`), streamable HTTP `headers`/`timeout`/
  `sse_read_timeout` (an `httpx2.AsyncClient` with `Timeout(timeout, read=sse_read_timeout)`) and
  `terminate_on_close`. `session_kwargs` maps to `mcp.Client` arguments (`read_timeout_seconds`,
  `elicitation_callback`, ...). fastmcp has no argument for several of these.
- After a request timeout the session keeps working and closes cleanly on every transport. fastmcp
  (and so `langchain.mcp`) loses the connection after a timeout on 2026-07-28 streamable HTTP.
- Leaving the client stops the stdio server process (fastmcp keeps it alive by default).
- One session serves concurrent calls (5 x 0.5 s tools finish in about 0.51 s).

Constraint: `mcp.Client` must be exited by the task that entered it. Connect, call and disconnect
from separate tasks (as FastAPI requests do) fails on disconnect with `RuntimeError: Attempted to
exit cancel scope in a different task than it was entered in`. A dedicated owner task per session
(enter, park until told to stop, exit) fixes it on every combination; see `OwnedSession` in the
lab's `sdk/client.py`.

kimcp 0.1.0 already has this bug: every `kimcp disconnect` answers `"disconnected": true` while the
gateway logs `Failed to close session ...: Attempted to exit cancel scope in a different task`. The
stdio server process was gone a second later anyway.

Output change: without LangChain, `run-tool` returns the MCP `CallToolResult` (`content`,
`structuredContent`, `isError`, `_meta`) instead of LangChain content blocks with `lc_...` ids, and
failures become visible as `isError: true`. `list-tools` can return the server's `inputSchema` as-is;
the `additionalProperties` rewrite exists for LLM providers, not for a gateway.

Elicitation: on 2026-07-28 a server that calls `ctx.elicit()` fails even when the client has a
handler; servers must return `InputRequiredResult`, which `mcp.Client` answers through
`elicitation_callback`. kimcp has no handler today; adding one is a separate feature.

## What to do (proposed)

1. Dependencies: drop `langchain-core` and `langchain-mcp-adapters`, require `mcp>=2.2,<3`, refresh
   `uv.lock`. Check whether kimcp's own `httpx` use can move to `httpx2` or stays.
2. Replace `MCPClient` with sessions built on `mcp.Client`, each owned by one task that enters the
   client, waits for a stop signal, and exits it. `disconnect` and gateway shutdown signal the owner
   and await it.
3. Map the existing connection models to `StdioServerParameters`, `sse_client(...)` and
   `streamable_http_client(..., http_client=httpx2.AsyncClient(...))`; keep the config format.
4. `list-tools`: return the MCP tool fields (`name`, `description`, `inputSchema`, and possibly
   `outputSchema` / `annotations`) and drop the schema rewrite. `run-tool`: return the
   `CallToolResult` as JSON. Record both as breaking changes in `CHANGELOG.md`.
5. Port the test server (`tests/data/mcp_server_impl/math.py`) from `mcp.server.fastmcp.FastMCP` to
   `mcp.server.mcpserver.MCPServer`, and add tests for connect / call / disconnect from separate
   requests and for the stdio process ending on disconnect.
6. Run `mise run ci` on Python 3.12 and 3.13, then smoke-test the CLI against real stdio, SSE and
   streamable HTTP servers, like the lab's `mise run kimcp-e2e`.

## Decisions for the owner

- Go ahead with the LangChain-free migration on `mcp` alone.
- Accept the `run-tool` / `list-tools` output change (0.1.0 is the only release and no active
  project depends on kimcp).
- Whether to publish a new version to PyPI (see `docs/how_to_release.md`).

## Done when

kimcp depends on `mcp` 2.x and no LangChain package, `mise run ci` and the CI workflow pass,
disconnect no longer logs the cancel-scope error, and the real-server smoke test covers every
supported transport.
