import subprocess
from pathlib import Path

def create_template(path: Path):
    script = Path(__file__).parent.parent.parent / "create_system_template"  # võtab deploy 2 taset üles praegusest failist
    result = subprocess.run(
        ["bash", str(script)],
        capture_output=True,
        text=True,
        cwd=path
    )
    return [result.stdout, result.stderr, result.returncode]