import os
import subprocess

from typing import Optional


def script_directory():
    return os.path.abspath(os.path.join(__file__, os.pardir))


def create_directory(directory: str):
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass


def run_required_process(arguments: list[str], cwd: Optional[str] = None):
    capture_output = True

    result = subprocess.run(arguments, cwd=cwd, capture_output=capture_output, text=True)

    if result.returncode != 0:
        if capture_output:
            print("stderr:")
            print(str(result.stderr))

            print("stdout:")
            print(str(result.stdout))

        raise Exception(
            f"running process `{arguments[0]}` failed with error code {result.returncode}")
