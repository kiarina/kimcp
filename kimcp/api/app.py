from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from importlib.metadata import version

from fastapi import FastAPI

from kimcp.api.connect import router as connect_router
from kimcp.api.disconnect import router as disconnect_router
from kimcp.api.health import router as health_router
from kimcp.api.list_mcp_servers import router as list_mcp_servers_router
from kimcp.api.list_tools import router as list_tools_router
from kimcp.api.run_tool import router as run_tool_router
from kimcp.core.mcp_client import mcp_client_registry


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    # Stop stdio servers and close HTTP sessions when the gateway shuts down.
    await mcp_client_registry.close_all()


app = FastAPI(title="kimcp", version=version("kimcp"), lifespan=lifespan)
app.include_router(health_router)
app.include_router(connect_router)
app.include_router(disconnect_router)
app.include_router(list_mcp_servers_router)
app.include_router(list_tools_router)
app.include_router(run_tool_router)
