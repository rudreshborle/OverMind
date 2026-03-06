import dspy
import os
from dotenv import load_dotenv

load_dotenv()

REASONING_MODEL = os.getenv("REASONING_MODEL", "qwen3")
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

# Configure DSPy to use the local language model for reasoning tasks
def setup_dspy_lm():
    local_lm = dspy.OllamaLocal(model=REASONING_MODEL, base_url=OLLAMA_API_BASE)
    dspy.settings.configure(lm=local_lm)

# Define a DSPy signature to optimize vague prompts into structured tasks
class PromptOptimizer(dspy.Signature):
    """Transforms a weak, vague prompt into a structured software engineering task."""
    
    vague_prompt = dspy.InputField(desc="A brief user request, for example 'improve my API'")
    structured_tasks = dspy.OutputField(desc="A detailed, markdown-formatted list of steps to execute the objective")

# The module that executes the signature
class TaskExpander(dspy.Module):
    def __init__(self):
        super().__init__()
        self.expand = dspy.Predict(PromptOptimizer)

    def forward(self, prompt: str):
        return self.expand(vague_prompt=prompt)

def run_optimizer(user_prompt: str) -> str:
    setup_dspy_lm()
    expander = TaskExpander()
    prediction = expander(user_prompt)
    return prediction.structured_tasks
