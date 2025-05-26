# Create Prompts

from typing import List
import pandas as pd

from opik import Opik

# Inicializa o cliente (certifique-se de estar autenticado se necessário)
client = Opik(use_local=True)

# Cria ou obtém o dataset
initial_analysis_dataset = client.get_or_create_dataset(name="run_initial_analysis")


initial_analysis_examples = [
    {
        "conversation_history": "Prospect: Olá, vi que vocês trabalham com automação de vendas. Gostaria de entender melhor.",
        "current_prospect_message": "A IA de vocês funciona com o RD Station?",
        "expected_output": {
            "intent": "inquiry",
            "key_entities": {
                "product_names": ["Sailer AI"],
                "features_mentioned": ["integração com RD Station"],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "Prospect: O plano de vocês é mensal ou anual?",
        "current_prospect_message": "Achei um pouco caro.",
        "expected_output": {
            "intent": "objection",
            "key_entities": {
                "product_names": [],
                "features_mentioned": [],
                "pain_points": ["preço"],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "Gostaria de agendar uma call para saber mais.",
        "expected_output": {
            "intent": "schedule_request",
            "key_entities": {
                "product_names": [],
                "features_mentioned": [],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "Prospect: Vi que integram com WhatsApp.",
        "current_prospect_message": "Consigo integrar com Instagram também?",
        "expected_output": {
            "intent": "technical_question",
            "key_entities": {
                "product_names": [],
                "features_mentioned": ["integração com Instagram"],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "A proposta parece interessante.",
        "expected_output": {
            "intent": "buying_signal",
            "key_entities": {
                "product_names": [],
                "features_mentioned": [],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "Qual o diferencial da Sailer em relação à Leadster?",
        "expected_output": {
            "intent": "compare_competitor",
            "key_entities": {
                "product_names": ["Sailer AI", "Leadster"],
                "features_mentioned": [],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "Prospect: Achei a proposta interessante.",
        "current_prospect_message": "Só preciso entender melhor como o CRM automático funciona.",
        "expected_output": {
            "intent": "clarification_request",
            "key_entities": {
                "product_names": ["CRM automático"],
                "features_mentioned": ["preenchimento automático de CRM"],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "Só estou dando uma olhada mesmo.",
        "expected_output": {
            "intent": "irrelevant",
            "key_entities": {
                "product_names": [],
                "features_mentioned": [],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "Legal a proposta. Parabéns pelo trabalho!",
        "expected_output": {
            "intent": "general_feedback",
            "key_entities": {
                "product_names": [],
                "features_mentioned": [],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "Gostei da ideia de não precisar atualizar o CRM manualmente.",
        "expected_output": {
            "intent": "buying_signal",
            "key_entities": {
                "product_names": ["CRM automático"],
                "features_mentioned": ["atualização automática de CRM"],
                "pain_points": ["atualização manual"],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "Qual o valor do plano mais básico?",
        "expected_output": {
            "intent": "budget_discussion",
            "key_entities": {
                "product_names": [],
                "features_mentioned": ["plano básico"],
                "pain_points": ["preço"],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "A IA se adapta a diferentes segmentos de mercado?",
        "expected_output": {
            "intent": "inquiry",
            "key_entities": {
                "product_names": [],
                "features_mentioned": ["adaptação por segmento"],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "Parabéns pelo atendimento. Fui muito bem atendido.",
        "expected_output": {
            "intent": "general_feedback",
            "key_entities": {
                "product_names": [],
                "features_mentioned": ["atendimento"],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "A IA roda fora do horário comercial?",
        "expected_output": {
            "intent": "technical_question",
            "key_entities": {
                "product_names": [],
                "features_mentioned": ["funcionamento 24/7"],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "Já usamos Pipedrive aqui. Funciona junto?",
        "expected_output": {
            "intent": "technical_question",
            "key_entities": {
                "product_names": ["Pipedrive"],
                "features_mentioned": ["integração com Pipedrive"],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "A IA substitui o vendedor humano?",
        "expected_output": {
            "intent": "clarification_request",
            "key_entities": {
                "product_names": [],
                "features_mentioned": ["substituição de vendedor"],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "Já uso chatbot, não preciso de outro.",
        "expected_output": {
            "intent": "objection",
            "key_entities": {
                "product_names": ["chatbot"],
                "features_mentioned": [],
                "pain_points": ["redundância de ferramenta"],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "Consigo personalizar as mensagens da IA?",
        "expected_output": {
            "intent": "inquiry",
            "key_entities": {
                "product_names": [],
                "features_mentioned": ["personalização de mensagens"],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "Como funciona a integração com CRM?",
        "expected_output": {
            "intent": "clarification_request",
            "key_entities": {
                "product_names": [],
                "features_mentioned": ["integração com CRM"],
                "pain_points": [],
            },
        },
    },
    {
        "conversation_history": "",
        "current_prospect_message": "Tem como falar com alguém da equipe comercial?",
        "expected_output": {
            "intent": "schedule_request",
            "key_entities": {
                "product_names": [],
                "features_mentioned": ["atendimento humano"],
                "pain_points": [],
            },
        },
    },
]
initial_analysis_examples_df = pd.DataFrame(initial_analysis_examples)

initial_analysis_dataset.insert_from_pandas(dataframe=initial_analysis_examples_df)
#
