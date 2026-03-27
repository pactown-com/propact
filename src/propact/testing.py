"""Testing helpers for propact examples."""

import os
from pathlib import Path
from typing import Dict, Any, Optional


class ExampleHelper:
    """Helper class for creating and managing example files."""
    
    @staticmethod
    def create_sample_file(filename: str, content: str = None, directory: Optional[Path] = None) -> Path:
        """Create a sample file for testing examples.
        
        Args:
            filename: Name of the file to create
            content: Content to write to file (auto-generated if None)
            directory: Directory to create file in (current directory if None)
            
        Returns:
            Path to the created file
        """
        if directory is None:
            directory = Path.cwd()
        
        file_path = directory / filename
        
        # Auto-generate content based on file extension if not provided
        if content is None:
            ext = Path(filename).suffix.lower()
            if ext in ['.mp3', '.wav', '.aac']:
                content = f"FAKE AUDIO DATA FOR {filename.upper()}"
            elif ext in ['.mp4', '.avi', '.mov']:
                content = f"FAKE VIDEO DATA FOR {filename.upper()}"
            elif ext in ['.png', '.jpg', '.jpeg', '.gif']:
                content = f"FAKE IMAGE DATA FOR {filename.upper()}"
            elif ext in ['.json']:
                content = '{"sample": "data", "test": true}'
            elif ext in ['.yaml', '.yml']:
                content = 'sample:\n  data: test\n  enabled: true'
            elif ext in ['.txt', '.md']:
                content = f"Sample text content for {filename}"
            else:
                content = f"FAKE BINARY DATA FOR {filename.upper()}"
        
        file_path.write_text(content)
        return file_path
    
    @staticmethod
    def cleanup_files(*files: Path) -> None:
        """Clean up created files.
        
        Args:
            *files: Files to remove
        """
        for file_path in files:
            try:
                if file_path.exists():
                    file_path.unlink()
            except Exception as e:
                print(f"Warning: Could not delete {file_path}: {e}")
    
    @staticmethod
    def check_dependencies(command: str) -> bool:
        """Check if a command/dependency is available.
        
        Args:
            command: Command to check
            
        Returns:
            True if command is available
        """
        import shutil
        return shutil.which(command) is not None
    
    @staticmethod
    def check_env_var(name: str) -> Optional[str]:
        """Check if environment variable is set.
        
        Args:
            name: Environment variable name
            
        Returns:
            Value of environment variable or None
        """
        return os.getenv(name)
    
    @staticmethod
    def print_status(message: str, status: str = "INFO") -> None:
        """Print formatted status message.
        
        Args:
            message: Message to print
            status: Status type (INFO, WARNING, ERROR, SUCCESS)
        """
        colors = {
            "INFO": "",
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "SUCCESS": "\033[92m"
        }
        reset = "\033[0m"
        
        color = colors.get(status, "")
        print(f"{color}[{status}]{reset} {message}")
    
    @staticmethod
    def run_example(example_dir: Path, endpoint: str = None, schema: str = None, 
                   mode: str = None, port: int = None) -> Dict[str, Any]:
        """Run a propact example with the given parameters.
        
        Args:
            example_dir: Directory containing the example
            endpoint: Endpoint to send data to
            schema: Schema file to use
            mode: Mode to run in (execute/server)
            port: Port for server mode
            
        Returns:
            Result dictionary with success status and any errors
        """
        import subprocess
        import sys
        
        readme_path = example_dir / "README.md"
        if not readme_path.exists():
            return {"success": False, "error": f"README.md not found in {example_dir}"}
        
        # Find the src directory
        src_dir = None
        current = example_dir
        while current.parent != current:
            potential_src = current / "src"
            if potential_src.exists() and (potential_src / "propact").exists():
                src_dir = potential_src
                break
            current = current.parent
        
        if not src_dir:
            return {"success": False, "error": "Could not find propact source directory"}
        
        # Build command
        cmd = [sys.executable, "-m", "propact.cli", str(readme_path)]
        
        # Set environment
        env = os.environ.copy()
        env["PYTHONPATH"] = str(src_dir) + ":" + env.get("PYTHONPATH", "")
        
        if endpoint:
            cmd.extend(["--endpoint", endpoint])
        if schema:
            cmd.extend(["--schema", str(schema)])
        if mode:
            cmd.extend(["--mode", mode])
        if port:
            cmd.extend(["--port", str(port)])
        
        # Run command
        try:
            result = subprocess.run(
                cmd,
                cwd=example_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Predefined sample data for common use cases
SAMPLE_DATA = {
    "audio_podcast": "This is a sample podcast episode about technology and innovation.\nEpisode 42: The Future of AI\nDuration: 45 minutes\nHost: Tech Expert",
    "medical_scan": "Patient: John Doe\nAge: 45\nDate: 2024-01-15\nType: Chest X-ray\nFindings: Clear lungs, no abnormalities detected",
    "demo_video": "Demo video showing propact capabilities\n- Markdown parsing\n- Protocol adaptation\n- Response conversion\nDuration: 30 seconds",
    "config_file": "server:\n  host: localhost\n  port: 8080\n  debug: false\n\nfeatures:\n  - authentication\n  - logging\n  - monitoring",
    "api_response": '{"status": "success", "data": {"id": 123, "message": "Operation completed successfully"}, "timestamp": "2024-01-15T10:30:00Z"}'
}
