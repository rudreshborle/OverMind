import os
from dotenv import load_dotenv
from litellm import completion

# Load environment variables from .env
load_dotenv()

REASONING_MODEL = os.getenv("REASONING_MODEL", "ollama/qwen3")
CODING_MODEL = os.getenv("CODING_MODEL", "ollama/deepseek-coder")
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

def reason_with_llm(prompt: str, system_prompt: str = "You are an expert software architect.") -> str:
    """Uses the primary reasoning model to think through a problem."""
    response = completion(
        model=REASONING_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        api_base=OLLAMA_API_BASE
    )
    return response.choices[0].message.content

def code_with_llm(prompt: str, system_prompt: str = "You are an expert developer.") -> str:
    """Uses the coding model to generate or modify code."""
    response = completion(
        model=CODING_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        api_base=OLLAMA_API_BASE
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # Simple test script behavior for internal debugging
    print(f"Router configured to use {REASONING_MODEL} for reasoning.")
    print(f"Router configured to use {CODING_MODEL} for coding.")
