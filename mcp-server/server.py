from mcp.server import MCPServer

mcp = MCPServer("Meu MCP Server")


@mcp.tool()
def somar(a: int, b: int) -> int:
    """Soma dois números."""
    return a + b


if __name__ == "__main__":
    mcp.run()