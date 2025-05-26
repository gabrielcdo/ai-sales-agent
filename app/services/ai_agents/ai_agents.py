from app.schemas.ai_agents import (
    State,
    Tool,
    ProspectMessageAnalysis,
    ProspectDetails,
    KnowledgeText,
    LLMOutput,
    ToolSelectionOutput,
)

from app.schemas.ai_agents import KnowledgeText
from langchain.chat_models import init_chat_model

import concurrent
from app.core.resources import Resources


def get_res():
    global _res_instance
    try:
        return _res_instance
    except NameError:
        _res_instance = Resources()
        return _res_instance


def fetch_prospect_details(state: State) -> State:
    """
    Busca informações do prospecto a partir do JSON de prospects carregado em Resources.
    Se não encontrar prospect_id, usa valores padrão.
    """
    res = get_res()

    details = None
    if state.prospect_id is not None:
        key = str(state.prospect_id)
        details = res.prospects.get(key)

    if not details:
        details = {
        }
    state.prospect_details = ProspectDetails(**details)
    return state


def fetch_knowledge_text(state: State) -> State:
    res = get_res()
    documents = res.documents
    index = res.faiss_index
    model = res.sentence_transformer_model
    # Trata caso None
    if state.prospect_message_analysis and state.prospect_message_analysis.intent:
        intents_str = ", ".join(state.prospect_message_analysis.intent)
    else:
        intents_str = ""
    query = (
        f"{state.current_prospect_message.strip()} Intenções detectadas: {intents_str}"
    )
    query_embedding = model.encode([query])
    top_k = 3
    _, indices = index.search(query_embedding, top_k)
    retrieved_chunks = [documents[i] for i in indices[0]]
    combined_text = "\n\n---\n\n".join(retrieved_chunks)
    state.knowledge_text = KnowledgeText(text=combined_text)
    return state


tools = [
    Tool(
        name="fetch_prospect_details",
        description="Busca informações do prospecto na base de dados",
        func=fetch_prospect_details,
    ),
    Tool(
        name="fetch_knowledge_text",
        description="Busca informações relevantes na base de conhecimento",
        func=fetch_knowledge_text,
    ),
]


def run_initial_analysis(state: State):
    res = get_res()
    llm = init_chat_model(model="gpt-4o-mini", temperature=0.0)
    llm = llm.with_structured_output(ProspectMessageAnalysis)
    initial_analysis_prompt = res.opik_client.get_prompt(
        name="initial_analysis_prompt"
    ).format(
        conversation_history=state.conversation_history,
        current_prospect_message=state.current_prospect_message,
    )
    state.prospect_message_analysis = llm.invoke(initial_analysis_prompt)
    return state


def tools_selection(state: State) -> State:
    res = get_res()
    tools_names = [tool.name + ": " + tool.description for tool in state.tools]
    tools_selection_prompt = res.opik_client.get_prompt(
        name="tools_selection_prompt"
    ).format(
        conversation_history=state.conversation_history,
        prospect_message_analysis=state.prospect_message_analysis,
        tools_names=tools_names,
    )
    llm = init_chat_model(model="gpt-4o-mini", temperature=0.0)
    llm = llm.with_structured_output(ToolSelectionOutput)
    state.tools_needed = llm.invoke(tools_selection_prompt).tools
    return state


def parallel_tools_execution(state: State) -> State:
    if not state.tools_needed:
        return state

    tools_to_run = [tool for tool in state.tools if tool.name in state.tools_needed]

    def call_tool(tool: Tool) -> State:
        return tool.func(state)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(call_tool, tools_to_run))

    for result in results:
        if result.knowledge_text is not None:
            state.knowledge_text = result.knowledge_text
        if result.prospect_details is not None:
            state.prospect_details = result.prospect_details

    return state


def synthesize_results(state: State) -> State:
    res = get_res()
    llm = init_chat_model(
        model="gpt-4o-mini",
        temperature=0.0,
    )
    llm = llm.with_structured_output(LLMOutput)
    synthesis_prompt = res.opik_client.get_prompt(name="synthesis_prompt").format(
        conversation_history=state.conversation_history,
        prospect_message_analysis=state.prospect_message_analysis,
        current_prospect_message=state.current_prospect_message,
        prospect_details=(
            "Dados do prospecto: " + str(state.prospect_details)
            if state.prospect_details
            else ""
        ),
        knowledge_text=(
            "Texto da base de conhecimento: " + state.knowledge_text.text
            if state.knowledge_text
            else ""
        ),
    )
    state.llm_output = llm.invoke(synthesis_prompt)
    return state
