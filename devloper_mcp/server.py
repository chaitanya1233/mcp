import asyncio
from mcp.server.fastmcp import FastMCP
from pypdf import PdfReader

mcp = FastMCP('Devloper_mcp')
    
@mcp.tool()
def read_file(file_path: str) -> str:
    """Extract and return text from PDF file."""

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



    
if __name__ == "__main__":
    mcp.run()