from mcp.server import MCPServer

mcp = MCPServer("Meu MCP Server")


@mcp.tool()
def somar(a: int, b: int) -> int:
    """Soma dois números."""
    return a + b

@mcp.tool()
def multiplicar(a: int, b: int) -> int:
    """Multiplica dois números inteiros."""
    return a * b


@mcp.tool()
def saudacao(nome: str) -> str:
    """Retorna uma saudação personalizada."""
    return f"Olá, {nome}! Bem-vindo ao nosso AI Agent."


if __name__ == "__main__":
    mcp.run()