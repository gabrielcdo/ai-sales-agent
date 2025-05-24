from fastapi import APIRouter

from typing import Dict

router = APIRouter()
from app.schemas.ai_agents import State
from app.services.ai_agents.ai_agents import tools

from opik.integrations.langchain import OpikTracer
import opik
import os
from app.core.resources import Resources
from app.services.ai_agents.graph import MainAgentGraph
# os.environ["OPIK_BASE_URL"] = "http://opik-frontend-1:5173/api"
# # OPIK_URL_OVERRIDE same
# os.environ["OPIK_URL_OVERRIDE"] = "http://opik-frontend-1:5173/api"
# os.environ["OPIK_API_KEY"] = "opik_api_key"
# os.environ["OPIK_URL_OVERRIDE"] = 'http://opik_default:5173/api'
from typing import Optional


graph = MainAgentGraph().agent_graph
opik_tracer = OpikTracer(graph=graph.get_graph(xray=True))

@router.post(
    "/process_message",
    response_model=str,
)
def process_message(
    conversation_history: Dict[str, str],
    current_prospect_message: str,
    prospect_id: Optional[int] = None,
):
    
    print(conversation_history)
    initial_state = State(
        prospect_id=123,
        tools=tools,
        conversation_history=[
            {
                "role": "user",
                "content": "Olá, recebi a proposta mas tenho dúvidas sobre a integração com Salesforce.",
            },
            {
                "role": "assistant",
                "content": "Claro, posso ajudar com isso. Qual aspecto da integração você gostaria de entender melhor?",
            },
        ],
        current_prospect_message="Quero saber se o sistema de vocês permite integração com Salesforce e Slack.",
    )

    initial_state.conversation_history.append(
        {
            "role": "user",
            "content": current_prospect_message,
        }
    )


    result = graph.invoke(initial_state, config={"callbacks": [opik_tracer]})
    new_state = State(**result)

    return new_state.llm_output.suggested_response_draft
