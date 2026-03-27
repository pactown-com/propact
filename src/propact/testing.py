"""Testing helpers for propact examples."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess
import sys

from .config import get_config


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
            config = get_config()
            result = subprocess.run(
                cmd,
                cwd=example_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=config.request_timeout
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
