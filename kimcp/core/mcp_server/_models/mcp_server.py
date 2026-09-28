from pydantic import BaseModel

from .._types.server_name import ServerName
from .sse_connection import SSEConnection
from .stdio_connection import StdioConnection
from .streamable_http_connection import StreamableHTTPConnection


class MCPServer(BaseModel):
    server_name: ServerName
    connection: SSEConnection | StdioConnection | StreamableHTTPConnection
