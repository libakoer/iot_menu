import subprocess

# Käivitame bash skripti (näiteks "../deploy")
result = subprocess.run(
    ["bash", "../deploy"],   # või ["sh", "../deploy"]
    capture_output=True,
    text=True
)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
