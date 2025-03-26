#!/usr/bin/env python3
"""
CLI entry point for uv-mcp.

This module provides the main entry point for the uv-mcp tool.
"""

import sys
import argparse
import os

def main():
    """
    Main entry point for the uv-mcp tool.
    
    This function parses command-line arguments and runs the MCP server.
    """
    parser = argparse.ArgumentParser(
        description="MCP server for interacting with Python installations via uv"
    )
    
    parser.add_argument(
        "venv_path", 
        nargs="?", 
        help="Path to a virtual environment to use. If not provided, will check for .venv or venv directories"
    )
    
    args = parser.parse_args()
    
    # Set the virtualenv path as an environment variable to be picked up by the server
    if args.venv_path:
        os.environ["UV_MCP_VENV_PATH"] = args.venv_path
    
    # Import the server module
    try:
        from uv_mcp.server import mcp
        
        # Run the server
        mcp.run()
    except ImportError as e:
        print(f"Error importing server module: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error running server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 