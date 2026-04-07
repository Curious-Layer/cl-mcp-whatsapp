import json
import logging

from fastmcp import FastMCP

logger = logging.getLogger("whatsapp-mcp-server")


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool(
        name="health_check",
        description="Check server readiness and configured authentication mode.",
    )
    def health_check() -> str:
        try:
            return json.dumps(
                {
                    "status": "ok",
                    "server": "CL WhatsApp MCP Server",
                }
            )
        except Exception as e:
            logger.error(f"Failed health_check: {e}")
            return json.dumps({"error": str(e)})
