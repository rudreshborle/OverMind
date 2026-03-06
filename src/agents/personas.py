import os
from dotenv import load_dotenv
from crewai import Agent, LLM

from src.tools.file_tools import read_file, write_file
from src.tools.system_executor import execute_command

load_dotenv()

# Prevent litellm from crashing when checking for OpenAI key on local models
os.environ["OPENAI_API_KEY"] = "NA"

# We specify litellm wrapper format natively used by CrewAI mapping to our loaded Env Vars
REASONING_MODEL = os.getenv("REASONING_MODEL", "ollama/qwen3")
CODING_MODEL = os.getenv("CODING_MODEL", "ollama/deepseek-coder")
BASE_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

architect_llm = LLM(model=REASONING_MODEL, base_url=BASE_URL)
developer_llm = LLM(model=CODING_MODEL, base_url=BASE_URL)

def create_architect_agent() -> Agent:
    return Agent(
        role='Software Architect',
        goal='Design robust, scalable, and efficient software systems.',
        backstory='You are a seasoned software architect with decades of experience designing high-performance systems. You think deeply about edge cases and structure before writing any code.',
        verbose=True,
        allow_delegation=False,
        llm=architect_llm,
        tools=[read_file]
    )

def create_developer_agent() -> Agent:
    return Agent(
        role='Backend Developer',
        goal='Implement software requirements efficiently and cleanly.',
        backstory='You are an expert Python and system developer. You write clean, well-tested, and well-documented code based on architectural blueprints.',
        verbose=True,
        allow_delegation=False,
        llm=developer_llm,
        tools=[read_file, write_file, execute_command]
    )

def create_tester_agent() -> Agent:
    return Agent(
        role='Quality Assurance Engineer',
        goal='Identify edge cases and verify code functionality.',
        backstory='You are a meticulous QA engineer. You look for ways systems might break and write solid test cases to prevent them.',
        verbose=True,
        allow_delegation=False,
        llm=developer_llm, # Usually coding models are good at writing tests
        tools=[read_file, write_file, execute_command] # Needs to run tests
    )
