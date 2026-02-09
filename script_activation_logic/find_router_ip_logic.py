import subprocess
from pathlib import Path

def router_ip(path: Path):
    script = Path(__file__).parent.parent.parent.parent / "bin/check_router_ip"  # võtab deploy 2 taset üles praegusest failist
    # Kõik sisendid järjekorras
    inputs = [ "yes"]

    # Sisendi string ühe korraga
    input_data = "\n".join(inputs) + "\n"

    process = subprocess.Popen(
        ["bash", str(script)],
        cwd=path,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # Kirjuta kogu sisend
    try:
        process.stdin.write(input_data)
        process.stdin.flush()
    except BrokenPipeError:
        print("Skript lõpetas enne, kui kõik sisendid jõudsid")

    # Reaalajas stdout ja stderr lugemine
    stdout_lines = []
    stderr_lines = []

    for line in process.stdout:
        print("[STDOUT]", line, end="")
        stdout_lines.append(line)

    for line in process.stderr:
        print("[STDERR]", line, end="")
        stderr_lines.append(line)

    process.wait()
    return "".join(stdout_lines), "".join(stderr_lines), process.returncode