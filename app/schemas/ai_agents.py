from typing import List, Literal
from pydantic import BaseModel
from typing import List, Dict, Optional, Any


class KeyEntities(BaseModel):
    product_names: List[str]
    features_mentioned: List[str]
    pain_points: List[str]


class ProspectMessageAnalysis(BaseModel):
    intent: List[
        Literal[
            "inquiry",
            "objection",
            "buying_signal",
            "clarification_request",
            "budget_discussion",
            "technical_question",
            "compare_competitor",
            "schedule_request",
            "irrelevant",
            "general_feedback",
        ]
    ]
    key_entities: KeyEntities
    sentiment: Literal["positive", "neutral", "negative"]


class ProspectDetails(BaseModel):
    past_interactions: List[str]
    lead_score: int
    company_size: int
    technologies: List[str]


class KnowledgeText(BaseModel):
    text: str

class LLMOutput(BaseModel):
    detailed_analysis: str
    suggested_response_draft: str
    internal_next_steps: List[str]
    tool_usage_log: List[str]
    confidence_score: float
    reasoning_trace: str


class ToolSelectionOutput(BaseModel):
    tools: List[str]


class Tool(BaseModel):
    name: str
    description: str
    func: Any


# Define state structure
class State(BaseModel):
    prospect_id: Optional[int] = (None,)

    tools: List[Tool] = []
    conversation_history: List[Dict[str, str]] = []
    current_prospect_message: str = ""

    # ouput of the analysis
    prospect_message_analysis: Optional[ProspectMessageAnalysis] = None

    # chosen tools
    tools_needed: Optional[List[str]] = []

    prospect_details: Optional[ProspectDetails] = None

    knowledge_text: Optional[KnowledgeText] = None

    llm_output: Optional[LLMOutput] = None
