# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")

# Add a multiply tool
@mcp.tool()
def multiply(first: int, second: int) -> int:
    """Multiply two numbers"""
    return first * second

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalised greeting"""
    return f"Hello, {name}!"

@mcp.resource("command://ping")
def get_echo() -> str:
    """Send pong"""
    return "Pong"

@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"