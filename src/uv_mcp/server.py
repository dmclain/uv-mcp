from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional, Tuple
from uv_mcp import uv_wrapper

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
@mcp.tool()
def list_packages() -> List[Dict[str, str]]:
    """List all installed packages"""
    packages = uv_wrapper.list_installed_packages()
    if isinstance(packages, list):
        return packages
    return [{"name": "error", "version": "Failed to retrieve packages"}]

@mcp.tool()
def get_package_info(package_name: str) -> Dict[str, Any]:
    """Get detailed info about a package"""
    info = uv_wrapper.get_package_info(package_name)
    if isinstance(info, dict):
        return info
    return {"name": package_name, "error": "Failed to retrieve package information"}

@mcp.tool()
def install_package(package_name: str, version: Optional[str] = None) -> str:
    """Install a package"""
    return uv_wrapper.install_package(package_name, version)

@mcp.tool()
def install_packages(packages: List[str | Tuple[str, str]]) -> str:
    """Install multiple packages"""
    return uv_wrapper.install_packages(packages)

# Additional tools that might be useful
@mcp.tool()
def uninstall_package(package_name: str) -> str:
    """Uninstall a package"""
    return uv_wrapper.uninstall_package(package_name)
