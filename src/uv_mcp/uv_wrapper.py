import subprocess
import json
import os
import sys
import uv
from typing import List, Dict, Any, Optional, Tuple, Union
import shlex
import pathlib

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

def spec(package_name: str, version: Optional[str] = None) -> Tuple[str, Optional[str]]:
    if version:
        return f"{package_name}=={version}"
    else:
        return package_name

class UVWrapper:
    """Wrapper class for UV CLI operations with virtual environment support"""
    
    def __init__(self, venv_path: Optional[str] = None):
        """
        Initialize with optional virtual environment path
        
        Args:
            venv_path: Path to virtual environment. If None, will look for .venv or venv
        """
        self.venv_path = self._resolve_venv_path(venv_path)
        print(f"Using virtual environment: {self.venv_path}")
        
    def _resolve_venv_path(self, venv_path: Optional[str]) -> Optional[str]:
        """
        Resolve the virtual environment path
        
        If venv_path is provided, use it.
        Otherwise, check if .venv or venv exists in the current directory.
        
        Returns:
            The resolved path or None if no venv found
        """
        if venv_path:
            path = pathlib.Path(venv_path)
            if not path.exists():
                print(f"Warning: Specified virtual environment path {venv_path} does not exist", file=sys.stderr)
            return str(path.absolute())
            
        # Check for .venv or venv in current directory
        for venv_dir in ['.venv', 'venv']:
            path = pathlib.Path(venv_dir)
            if path.exists() and path.is_dir():
                return str(path.absolute())
                
        return None
        
    def run_uv_command(self, command: List[str]) -> Union[str, Dict[str, Any]]:
        """
        Run a uv command and return the output
        
        Args:
            command: List of command arguments (without 'uv' prefix)
        
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
            
            env = os.environ.copy()
            
            # If we have a venv path, add it to the command
            if self.venv_path:
                env["VIRTUAL_ENV"] = self.venv_path
                env["PATH"] = os.path.join(self.venv_path, "bin") + os.pathsep + env["PATH"]
                
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                check=False,  # We'll handle errors ourselves
                env=env
            )
            
            if result.returncode != 0:
                cmd_str = ' '.join(shlex.quote(arg) for arg in full_command)
                raise UVCommandError(cmd_str, result.returncode, result.stderr)
            
            return result.stdout
        
        except FileNotFoundError:
            raise UVNotFoundError(f"UV executable not found or could not be executed")