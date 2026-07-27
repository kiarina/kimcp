from pydantic import BaseModel

from .._types.lc_connections import LCConnections
from .._types.server_name import ServerName
from .sse_connection import SSEConnection
from .stdio_connection import StdioConnection
from .streamable_http_connection import StreamableHTTPConnection


class MCPServer(BaseModel):
    server_name: ServerName
    connection: SSEConnection | StdioConnection | StreamableHTTPConnection

    def to_lc_connections(self) -> LCConnections:
        return {self.server_name: self.connection.to_connection()}
