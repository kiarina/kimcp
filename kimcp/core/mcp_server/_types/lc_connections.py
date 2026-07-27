from .lc_connection import LCConnection
from .server_name import ServerName

type LCConnections = dict[ServerName, LCConnection]
