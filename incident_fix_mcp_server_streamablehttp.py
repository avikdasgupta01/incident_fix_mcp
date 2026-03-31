from __future__ import annotations

import os

from incident_fix_mcp_server import mcp


HOST = os.getenv("INCIDENT_FIX_HOST", "127.0.0.1")
PORT = int(os.getenv("INCIDENT_FIX_PORT", "8000"))
PATH = os.getenv("INCIDENT_FIX_PATH", "/mcp")


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host=HOST,
        port=PORT,
        path=PATH,
    )
