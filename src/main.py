import sys
import argparse
from dotenv import load_dotenv

from src.models.router import reason_with_llm, code_with_llm

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Local Autonomous Coding System")
    parser.add_argument("prompt", type=str, nargs="?", help="The task for the local agent.")
    parser.add_argument("--test-reason", action="store_true", help="Test the reasoning model.")
    parser.add_argument("--test-code", action="store_true", help="Test the coding model.")

    args = parser.parse_args()

    if args.test_reason:
        print("Testing Reasoning Model...")
        response = reason_with_llm("Why is the sky blue? Answer in one sentence.")
        print(f"Response: {response}")
        return

    if args.test_code:
        print("Testing Coding Model...")
        response = code_with_llm("Write a python function to add two numbers.")
        print(f"Response:\n{response}")
        return

    if args.prompt:
        print(f"Received task: {args.prompt}")
        print("Initializing agents... (Feature under construction)")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
