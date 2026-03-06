import os
from interpreter import interpreter

# Configure open-interpreter to use local model logic if needed
# We can also just configure it through environment variables

def setup_interpreter():
    # If using local ollama with interpreter
    interpreter.llm.model = os.getenv("CODING_MODEL", "ollama/deepseek-coder")
    interpreter.llm.api_base = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
    
    # Auto-run commands if true, else require user confirmation
    auto_run = os.getenv("INTERPRETER_AUTO_RUN", "false").lower() == "true"
    interpreter.auto_run = auto_run

def execute_command(cli_goal: str):
    """Passes a high-level goal to open-interpreter to execute on the local machine."""
    setup_interpreter()
    print(f"Executing goal via Open Interpreter: {cli_goal}")
    response = interpreter.chat(cli_goal)
    return response

if __name__ == "__main__":
    # Test
    print("Interpreter tool loaded.")
