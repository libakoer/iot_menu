import subprocess
from pathlib import Path

def deploy_script(path: Path, ssid, password, retry, ip, gateway):
    script = Path(__file__).parent.parent.parent / "wifi_setup_systemconf"

    # Kõik sisendid järjekorras
    inputs = [ssid, password, retry, "yes", gateway, ip]

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

def setup_conf(path: Path):
    script = Path(__file__).parent.parent.parent / "setup_systemconf" 
    result = subprocess.run(
        ["bash", str(script)],
        capture_output=True,
        text=True,
        cwd=path
    )
    return [result.stdout, result.stderr, result.returncode]