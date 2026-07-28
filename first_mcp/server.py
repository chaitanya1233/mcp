from mcp.server.fastmcp import FastMCP


# Create MCP server
mcp = FastMCP("My First MCP Server")


# ============================================================
# TOOL
# ============================================================

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


# ============================================================
# RESOURCE
# ============================================================

@mcp.resource("greeting://hello")
def greeting() -> str:
    """Return a simple greeting."""
    return "Hello Chaitanya! Welcome to MCP."


# ============================================================
# PROMPT
# ============================================================

@mcp.prompt()
def greet_user(name: str) -> str:
    """Create a greeting prompt for a user."""
    return f"Give a friendly greeting to {name}."


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    mcp.run()