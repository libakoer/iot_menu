import subprocess


def deploy_script():

    result = subprocess.run(
        ["bash", "../deploy"],
        capture_output=True,
        text=True
    )

    return [result.stdout, result.stderr, result.returncode ]
