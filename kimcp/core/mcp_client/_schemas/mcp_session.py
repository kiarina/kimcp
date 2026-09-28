import asyncio
import logging
from contextlib import AsyncExitStack

from mcp import Client

from kimcp.core.mcp_server import MCPServer

logger = logging.getLogger(__name__)


class MCPSession:
    """One live connection to an MCP server, owned by a dedicated task.

    `mcp.Client` must be exited by the task that entered it, while the gateway
    connects, calls tools and disconnects from separate request tasks. The owner
    task enters the client, waits until `close()` asks it to stop, and exits it.
    """

    def __init__(self, server: MCPServer) -> None:
        self.server = server
        self._client: Client | None = None
        self._ready = asyncio.Event()
        self._stop = asyncio.Event()
        self._task: asyncio.Task[None] | None = None
        self._error: BaseException | None = None

    @classmethod
    async def open(cls, server: MCPServer) -> "MCPSession":
        session = cls(server)
        session._task = asyncio.create_task(
            session._run(), name=f"kimcp-mcp-session:{server.server_name}"
        )
        await session._ready.wait()

        if session._error is not None:
            await asyncio.gather(session._task, return_exceptions=True)
            raise session._error

        return session

    @property
    def client(self) -> Client:
        if self._client is None or self._task is None or self._task.done():
            raise RuntimeError(f"MCP session is closed: {self.server.server_name}")

        return self._client

    async def close(self) -> None:
        if self._task is None:
            return

        self._stop.set()
        await self._task

    async def _run(self) -> None:
        connection = self.server.connection

        try:
            async with AsyncExitStack() as stack:
                target = await connection.enter_client_target(stack)
                self._client = await stack.enter_async_context(
                    Client(target, **connection.session_kwargs)
                )
                self._ready.set()
                await self._stop.wait()
        except Exception as exc:
            if not self._ready.is_set():
                self._error = exc
            else:
                logger.warning(
                    "MCP session ended with an error: %s: %s", self.server.server_name, exc
                )
        finally:
            self._client = None
            self._ready.set()
