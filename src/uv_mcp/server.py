from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional, Tuple
from uv_mcp.uv_wrapper import UVWrapper
import os

# Get venv path from environment variable if set by CLI
venv_path = os.environ.get("UV_MCP_VENV_PATH")

# Create a UVWrapper instance with the virtualenv path
uv_wrapper = UVWrapper(venv_path)

# Create uv-mcp server with dependencies
mcp = FastMCP("uv-mcp", dependencies=["uv"])

# Resources
@mcp.resource("python:packages://installed", name="Installed Python Packages", mime_type="application/json")
def get_installed_packages() -> List[Dict[str, Any]]:
    """List of all installed packages and versions"""
    try:
        packages = uv_wrapper.list_installed_packages()
        return packages
    except Exception as e:
        return f"Error retrieving installed packages: {str(e)}"

@mcp.resource("python:packages://outdated", name="Outdated Python Packages", mime_type="application/json")
def get_outdated_packages() -> List[Dict[str, Any]]:
    """List of installed packages with newer versions available"""
    try:
        outdated = uv_wrapper.get_outdated_packages()
        return outdated
    except Exception as e:
        return f"Error retrieving outdated packages: {str(e)}"

@mcp.resource("python:packages://{package_name}/info", name="Python Package Information", mime_type="application/json")
def get_package_info_resource(package_name: str) -> Dict[str, Any]:
    """Detailed information about a specific package"""
    try:
        info = uv_wrapper.get_package_info(package_name)
        return info
    except Exception as e:
        return f"Error retrieving info for {package_name}: {str(e)}"

# Tools
@mcp.tool("run")
def run_command(command: List[str]) -> str:
    """Run a command or script"""
    try:
        return uv_wrapper.run_uv_command(["run"] + command)
    except Exception as e:
        return f"Error running command: {str(e)}"

@mcp.tool("init")
def init_project() -> str:
    """Create a new project"""
    try:
        return uv_wrapper.run_uv_command(["init"])
    except Exception as e:
        return f"Error initializing project: {str(e)}"

@mcp.tool("add")
def add_dependency(package_name: str, version: Optional[str] = None) -> str:
    """Add dependencies to the project"""
    try:
        return uv_wrapper.add_dependency(package_name, version)
    except Exception as e:
        return f"Error adding dependency {package_name}: {str(e)}"

@mcp.tool("remove")
def remove_dependency(package_name: str) -> str:
    """Remove dependencies from the project"""
    try:
        return uv_wrapper.remove_dependency(package_name)
    except Exception as e:
        return f"Error removing dependency {package_name}: {str(e)}"

@mcp.tool("sync")
def sync_dependencies(dry_run: bool = False) -> str:
    """Install all declared dependencies, uninstall anything not declared"""
    try:
        command = ["sync"]
        if dry_run:
            command.append("--dry-run")
        return uv_wrapper.run_uv_command(command)
    except Exception as e:
        return f"Error syncing dependencies: {str(e)}"

@mcp.tool("lock")
def lock_dependencies() -> str:
    """Update the project's lockfile"""
    try:
        return uv_wrapper.run_uv_command(["lock"])
    except Exception as e:
        return f"Error locking dependencies: {str(e)}"

@mcp.tool("pip")
def pip_command(command: List[str]) -> str:
    """Run a pip command"""
    try:
        pip_cmd = ["pip"] + command
        return uv_wrapper.run_uv_command(pip_cmd)
    except Exception as e:
        return f"Error running pip command: {str(e)}"

@mcp.tool("pip_install")
def pip_install(package_name: str, version: Optional[str] = None) -> str:
    """Install a package using pip"""
    try:
        return uv_wrapper.install_package(package_name, version)
    except Exception as e:
        return f"Error installing {package_name}: {str(e)}"

@mcp.tool("pip_uninstall")
def pip_uninstall(package_name: str) -> str:
    """Uninstall a package using pip"""
    try:
        return uv_wrapper.uninstall_package(package_name)
    except Exception as e:
        return f"Error uninstalling {package_name}: {str(e)}"

@mcp.tool("pip_list")
def pip_list() -> List[Dict[str, Any]]:
    """List all installed packages using pip"""
    try:
        return uv_wrapper.list_installed_packages()
    except Exception as e:
        return f"Error listing packages: {str(e)}"