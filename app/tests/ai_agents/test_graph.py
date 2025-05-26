import pytest
from unittest.mock import patch, MagicMock
from app.services.ai_agents import graph


@patch("app.services.ai_agents.graph.StateGraph")
@patch("app.services.ai_agents.graph.run_initial_analysis")
@patch("app.services.ai_agents.graph.tools_selection")
@patch("app.services.ai_agents.graph.parallel_tools_execution")
@patch("app.services.ai_agents.graph.synthesize_results")
def test_build_graph_structure(
    mock_synth, mock_parallel, mock_tools_sel, mock_init, mock_stategraph
):
    # Mock StateGraph and its methods
    mock_graph_builder = MagicMock()
    mock_stategraph.return_value = mock_graph_builder
    mock_graph_builder.compile.return_value = "compiled_graph"

    agent_graph = graph.MainAgentGraph()
    # O grafo compilado deve ser atribuído
    assert agent_graph.agent_graph == "compiled_graph"
    # Verifica se os nós e arestas foram adicionados corretamente
    for method, args, kwargs in [
        (mock_graph_builder.add_node, (mock_init,), {}),
        (mock_graph_builder.add_node, (mock_tools_sel,), {}),
        (mock_graph_builder.add_node, (mock_parallel,), {}),
        (mock_graph_builder.add_node, (mock_synth,), {}),
        (mock_graph_builder.add_edge, (graph.START, "run_initial_analysis"), {}),
        (mock_graph_builder.add_edge, ("run_initial_analysis", "tools_selection"), {}),
        (
            mock_graph_builder.add_edge,
            ("tools_selection", "parallel_tools_execution"),
            {},
        ),
        (
            mock_graph_builder.add_edge,
            ("parallel_tools_execution", "synthesize_results"),
            {},
        ),
        (mock_graph_builder.add_edge, ("synthesize_results", graph.END), {}),
    ]:
        method.assert_any_call(*args, **kwargs)
    mock_graph_builder.compile.assert_called_once()
