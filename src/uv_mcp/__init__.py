"""uv-mcp - Model Context Protocol (MCP) server for interacting with Python installations via uv"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("uv-mcp")
except PackageNotFoundError:
    # Package is not installed
    __version__ = "0.0.0"