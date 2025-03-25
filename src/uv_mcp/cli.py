#!/usr/bin/env python3
"""
CLI entry point for uv-mcp.

This module provides the main entry point for the uv-mcp tool.
"""

import sys
import argparse

def main():
    """
    Main entry point for the uv-mcp tool.
    
    This function parses command-line arguments and runs the MCP server.
    """
    parser = argparse.ArgumentParser(
        description="MCP server for interacting with Python installations via uv"
    )
    parser.add_argument(
        "--host", 
        default="127.0.0.1",
        help="Host to bind the server to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=0,
        help="Port to bind the server to (default: auto-select)"
    )
    parser.add_argument(
        "--verbose", 
        "-v", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Import the server module
    try:
        from uv_mcp.server import mcp
        
        # Run the server
        print(f"Starting uv-mcp server...")
        mcp.run()
    except ImportError as e:
        print(f"Error importing server module: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error running server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 