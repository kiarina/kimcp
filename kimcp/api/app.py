from fastapi import FastAPI

from kimcp.api.connect import router as connect_router
from kimcp.api.disconnect import router as disconnect_router
from kimcp.api.health import router as health_router
from kimcp.api.list_mcp_servers import router as list_mcp_servers_router
from kimcp.api.list_tools import router as list_tools_router
from kimcp.api.run_tool import router as run_tool_router

app = FastAPI(title="kimcp", version="0.1.0")
app.include_router(health_router)
app.include_router(connect_router)
app.include_router(disconnect_router)
app.include_router(list_mcp_servers_router)
app.include_router(list_tools_router)
app.include_router(run_tool_router)
