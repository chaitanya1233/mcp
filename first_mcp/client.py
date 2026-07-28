import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ============================================================
# CONFIGURE MCP SERVER
# ============================================================

server_params = StdioServerParameters(
    command=sys.executable,
    args=["server.py"],
)


async def main():

    # ========================================================
    # START MCP SERVER USING STDIO
    # ========================================================

    async with stdio_client(
        server_params,
        errlog=sys.stderr
    ) as (read, write):

        # ====================================================
        # CREATE MCP CLIENT SESSION
        # ====================================================

        async with ClientSession(read, write) as session:

            # =================================================
            # INITIALIZE CONNECTION
            # =================================================

            await session.initialize()


            # =================================================
            # 1. DISCOVER TOOLS
            # =================================================

            tools = await session.list_tools()

            print("\n===== AVAILABLE TOOLS =====")

            for tool in tools.tools:
                print(tool.name)


            # =================================================
            # 2. CALL TOOL
            # =================================================

            result = await session.call_tool(
                "add_numbers",
                arguments={
                    "a": 10,
                    "b": 20
                }
            )

            print("\n===== TOOL RESULT =====")
            print(result)


            # =================================================
            # 3. DISCOVER RESOURCES
            # =================================================

            resources = await session.list_resources()

            print("\n===== AVAILABLE RESOURCES =====")

            for resource in resources.resources:
                print(resource.uri)


            # =================================================
            # 4. READ RESOURCE
            # =================================================

            resource_result = await session.read_resource(
                "greeting://hello"
            )

            print("\n===== RESOURCE RESULT =====")
            print(resource_result)


            # =================================================
            # 5. DISCOVER PROMPTS
            # =================================================

            prompts = await session.list_prompts()

            print("\n===== AVAILABLE PROMPTS =====")

            for prompt in prompts.prompts:
                print(prompt.name)


            # =================================================
            # 6. GET PROMPT
            # =================================================

            prompt_result = await session.get_prompt(
                "greet_user",
                arguments={
                    "name": "Chaitanya"
                }
            )

            print("\n===== PROMPT RESULT =====")
            print(prompt_result)


# ============================================================
# RUN CLIENT
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())