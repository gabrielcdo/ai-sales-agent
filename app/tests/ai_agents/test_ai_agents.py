import pytest
from unittest.mock import patch, MagicMock
from app.services.ai_agents import ai_agents
from app.schemas.ai_agents import (
    State,
    ProspectMessageAnalysis,
    ToolSelectionOutput,
    LLMOutput,
    KnowledgeText,
    ProspectDetails,
)


def test_pytest_sanity():
    assert True


class DummyState(State):
    pass


def make_state(**kwargs):
    # Helper para criar um State mínimo
    return DummyState(
        prospect_id=1,
        tools=[],
        conversation_history=[],
        current_prospect_message="msg",
        prospect_message_analysis=kwargs.get("prospect_message_analysis"),
        tools_needed=kwargs.get("tools_needed", []),
        prospect_details=kwargs.get("prospect_details"),
        knowledge_text=kwargs.get("knowledge_text"),
        llm_output=kwargs.get("llm_output"),
    )


@patch("app.services.ai_agents.ai_agents.ProspectDetails")
def test_fetch_prospect_details(mock_prospect_details):
    state = make_state()
    mock_prospect_details.return_value = MagicMock()
    result = ai_agents.fetch_prospect_details(state)
    assert hasattr(result, "prospect_details")
    mock_prospect_details.assert_called_once()


# Testa fetch_prospect_details com state incompleto
@patch("app.services.ai_agents.ai_agents.ProspectDetails")
def test_fetch_prospect_details_incomplete_state(mock_prospect_details):
    state = make_state(prospect_message_analysis=None)
    mock_prospect_details.return_value = MagicMock()
    result = ai_agents.fetch_prospect_details(state)
    assert hasattr(result, "prospect_details")


@patch("app.services.ai_agents.ai_agents.get_res")
def test_fetch_knowledge_text(mock_res):
    analysis = ProspectMessageAnalysis(
        intent=["inquiry"],
        key_entities={"product_names": [], "features_mentioned": [], "pain_points": []},
        sentiment="neutral",
    )
    state = make_state(prospect_message_analysis=analysis)
    mock_instance = MagicMock()
    mock_instance.documents = ["doc1", "doc2", "doc3"]
    mock_instance.faiss_index.search.return_value = (None, [[0, 1, 2]])
    mock_instance.sentence_transformer_model.encode.return_value = [[0.1, 0.2, 0.3]]
    mock_res.return_value = mock_instance
    result = ai_agents.fetch_knowledge_text(state)
    assert hasattr(result, "knowledge_text")
    assert isinstance(result.knowledge_text, KnowledgeText)


# Testa fetch_knowledge_text com state sem prospect_message_analysis
@patch("app.services.ai_agents.ai_agents.get_res")
def test_fetch_knowledge_text_no_analysis(mock_res):
    state = make_state(prospect_message_analysis=None)
    mock_instance = MagicMock()
    mock_instance.documents = ["doc1", "doc2", "doc3"]
    mock_instance.faiss_index.search.return_value = (None, [[0, 1, 2]])
    mock_instance.sentence_transformer_model.encode.return_value = [[0.1, 0.2, 0.3]]
    mock_res.return_value = mock_instance
    result = ai_agents.fetch_knowledge_text(state)
    assert hasattr(result, "knowledge_text")


@patch("app.services.ai_agents.ai_agents.init_chat_model")
@patch("app.services.ai_agents.ai_agents.get_res")
def test_run_initial_analysis(mock_res, mock_init_chat):
    state = make_state()
    mock_llm = MagicMock()
    mock_init_chat.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_llm
    mock_llm.invoke.return_value = MagicMock()
    mock_instance = MagicMock()
    mock_instance.opik_client.get_prompt.return_value = (
        "prompt {conversation_history} {current_prospect_message}"
    )
    mock_res.return_value = mock_instance
    result = ai_agents.run_initial_analysis(state)
    assert hasattr(result, "prospect_message_analysis")
    mock_llm.invoke.assert_called_once()


# Testa run_initial_analysis com erro no LLM
@patch("app.services.ai_agents.ai_agents.init_chat_model")
@patch("app.services.ai_agents.ai_agents.get_res")
def test_run_initial_analysis_llm_error(mock_res, mock_init_chat):
    state = make_state()
    mock_llm = MagicMock()
    mock_init_chat.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_llm
    mock_llm.invoke.side_effect = Exception("LLM error")
    mock_instance = MagicMock()
    mock_instance.opik_client.get_prompt.return_value = (
        "prompt {conversation_history} {current_prospect_message}"
    )
    mock_res.return_value = mock_instance
    with pytest.raises(Exception):
        ai_agents.run_initial_analysis(state)


@patch("app.services.ai_agents.ai_agents.init_chat_model")
@patch("app.services.ai_agents.ai_agents.get_res")
def test_tools_selection(mock_res, mock_init_chat):
    analysis = ProspectMessageAnalysis(
        intent=["inquiry"],
        key_entities={"product_names": [], "features_mentioned": [], "pain_points": []},
        sentiment="neutral",
    )
    state = make_state(
        prospect_message_analysis=analysis,
        tools=[MagicMock(name="t1", description="desc", spec=[])],
    )
    mock_llm = MagicMock()
    mock_init_chat.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_llm
    mock_llm.invoke.return_value = ToolSelectionOutput(tools=["t1"])
    mock_instance = MagicMock()
    mock_instance.opik_client.get_prompt.return_value = (
        "prompt {conversation_history} {prospect_message_analysis} {tools_names}"
    )
    mock_res.return_value = mock_instance
    result = ai_agents.tools_selection(state)
    assert hasattr(result, "tools_needed")
    assert result.tools_needed == ["t1"]
    mock_llm.invoke.assert_called_once()


# Testa tools_selection com tools vazios
@patch("app.services.ai_agents.ai_agents.init_chat_model")
@patch("app.services.ai_agents.ai_agents.get_res")
def test_tools_selection_empty_tools(mock_res, mock_init_chat):
    analysis = ProspectMessageAnalysis(
        intent=["inquiry"],
        key_entities={"product_names": [], "features_mentioned": [], "pain_points": []},
        sentiment="neutral",
    )
    state = make_state(prospect_message_analysis=analysis, tools=[])
    mock_llm = MagicMock()
    mock_init_chat.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_llm
    mock_llm.invoke.return_value = ToolSelectionOutput(tools=[])
    mock_instance = MagicMock()
    mock_instance.opik_client.get_prompt.return_value = (
        "prompt {conversation_history} {prospect_message_analysis} {tools_names}"
    )
    mock_res.return_value = mock_instance
    result = ai_agents.tools_selection(state)
    assert hasattr(result, "tools_needed")
    assert result.tools_needed == []


@patch("concurrent.futures.ThreadPoolExecutor")
def test_parallel_tools_execution(mock_executor):
    state = make_state(
        tools_needed=["t1", "t2"],
        tools=[
            MagicMock(
                name="t1", func=MagicMock(return_value=MagicMock(knowledge_text="kt"))
            ),
            MagicMock(
                name="t2", func=MagicMock(return_value=MagicMock(prospect_details="pd"))
            ),
        ],
    )
    mock_executor.return_value.__enter__.return_value.map.return_value = [
        MagicMock(knowledge_text="kt"),
        MagicMock(prospect_details="pd"),
    ]
    result = ai_agents.parallel_tools_execution(state)
    assert hasattr(result, "knowledge_text") or hasattr(result, "prospect_details")


# Testa parallel_tools_execution com tools_needed vazio
@patch("concurrent.futures.ThreadPoolExecutor")
def test_parallel_tools_execution_empty(mock_executor):
    state = make_state(tools_needed=[], tools=[])
    mock_executor.return_value.__enter__.return_value.map.return_value = []
    result = ai_agents.parallel_tools_execution(state)
    assert result is not None


@patch("app.services.ai_agents.ai_agents.init_chat_model")
@patch("app.services.ai_agents.ai_agents.get_res")
def test_synthesize_results(mock_res, mock_init_chat):
    analysis = ProspectMessageAnalysis(
        intent=["inquiry"],
        key_entities={"product_names": [], "features_mentioned": [], "pain_points": []},
        sentiment="neutral",
    )
    details = ProspectDetails(
        past_interactions=[], lead_score=0, company_size=0, technologies=[]
    )
    knowledge = KnowledgeText(text="texto")
    state = make_state(
        conversation_history=[{"role": "user", "content": "msg"}],
        prospect_message_analysis=analysis,
        current_prospect_message="msg",
        prospect_details=details,
        knowledge_text=knowledge,
    )
    mock_llm = MagicMock()
    mock_init_chat.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_llm
    mock_llm.invoke.return_value = LLMOutput(
        detailed_analysis="a",
        suggested_response_draft="b",
        internal_next_steps=[],
        tool_usage_log=[],
        confidence_score=1.0,
        reasoning_trace=None,
    )
    mock_instance = MagicMock()
    mock_instance.opik_client.get_prompt.return_value = "prompt {conversation_history} {prospect_message_analysis} {current_prospect_message} {prospect_details} {knowledge_text}"
    mock_res.return_value = mock_instance
    result = ai_agents.synthesize_results(state)
    assert hasattr(result, "llm_output")
    mock_llm.invoke.assert_called_once()


# Testa synthesize_results com erro no LLM
@patch("app.services.ai_agents.ai_agents.init_chat_model")
@patch("app.services.ai_agents.ai_agents.get_res")
def test_synthesize_results_llm_error(mock_res, mock_init_chat):
    analysis = ProspectMessageAnalysis(
        intent=["inquiry"],
        key_entities={"product_names": [], "features_mentioned": [], "pain_points": []},
        sentiment="neutral",
    )
    details = ProspectDetails(
        past_interactions=[], lead_score=0, company_size=0, technologies=[]
    )
    knowledge = KnowledgeText(text="texto")
    state = make_state(
        conversation_history=[{"role": "user", "content": "msg"}],
        prospect_message_analysis=analysis,
        current_prospect_message="msg",
        prospect_details=details,
        knowledge_text=knowledge,
    )
    mock_llm = MagicMock()
    mock_init_chat.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_llm
    mock_llm.invoke.side_effect = Exception("LLM error")
    mock_instance = MagicMock()
    mock_instance.opik_client.get_prompt.return_value = "prompt {conversation_history} {prospect_message_analysis} {current_prospect_message} {prospect_details} {knowledge_text}"
    mock_res.return_value = mock_instance
    with pytest.raises(Exception):
        ai_agents.synthesize_results(state)
