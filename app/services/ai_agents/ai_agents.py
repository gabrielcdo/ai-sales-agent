from app.schemas.ai_agents import (
    State,
    Tool,
    ProspectMessageAnalysis,
    ProspectDetails,
    KnowledgeText,
    LLMOutput,
    ToolSelectionOutput,
)
import json

from app.schemas.ai_agents import KnowledgeText
from langchain.chat_models import init_chat_model

import concurrent
from app.core.resources import Resources

res = Resources()


def fetch_prospect_details(state: State) -> ProspectDetails:
    # Mocking a database fetch
    # details = data.get(state.prospect_id, {})
    details = {
        "past_interactions": ["E-mail de boas-vindas", "Demonstração agendada"],
        "lead_score": 85,
        "company_size": 50,
        "technologies": ["Salesforce", "Slack"],
    }
    state.prospect_details = ProspectDetails(**details)

    return state


def fetch_knowledge_text(state: State) -> State:

    documents = res.documents
    index = res.faiss_index

    # Modelo local
    # model = SentenceTransformer("all-MiniLM-L6-v2")
    model = res.sentence_transformer_model
    # Gera query baseada na mensagem e nas intenções detectadas
    intents_str = ", ".join(state.prospect_message_analysis.intent or [])
    query = (
        f"{state.current_prospect_message.strip()} Intenções detectadas: {intents_str}"
    )

    query_embedding = model.encode([query])

    # Busca top 3
    top_k = 3
    _, indices = index.search(query_embedding, top_k)
    retrieved_chunks = [documents[i] for i in indices[0]]
    combined_text = "\n\n---\n\n".join(retrieved_chunks)

    # Atualiza state
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
    llm = init_chat_model(model="gpt-4.1-nano", temperature=0.0)
    llm = llm.with_structured_output(ProspectMessageAnalysis)

    initial_analysis_prompt = res.opik_client.get_prompt(
        name="initial_analysis_prompt"
    ).format(
        conversation_history=state.conversation_history,
        current_prospect_message=state.current_prospect_message,
    )
    state.prospect_message_analysis = llm.invoke(initial_analysis_prompt)

    return state


# function that will be used to strategit tool invocation logic
def tools_selection(state: State) -> State:
    # based in a prompt
    tools_names = [tool.name + ": " + tool.description for tool in state.tools]
    # tools_selection_prompt = f"""
    #     Você é um assistente de pré-vendas responsável por selecionar ferramentas para responder a um prospect.
    #     Considere a análise da mensagem do prospect e o histórico da conversa e ferramentas disponíveis.
    #     Histórico da conversa:
    #     {conversation_history}
    #     Análise da mensagem do prospect:
    #     {prospect_message_analysis}
    #     Ferramentas disponíveis:
    #     {tools_names}

    #     Com base nisso, decida quais ferramentas são necessárias para responder ao prospect.
    #     Retorne uma dicionário com a chave "tools" e dentro uma lista de strings com os nomes das ferramentas necessárias. Se nenhuma ferramenta for necessária, essa lista deve ser vazia.
    #     """
    tools_selection_prompt = (
        res.opik_client.get_prompt(name="tools_selection_prompt")
        .format(
            conversation_history=state.conversation_history,
            prospect_message_analysis=state.prospect_message_analysis,
            tools_names=tools_names,
        )
    )
    llm = init_chat_model(model="gpt-4.1-nano", temperature=0.0)
    # print(f"Tools selection prompt: {tools_selection_prompt}")
    llm = llm.with_structured_output(ToolSelectionOutput)
    # state.tools_needed = llm.invoke(tools_selection_prompt).tools
    state.tools_needed = ["fetch_prospect_details", "fetch_knowledge_text"]
    # print(f"Tools needed: {state.tools_needed}")
    return state


def parallel_tools_execution(state: State) -> State:
    if not state.tools_needed:
        return state

    tools_to_run = [tool for tool in state.tools if tool.name in state.tools_needed]

    # Definimos uma função que será chamada em paralelo
    def call_tool(tool: Tool) -> State:
        return tool.func(state)

    # print(f"Tools to run: {tools_to_run}")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(call_tool, tools_to_run))

    # Merge dos resultados
    for result in results:
        if result.knowledge_text is not None:
            state.knowledge_text = result.knowledge_text
        if result.prospect_details is not None:
            state.prospect_details = result.prospect_details

    return state


def synthesize_results(state: State) -> State:
    # Aqui você pode combinar os resultados das ferramentas e gerar uma resposta final
    llm = init_chat_model(
        model="gpt-4.1-nano",
        temperature=0.0,
    )
    llm = llm.with_structured_output(LLMOutput)

    synthesis_prompt = f"""
        Você é um assistente de pré-vendas responsável por sintetizar informações coletadas de várias ferramentas.
        Histórico da conversa:
        {state.conversation_history}
        Análise da mensagem do prospect:
        {state.prospect_message_analysis}
        Mensagem atual do prospect:
        "{state.current_prospect_message}"

        Dados obtidos das ferramentas:
        {"Dados do prospecto: " + str(state.prospect_details) if state.prospect_details else ""}
        {"Texto da base de conhecimento: " + state.knowledge_text.text if state.knowledge_text else ""}
    
        Com base nisso, gere uma resposta estruturada com os seguintes campos:

        {{
            "detailed_analysis": "Um resumo do ententimento da mensagem do prospecto e contexto",
            "suggested_response_draft": "Um resposta concisa, contextualmente apropiada e útil para o prospecto.",
            "confidence_score": 0.95  # Uma pontuação de confiança estimada entre 0.0 e 1.0
        }}
        """
    synthesis_prompt = res.opik_client.get_prompt(
        name="synthesis_results_prompt"
    ).prompt
    state.llm_output = llm.invoke(synthesis_prompt)
    return state
