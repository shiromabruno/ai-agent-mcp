import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="../mcp-server/.venv/bin/python",
        args=["../mcp-server/server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Inicializa a comunicação MCP
            await session.initialize()

            # Pergunta ao servidor quais tools estão disponíveis
            tools = await session.list_tools()

            print("Tools disponíveis:")
            for tool in tools.tools:
                print(f"- {tool.name}")

            # Executa uma tool remotamente via MCP
            resultado = await session.call_tool(
                "somar",
                arguments={
                    "a": 10,
                    "b": 20
                }
            )

            print("\nResultado:")
            print(resultado.content)


if __name__ == "__main__":
    asyncio.run(main())