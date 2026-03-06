from crewai.tools import tool
import os

@tool("Read File")
def read_file(file_path: str) -> str:
    """Read the contents of a file given its absolute or relative path."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

@tool("Write File")
def write_file(file_path: str, content: str) -> str:
    """Write contents to a file. Overwrites the file if it exists."""
    try:
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing to file {file_path}: {str(e)}"
