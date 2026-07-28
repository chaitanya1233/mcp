import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Configure MCP Server
server_params = StdioServerParameters(
    command=sys.executable,
    args=["server.py"]
)


async def main():

    # Start MCP server using stdio
    async with stdio_client(server_params) as (read, write):

        # Create MCP Client Session
        async with ClientSession(read, write) as session:

            # Initialize the connection
            await session.initialize()

            #--------------------------------
            # Discover tools
            #--------------------------------
            tools = await session.list_tools()
            print(tools)
            
            print("="*50)
            
            print("File Content:\n\n")
            
            #--------------------------------
            # Call tool 
            #--------------------------------
            
            result = await session.call_tool(
                "read_pdf",
                arguments={  # hear file_path is the arguement name that read_file function accepts.add()
                    "file_path" :"C:/Users/chait/OneDrive/Desktop/FYP/Data/Data Science/DSM NOTES UNIT 3.pdf"
                } 
                
            )

            print(result)

if __name__ == "__main__":
    asyncio.run(main())