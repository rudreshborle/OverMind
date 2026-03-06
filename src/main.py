import sys
import argparse
from dotenv import load_dotenv

from src.models.router import reason_with_llm, code_with_llm
from src.orchestration.state_machine import build_graph

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
        print("Initializing autonomous agent workflow...")
        app = build_graph()
        
        # Initial State
        initial_state = {
            "objective": args.prompt,
            "iteration": 0
        }
        
        # Stream the execution
        print("\n--- Starting Execution ---")
        for output in app.stream(initial_state):
            # stream() yields dictionaries with node names as keys and state updates as values
            for key, value in output.items():
                print(f"Finished node: {key}")
        
        print("--- Execution Complete ---")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
