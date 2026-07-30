import sys
import asyncio 
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import ClientSession

#----------------------------
# SERVER CONFIGURATION
#----------------------------
server_params = StdioServerParameters(
    command=sys.executable,
    args=["server.py"]    
)

async def main():
    
    #---------------------------------
    # START MCP SERVER
    #---------------------------------
    async with stdio_client(server_params) as (read,write):
        
        #----------------------------
        # CREATE A CLIENT SESSION
        #----------------------------
        async with ClientSession(read,write) as session:
            
            #---------------------------
            # INIRIALIZE SESSION
            #---------------------------
            await session.initialize()
            print("\nMCP Server connection initialized.")
            
            # =================================================
            # DISCOVER TOOLS
            # =================================================
            
            print("\n==TOOLS==:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(tool.name)
                
            # =================================================
            # DISCOVER RESOURCES
            # =================================================
            
            print("\n+==RESOURCES==:")
            resources = await session.list_resources()
            for resource in resources.resources:
                print(resource.uri)
                
            
            # =================================================
            # DISCOVER PROMPTS
            # =================================================
            
            print("\n==PROMPTS")
            prompts = await session.list_prompts()
            for prompt in prompts.prompts:
                print(prompt.name)
                
            
            # =================================================
            # CALL TOOL
            # =================================================
            
            tool_result = await session.call_tool(
                "add_numbers",
                arguments={
                    "a":10,
                    "b":20
                }
            )    
            
            print("tool result:\n",tool_result,"\n\n")
            print("===================================")
            # =================================================
            # READ RESOURCE
            # =================================================
            
            resource_result = await session.read_resource(
                    "info://server" 
            )            
            
            print("Resource result:\n",resource_result,"\n\n")
            print("===================================")
            
            # =================================================
            # GET PROMPT
            # =================================================
            
            prompt_result = await session.get_prompt(
                "greeting_prompt",
                arguments={"user":"Aahilya"}
            )            
            
            print("Prompt result:\n",prompt_result,"\n\n")
                                
if __name__ == "__main__":
    asyncio.run(main())            