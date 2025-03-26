# uv-mcp

A Model Context Protocol (MCP) server for interacting with Python installations via uv, the fast Python package installer.

## Overview

uv-mcp provides LLMs with direct access to inspect and manage Python environments through the [uv](https://github.com/astral-sh/uv) package manager. This allows AI assistants to help with Python dependency management, environment inspection, and troubleshooting tasks.

## Features

- **Environment Inspection**: Query installed packages and their versions
- **Dependency Resolution**: Check compatibility between packages
- **Environment Comparison**: Identify differences between local and cloud/production environments
- **Requirement Management**: Parse and validate requirements files
- **Package Information**: Retrieve metadata about PyPI packages
- **Virtual Environment Management**: Create and manage virtual environments

## How It Works

uv-mcp implements the [Model Context Protocol](https://modelcontextprotocol.io) to expose Python environment data and package management functionality through standardized resources and tools.

### Resources

- `python:packages://installed` - List of all installed packages and versions
- `python:packages://outdated` - List of installed packages with newer versions available
- `python:packages://{package_name}/latest` - Latest versions available for a package
- `python:packages://{package_name}/dependencies` - List of dependencies for a specific package
- `python:requirements://{file_path}` - Parsed content of requirements files

### Tools

- `uv_run(command: str[])` - Run a command or script
- `uv_init()` - Create a new project
- `uv_add(package_name: str, version: Optional[str])` - Add dependencies to the project
- `uv_remove(package_name: str)` - Remove dependencies from the project
- `uv_sync(dry_run: bool)` - Install all declared dependencies, uninstall anything not declared
- `uv_lock()` - Update the project's lockfile
- `pip(command: str[])` - Run a pip command
- `pip_install(package_name: str, version: Optional[str])` - Install a package using pip
- `pip_uninstall(package_name: str)` - Uninstall a package using pip
- `pip_list()` - List all installed packages using pip

## Usage

To start the server:

```bash
uvx uv-mcp
```

## Development

This project is built with the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and [uv](https://github.com/astral-sh/uv). 