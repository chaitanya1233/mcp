import asyncio 
import sys
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import ClientSession
 

server_params = StdioServerParameters(
    command = sys.executable,
    args=['server.py']
)

async def main():
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            
            # Discover available tools 
            tools = await session.list_tools()
            
            print("===== AVAILABLE TOOLS =====")
            for tool in tools.tools:
                print(f"-{tool.name}")
                
                   
            # MANNUAL DECISION
            selected_tool = "read_pdf"
            
            
            file_path =  (
                "C:/Users/chait/OneDrive/Desktop/"
                "FYP/Data/Data Science/DSM NOTES UNIT 3.pdf"
            )
             
            
            # EXECUTE MCP TOOL 
            result = await session.call_tool(
                selected_tool,
                arguments={"file_path":file_path}
            )   
            
            print("\n==TOOL RESULT:==")
            print(result.structuredContent['result'])
            
            
if __name__ == "__main__":
    asyncio.run(main())                
    

        

