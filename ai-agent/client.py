import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
#     StdioServerParameters(...)
# é um objeto que diz ao cliente como iniciar o processo do servidor.
#     command=...
# indica qual executável vai rodar: o Python da venv do servidor.
#      args=["../mcp-server/server.py"]
# informa quais argumentos passar para esse Python, ou seja, qual script executar:
# o arquivo server.py dentro da pasta mcp-server.
    server_params = StdioServerParameters(
        command="../mcp-server/.venv/bin/python",
        args=["../mcp-server/server.py"]
    )

# abrir a comunicação via stdin/stdout com esse processo, 
# permitindo que o cliente chame ferramentas do servidor 
# com session.call_tool(...)
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Inicializa a comunicação MCP
            await session.initialize()

            # Pergunta ao servidor quais tools estão disponíveis
            tools = await session.list_tools()

            print("Tools disponíveis:")
            for tool in tools.tools:
                print("Nome:", tool.name)
                print("Descrição:", tool.description)
                print("Schema:", tool.input_schema)
                print("------------------------")

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