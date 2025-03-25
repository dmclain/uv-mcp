import subprocess
import json
import os
import sys
from typing import List, Dict, Any, Optional, Tuple, Union
import shlex
from . import uv

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
        full_command = [uv_bin] + command
        
        # Add --format=json if capturing JSON output
        if capture_json and "--format=json" not in command:
            full_command.append("--format=json")
            
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
    return run_uv_command(["pip", "list"], capture_json=json_format)

def get_outdated_packages(json_format: bool = True) -> Union[List[Dict[str, Any]], str]:
    """List outdated packages"""
    return run_uv_command(["pip", "list", "--outdated"], capture_json=json_format)

def get_package_info(package_name: str, json_format: bool = True) -> Union[Dict[str, Any], str]:
    """Get detailed information about a package"""
    return run_uv_command(["pip", "show", package_name], capture_json=json_format)

def install_package(package_name: str, version: Optional[str] = None) -> str:
    """Install a package using uv"""
    command = ["pip", "install"]
    
    if version:
        command.append(f"{package_name}=={version}")
    else:
        command.append(package_name)
    
    return run_uv_command(command)

def uninstall_package(package_name: str) -> str:
    """Uninstall a package using uv"""
    return run_uv_command(["pip", "uninstall", "--yes", package_name])

def parse_requirements(file_path: str, json_format: bool = True) -> Union[Dict[str, Any], str]:
    """Parse a requirements file"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Requirements file not found: {file_path}")
    
    return run_uv_command(["pip", "install", "--dry-run", "--report", "-r", file_path], 
                         capture_json=json_format)

def create_virtualenv(path: str, packages: Optional[List[str]] = None) -> str:
    """Create a new virtual environment"""
    command = ["venv", "create", path]
    result = run_uv_command(command)
    
    # Install packages if specified
    if packages and packages:
        python_bin = os.path.join(path, "bin", "python") if sys.platform != "win32" else os.path.join(path, "Scripts", "python.exe")
        
        for package in packages:
            subprocess.run([python_bin, "-m", "uv", "pip", "install", package], check=True)
    
    return result

def compare_environments(env_path1: str, env_path2: str) -> Dict[str, Any]:
    """Compare packages between two environments"""
    # Get packages in first environment
    python_bin1 = os.path.join(env_path1, "bin", "python") if sys.platform != "win32" else os.path.join(env_path1, "Scripts", "python.exe")
    result1 = subprocess.run([python_bin1, "-m", "uv", "pip", "list", "--format=json"], 
                           capture_output=True, text=True, check=True)
    packages1 = json.loads(result1.stdout)
    
    # Get packages in second environment
    python_bin2 = os.path.join(env_path2, "bin", "python") if sys.platform != "win32" else os.path.join(env_path2, "Scripts", "python.exe")
    result2 = subprocess.run([python_bin2, "-m", "uv", "pip", "list", "--format=json"], 
                           capture_output=True, text=True, check=True)
    packages2 = json.loads(result2.stdout)
    
    # Convert to dictionaries for easier comparison
    pkg_dict1 = {pkg["name"]: pkg["version"] for pkg in packages1}
    pkg_dict2 = {pkg["name"]: pkg["version"] for pkg in packages2}
    
    # Find differences
    only_in_env1 = [name for name in pkg_dict1 if name not in pkg_dict2]
    only_in_env2 = [name for name in pkg_dict2 if name not in pkg_dict1]
    
    # Find version differences
    version_differences = {}
    for name in pkg_dict1:
        if name in pkg_dict2 and pkg_dict1[name] != pkg_dict2[name]:
            version_differences[name] = {
                "env1": pkg_dict1[name],
                "env2": pkg_dict2[name]
            }
    
    return {
        "only_in_env1": only_in_env1,
        "only_in_env2": only_in_env2,
        "version_differences": version_differences
    } 