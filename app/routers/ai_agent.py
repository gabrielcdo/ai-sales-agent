from fastapi import APIRouter

from typing import Dict
from typing import List
router = APIRouter()
from app.schemas.ai_agents import State
from app.schemas.ai_agents import LLMOutput
from app.services.ai_agents.ai_agents import tools

from opik.integrations.langchain import OpikTracer

from app.services.ai_agents.graph import MainAgentGraph

from typing import Optional


graph = MainAgentGraph().agent_graph
opik_tracer = OpikTracer(graph=graph.get_graph(xray=True))


@router.post(
    "/process_message",
    response_model=LLMOutput,
)
def process_message(
    current_prospect_message: str,
    prospect_id: Optional[int] = None,
    conversation_history: List[Dict[str, str]] = [],
):
    initial_state = State(
        prospect_id=prospect_id,
        tools=tools,
        conversation_history=conversation_history,
        current_prospect_message=current_prospect_message,
    )

    initial_state.conversation_history.append(
        {
            "role": "user",
            "content": current_prospect_message,
        }
    )

    result = graph.invoke(initial_state, config={"callbacks": [opik_tracer]})
    new_state = State(**result)

    return new_state.llm_output
