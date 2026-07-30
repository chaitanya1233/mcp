import asyncio
from mcp.server.fastmcp import FastMCP
from pypdf import PdfReader

mcp = FastMCP('Devloper_mcp')

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

    
@mcp.tool()
def read_file(file_path: str) -> str:
    """Extract and return text from utf-8 coded text file."""

    with open(file=file_path, mode="r", encoding="utf-8") as file:
        content = file.read()

    return content

@mcp.tool()
def read_pdf(file_path:str) -> str:
    """Read the content of PDF"""
    reader = PdfReader(file_path)
    
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n\n"
    
    return text

@mcp.resource("info://server")
def server_info() -> str:
    """Return information about this MCP server."""
    return """
    Developer MCP Server

    Purpose:
    Provide tools, resources and prompts for AI applications.

    Available capabilities:
    - File reading
    - PDF reading
    - Server information
    """

@mcp.prompt()
def greeting_prompt(user:str) -> str:
    """Create a greeting prompt for the user"""
    return f"""Give the friendly greeting to the user {user}"""




    
if __name__ == "__main__":
    mcp.run()