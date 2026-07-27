from pydantic import BaseModel


class MCPGatewayProcessInfo(BaseModel):
    host: str
    port: int
    pid: int
    create_time: float
