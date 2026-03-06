from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, END

# Define the state for our autonomous agent loop
class AgentState(TypedDict):
    task: str
    plan: list[str]
    code: str
    error: str | None
    iteration: int

def planner_node(state: AgentState) -> AgentState:
    print(f"Planning task: {state['task']}")
    # TODO: Connect to Architect Persona
    state['plan'] = ["Step 1", "Step 2"]
    return state

def executor_node(state: AgentState) -> AgentState:
    print("Executing plan...")
    # TODO: Connect to Developer Persona
    state['code'] = "def implemented(): pass"
    return state

def observer_node(state: AgentState) -> AgentState:
    print("Observing results...")
    # TODO: Connect to Tester Persona / subprocess run
    state['error'] = None # Example: Set this if tests fail
    return state

def router_node(state: AgentState) -> str:
    """Decides what to do next based on the state."""
    if state['error'] and state['iteration'] < 3:
        return "executor_node"
    return "end"

def build_graph():
    workflow = StateGraph(AgentState)
    
    # Define Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("observer", observer_node)

    # Define Edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", "observer")
    workflow.add_conditional_edges(
        "observer",
        router_node,
        {
            "executor_node": "executor",
            "end": END
        }
    )

    return workflow.compile()
