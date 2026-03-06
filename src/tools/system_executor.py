import os
import subprocess
from crewai.tools import tool

@tool("System Executor")
def execute_command(cli_goal: str) -> str:
    """Executes a terminal or shell command on the local machine and returns the output.
    Useful for running python scripts, tests, or installing packages.
    """
    print(f"Executing system command: {cli_goal}")
    try:
        result = subprocess.run(
            cli_goal,
            shell=True,
            text=True,
            capture_output=True,
            timeout=120
        )
        output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}\n\nReturn Code: {result.returncode}"
        return output
    except Exception as e:
        return f"Failed to execute command. Error: {str(e)}"

if __name__ == "__main__":
    # Test
    print(execute_command.run("echo 'Hello World'"))
