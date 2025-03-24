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

## Example Interactions

An LLM can ask questions or perform tasks like:

- "What packages are installed in the current environment?"
- "Is package X installed? What version?"
- "What's the latest version of package Y available on PyPI?"
- "Are there any dependency conflicts in this requirements.txt file?"
- "What packages in my local environment differ from those specified in requirements.txt?"
- "Create a new virtual environment with these dependencies"
- "Add package Z to the current environment"

## How It Works

uv-mcp implements the [Model Context Protocol](https://modelcontextprotocol.io) to expose Python environment data and package management functionality through standardized resources and tools.

### Resources

- `packages://installed` - List of all installed packages and versions
- `packages://outdated` - List of installed packages with newer versions available
- `packages://{package_name}/info` - Detailed information about a specific package
- `requirements://{file_path}` - Parsed content of requirements files

### Tools

- `list_packages()` - List all installed packages
- `get_package_info(package_name: str)` - Get detailed info about a package
- `check_package_installed(package_name: str)` - Check if a package is installed
- `compare_environments(env_path1: str, env_path2: str)` - Compare two environments
- `install_package(package_name: str, version: Optional[str])` - Install a package
- `create_virtualenv(path: str, packages: List[str])` - Create a new virtual environment

## Installation

```bash
pip install uv-mcp
```

## Usage

To start the server:

```bash
uv-mcp serve
```

In Claude Desktop or other MCP-compatible clients, you can install this server with:

```bash
mcp install uv-mcp
```

## Development

This project is built with the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and [uv](https://github.com/astral-sh/uv). 