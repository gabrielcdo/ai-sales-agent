
from langgraph.graph import StateGraph, START, END
from app.core.singleton import singleton
from app.schemas.ai_agents import State
from app.services.ai_agents.ai_agents import (
    run_initial_analysis,
    tools_selection,
    parallel_tools_execution,
    synthesize_results
)

from app.core.singleton import singleton

class MainAgentGraph:
    def __init__(self):
        self.agent_graph = self.build_graph()
        
    def build_graph(self):
        graph_builder = StateGraph(State)
        graph_builder.add_node(run_initial_analysis)
        graph_builder.add_node(tools_selection)
        graph_builder.add_node(parallel_tools_execution)
        graph_builder.add_node(synthesize_results)
        graph_builder.add_edge(START, "run_initial_analysis")
        graph_builder.add_edge("run_initial_analysis", "tools_selection")
        graph_builder.add_edge("tools_selection", "parallel_tools_execution")
        graph_builder.add_edge("parallel_tools_execution", "synthesize_results")
        graph_builder.add_edge("synthesize_results", END)

        graph = graph_builder.compile()
        
        return graph