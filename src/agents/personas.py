from crewai import Agent

def create_architect_agent() -> Agent:
    return Agent(
        role='Software Architect',
        goal='Design robust, scalable, and efficient software systems.',
        backstory='You are a seasoned software architect with decades of experience designing high-performance systems. You think deeply about edge cases and structure before writing any code.',
        verbose=True,
        allow_delegation=False
    )

def create_developer_agent() -> Agent:
    return Agent(
        role='Backend Developer',
        goal='Implement software requirements efficiently and cleanly.',
        backstory='You are an expert Python and system developer. You write clean, well-tested, and well-documented code based on architectural blueprints.',
        verbose=True,
        allow_delegation=False
    )

def create_tester_agent() -> Agent:
    return Agent(
        role='Quality Assurance Engineer',
        goal='Identify edge cases and verify code functionality.',
        backstory='You are a meticulous QA engineer. You look for ways systems might break and write solid test cases to prevent them.',
        verbose=True,
        allow_delegation=False
    )
