import sys
import asyncio
import json
import os

from dotenv import load_dotenv
from groq import Groq

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# MCP SERVER CONFIGURATION
# ============================================================

server_params = StdioServerParameters(
    command=sys.executable,
    args=["server.py"]
)


# ============================================================
# MCP TOOL → LLM TOOL FORMAT
# ============================================================

def get_tools(tool):
    """
    Convert an MCP tool definition into
    the tool format expected by the LLM.
    """

    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.inputSchema
        }
    }


# ============================================================
# MAIN
# ============================================================

async def main():

    # --------------------------------------------------------
    # Connect to MCP server using STDIO
    # --------------------------------------------------------

    async with stdio_client(
        server_params
    ) as (read, write):

        # Create MCP client session
        async with ClientSession(
            read,
            write
        ) as session:

            # ------------------------------------------------
            # Initialize MCP connection
            # ------------------------------------------------

            await session.initialize()

            print("MCP connection initialized.\n")


            # =================================================
            # 1. DISCOVER MCP TOOLS
            # =================================================

            tools = await session.list_tools()

            print("===== MCP TOOLS =====")

            llm_tools = []

            for tool in tools.tools:

                print(
                    f"- {tool.name}: "
                    f"{tool.description}"
                )

                llm_tool = get_tools(tool)

                llm_tools.append(llm_tool)

            print()


            # =================================================
            # 2. USER MESSAGE
            # =================================================

            messages = [
                {
                    "role": "user",
                    "content": (
                        "Read this PDF and tell me "
                        "what AI and technical skills "
                        "are mentioned in my resume: "
                        "C:/Users/chait/Downloads/"
                        "resume_chaitanya.pdf"
                    )
                }
            ]


            # =================================================
            # 3. FIRST LLM CALL
            #
            # LLM decides which MCP tool to use
            # =================================================

            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",

                messages=messages,

                tools=llm_tools,

                tool_choice="auto"
            )


            # Get assistant response
            assistant_message = response.choices[0].message


            # =================================================
            # 4. CHECK WHETHER LLM WANTS A TOOL
            # =================================================

            if not assistant_message.tool_calls:

                print("===== FINAL ANSWER =====")
                print(assistant_message.content)

                return


            # =================================================
            # 5. ADD ASSISTANT TOOL CALL TO CONVERSATION
            # =================================================

            messages.append(
                assistant_message
            )


            # =================================================
            # 6. PROCESS TOOL CALLS
            # =================================================

            for tool_call in assistant_message.tool_calls:

                # --------------------------------------------
                # Extract tool name
                # --------------------------------------------

                tool_name = tool_call.function.name


                # --------------------------------------------
                # Extract tool arguments
                # --------------------------------------------

                arguments = json.loads(
                    tool_call.function.arguments
                )


                print("===== LLM TOOL CALL =====")

                print(
                    "Tool:",
                    tool_name
                )

                print(
                    "Arguments:",
                    arguments
                )


                # =================================================
                # 7. EXECUTE MCP TOOL
                # =================================================

                result = await session.call_tool(
                    tool_name,
                    arguments=arguments
                )


                print("\n===== MCP TOOL EXECUTED =====")

                print(
                    "Tool:",
                    tool_name
                )


                # =================================================
                # 8. EXTRACT MCP RESULT
                # =================================================

                if result.isError:

                    tool_result = (
                        "The MCP tool failed: "
                        + str(result.content)
                    )

                elif result.structuredContent:

                    tool_result = str(
                        result.structuredContent.get(
                            "result",
                            result.structuredContent
                        )
                    )

                else:

                    # Fallback for tools that only return
                    # TextContent
                    tool_result = "\n".join(
                        item.text
                        for item in result.content
                        if hasattr(item, "text")
                    )


                print(
                    "Result received from MCP."
                )


                # =================================================
                # 9. SEND MCP RESULT BACK TO LLM
                # =================================================

                messages.append(
                    {
                        "role": "tool",

                        "tool_call_id":
                            tool_call.id,

                        "content":
                            tool_result
                    }
                )


            # =================================================
            # 10. SECOND LLM CALL
            #
            # LLM now has:
            # - Original user request
            # - Its tool call
            # - MCP tool result
            # =================================================

            final_response = (
                groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",

                    messages=messages
                )
            )


            # =================================================
            # 11. FINAL ANSWER
            # =================================================

            final_message = (
                final_response
                .choices[0]
                .message
            )

            print("\n====================================")
            print("===== FINAL ANSWER =====")
            print("====================================\n")

            print(
                final_message.content
            )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())


