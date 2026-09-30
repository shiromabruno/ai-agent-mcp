import asyncio
import json

from urllib import response
from openai import OpenAI

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

    openai_client = OpenAI()

# abrir a comunicação via stdin/stdout com esse processo, 
# permitindo que o cliente chame ferramentas do servidor 
# com session.call_tool(...)
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Inicializa a comunicação MCP
            await session.initialize()

            # Pergunta ao servidor quais tools estão disponíveis
            tools = await session.list_tools()

            # print("Tools disponíveis:")
            # for tool in tools.tools:
            #     print("Nome:", tool.name)
            #     print("Descrição:", tool.description)
            #     print("Schema:", tool.input_schema)
            #     print("------------------------")

            openai_tools = []

            for tool in tools.tools:
                openai_tools.append({
                    "type": "function",
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema
                })

            print("Tools disponíveis do openai_tools:")
            print(openai_tools)

            response = openai_client.responses.create(
                model="gpt-5.6-luna",
                input="Quanto é 15 vezes 7?",
                tools=openai_tools
            )

            # response = openai_client.responses.create(
            #     model="gpt-5.6-luna",
            #     input="Quanto é 15 mais 7?",
            #     tools=openai_tools
            # )

            # print(response.output)
            # ResponseFunctionToolCall(arguments='{"a":15,"b":7}', call_id='call_0kVq51Tog8kevL78pz2iDMTT', 
            # name='somar', type='function_call', id='fc_01166c0e5f2337a4006abc607dbf6087d1909b8376eaa353c6', 
            # async_=None, caller=None, namespace=None, status='completed')]

            for item in response.output:
                if item.type == "function_call":

                    print("Tool escolhida:", item.name)
                    print("Argumentos recebidos:", item.arguments)

                    arguments = json.loads(item.arguments)
                    print("Argumentos json.loads:", arguments)

                    result = await session.call_tool(
                        item.name,
                        arguments
                    )

                    print("Resultado MCP:", result)

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