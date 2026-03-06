from typing import TypedDict
from langgraph.graph import StateGraph, END
from crewai import Task, Crew

from src.agents.personas import create_architect_agent, create_developer_agent, create_tester_agent

# Define the state for our autonomous agent loop
class AgentState(TypedDict):
    objective: str
    plan: str
    code_output: str
    test_results: str
    error: str | None
    iteration: int

def planner_node(state: AgentState) -> AgentState:
    print(f"\n[Planner Node] Generating plan for: {state['objective']}")
    architect = create_architect_agent()
    
    task = Task(
        description=f"Create a step-by-step technical implementation plan for the following objective:\n{state['objective']}\n\nList the precise files to create/edit and the logical steps.",
        expected_output="A markdown formatted technical implementation plan.",
        agent=architect
    )
    
    crew = Crew(agents=[architect], tasks=[task], verbose=True)
    result = crew.kickoff()
    
    state['plan'] = str(result)
    state['iteration'] = state.get('iteration', 0)
    return state

def executor_node(state: AgentState) -> AgentState:
    print("\n[Executor Node] Writing code based on plan...")
    developer = create_developer_agent()
    
    task = Task(
        description=f"Execute the following implementation plan to achieve the objective:\n\nObjective: {state['objective']}\n\nPlan:\n{state['plan']}\n\nPrevious Errors (if any): {state.get('error', 'None')}\n\nUse your tools to write the code files.",
        expected_output="A summary of the files written and actions taken.",
        agent=developer
    )
    
    crew = Crew(agents=[developer], tasks=[task], verbose=True)
    result = crew.kickoff()
    
    state['code_output'] = str(result)
    return state

def observer_node(state: AgentState) -> AgentState:
    print("\n[Observer Node] Testing implemented codebase...")
    tester = create_tester_agent()
    
    task = Task(
        description=f"Review the implementation against the objective:\n\nObjective: {state['objective']}\n\nActions Taken:\n{state['code_output']}\n\nWrite and run tests using your system execution tools if possible. Verify the functionality. If there are profound errors preventing success, list them explicitly. If successful, state 'SUCCESS'.",
        expected_output="Test execution results and a final verdict (SUCCESS or detailed error trace).",
        agent=tester
    )
    
    crew = Crew(agents=[tester], tasks=[task], verbose=True)
    result = crew.kickoff()
    
    state['test_results'] = str(result)
    
    # Simple heuristic to determine if we need to loop back
    if "SUCCESS" in state['test_results'].upper():
        state['error'] = None
    else:
        state['error'] = state['test_results']
        
    state['iteration'] += 1
    return state

def router_node(state: AgentState) -> str:
    """Decides what to do next based on the state."""
    # Max 3 iterations to prevent infinite loops
    if state['error'] and state['iteration'] < 3:
        print(f"\n[Router] Errors detected. Routing back to Executor. (Iteration {state['iteration']}/3)")
        return "executor_node"
    
    print("\n[Router] Task complete or reached max iterations. Ending.")
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
