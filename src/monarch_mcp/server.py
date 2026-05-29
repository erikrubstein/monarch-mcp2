from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from monarch_mcp.groups import auth


def create_mcp() -> FastMCP:
    mcp = FastMCP("monarch")
    auth.register(mcp)
    return mcp


mcp = create_mcp()


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
