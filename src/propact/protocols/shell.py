"""Shell protocol implementation for Propact."""

import asyncio
from typing import Dict, Any, Optional
from pathlib import Path


class ShellProtocol:
    """Handles shell command execution within Protocol Pact."""
    
    def __init__(self, shell: str = "/bin/bash"):
        """
        Initialize ShellProtocol.
        
        Args:
            shell: Shell executable to use.
        """
        self.shell = shell
        
    async def execute(self, command: str, cwd: Optional[Path] = None, 
                     env: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Execute a shell command.
        
        Args:
            command: Shell command to execute.
            cwd: Working directory for command execution.
            env: Environment variables for command execution.
            
        Returns:
            Dictionary with execution results.
        """
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                env=env,
                executable=self.shell
            )
            
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "returncode": process.returncode,
                "stdout": stdout.decode('utf-8') if stdout else "",
                "stderr": stderr.decode('utf-8') if stderr else "",
                "command": command,
                "cwd": str(cwd) if cwd else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": command,
                "cwd": str(cwd) if cwd else None
            }
            
    async def execute_script(self, script: str, cwd: Optional[Path] = None,
                           env: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Execute a multi-line shell script.
        
        Args:
            script: Shell script content.
            cwd: Working directory for script execution.
            env: Environment variables for script execution.
            
        Returns:
            Dictionary with execution results.
        """
        return await self.execute(script, cwd=cwd, env=env)
