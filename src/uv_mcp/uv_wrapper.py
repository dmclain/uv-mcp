import subprocess
import json
import os
import sys
import uv
from typing import List, Dict, Any, Optional, Tuple, Union
import shlex

class UVError(Exception):
    """Base exception for UV command errors"""
    pass

class UVCommandError(UVError):
    """Exception raised when a UV command fails"""
    def __init__(self, command: str, returncode: int, stderr: str):
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        message = f"UV command '{command}' failed with exit code {returncode}: {stderr}"
        super().__init__(message)

class UVNotFoundError(UVError):
    """Exception raised when UV executable cannot be found"""
    pass

def run_uv_command(command: List[str], capture_json: bool = False) -> Union[str, Dict[str, Any]]:
    """
    Run a uv command and return the output
    
    Args:
        command: List of command arguments (without 'uv' prefix)
        capture_json: If True, attempt to parse output as JSON
    
    Returns:
        Command output as string or parsed JSON
    
    Raises:
        UVNotFoundError: If uv executable cannot be found
        UVCommandError: If command execution fails
    """
    try:
        uv_bin = uv.find_uv_bin()
        full_command = [uv_bin]
        
        full_command.extend(command)
            
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            check=False  # We'll handle errors ourselves
        )
        
        if result.returncode != 0:
            cmd_str = ' '.join(shlex.quote(arg) for arg in full_command)
            raise UVCommandError(cmd_str, result.returncode, result.stderr)
        
        if capture_json:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                # Fall back to returning raw output if JSON parsing fails
                return result.stdout
        
        return result.stdout
    
    except FileNotFoundError:
        raise UVNotFoundError(f"UV executable not found or could not be executed")

# Specific wrappers for common uv operations

def list_installed_packages(json_format: bool = True) -> Union[List[Dict[str, Any]], str]:
    """List all installed packages"""
    return run_uv_command(["pip", "list", "--format=json"])

def get_outdated_packages(json_format: bool = True) -> Union[List[Dict[str, Any]], str]:
    """List outdated packages"""
    return run_uv_command(["pip", "list", "--outdated", "--format=json"])

def get_package_info(package_name: str, json_format: bool = True) -> Union[Dict[str, Any], str]:
    """Get detailed information about a package"""
    return run_uv_command(["pip", "show", package_name, "--format=json"])

def install_package(package_name: str, version: Optional[str] = None) -> str:
    """Install a package using uv"""
    command = ["pip", "install"]
    
    if version:
        command.append(f"{package_name}=={version}")
    else:
        command.append(package_name)
    
    return run_uv_command(command)

def install_packages(packages: List[str | Tuple[str, str]]) -> str:
    """Install a package using uv"""
    command = ["pip", "install"]
    
    for package in packages:
        if isinstance(package, str):
            command.append(package)
        elif isinstance(package, tuple):
            command.append(f"{package[0]}=={package[1]}")
    
    return run_uv_command(command)

def uninstall_package(package_name: str) -> str:
    """Uninstall a package using uv"""
    return run_uv_command(["pip", "uninstall", "--yes", package_name])
