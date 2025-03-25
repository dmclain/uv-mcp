from mcp.server.fastmcp import FastMCP, Context
from typing import List, Dict, Any, Optional
import uv_wrapper

# Create uv-mcp server with dependencies
mcp = FastMCP("uv-mcp", dependencies=["uv"])

# Resources
@mcp.resource("python:packages://installed")
def get_installed_packages() -> str:
    """List of all installed packages and versions"""
    try:
        packages = uv_wrapper.list_installed_packages()
        return str(packages)
    except Exception as e:
        return f"Error retrieving installed packages: {str(e)}"

@mcp.resource("python:packages://outdated")
def get_outdated_packages() -> str:
    """List of installed packages with newer versions available"""
    try:
        outdated = uv_wrapper.get_outdated_packages()
        return str(outdated)
    except Exception as e:
        return f"Error retrieving outdated packages: {str(e)}"

@mcp.resource("python:packages://{package_name}/info")
def get_package_info_resource(package_name: str) -> str:
    """Detailed information about a specific package"""
    try:
        info = uv_wrapper.get_package_info(package_name)
        return str(info)
    except Exception as e:
        return f"Error retrieving info for {package_name}: {str(e)}"

@mcp.resource("python:requirements://{file_path}")
def get_requirements_info(file_path: str) -> str:
    """Parsed content of requirements files"""
    try:
        requirements = uv_wrapper.parse_requirements(file_path)
        return str(requirements)
    except Exception as e:
        return f"Error parsing requirements from {file_path}: {str(e)}"

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
def check_package_installed(package_name: str) -> bool:
    """Check if a package is installed"""
    try:
        packages = uv_wrapper.list_installed_packages()
        if isinstance(packages, list):
            return any(pkg["name"].lower() == package_name.lower() for pkg in packages)
        return False
    except Exception:
        return False

@mcp.tool()
def compare_environments(env_path1: str, env_path2: str) -> Dict[str, Any]:
    """Compare two environments"""
    return uv_wrapper.compare_environments(env_path1, env_path2)

@mcp.tool()
def install_package(package_name: str, version: Optional[str] = None) -> str:
    """Install a package"""
    return uv_wrapper.install_package(package_name, version)

@mcp.tool()
def create_virtualenv(path: str, packages: List[str] = None) -> str:
    """Create a new virtual environment"""
    return uv_wrapper.create_virtualenv(path, packages)

# Additional tools that might be useful
@mcp.tool()
def uninstall_package(package_name: str) -> str:
    """Uninstall a package"""
    return uv_wrapper.uninstall_package(package_name)

@mcp.tool()
def upgrade_package(package_name: str) -> str:
    """Upgrade a package to the latest version"""
    # Using install with no version specified should upgrade to the latest
    return uv_wrapper.install_package(package_name)

@mcp.tool()
def parse_requirements(file_path: str) -> List[Dict[str, str]]:
    """Parse a requirements file"""
    result = uv_wrapper.parse_requirements(file_path)
    if isinstance(result, dict) and "install" in result:
        return [{"name": pkg["name"], "version": pkg.get("version", "")} 
                for pkg in result["install"]]
    return [{"name": "error", "version": "Failed to parse requirements"}]

if __name__ == "__main__":
    mcp.run()