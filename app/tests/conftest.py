import pytest

ILETRUS_ENEM_SCORES = [120, 120, 120, 120, 80]


@pytest.fixture(scope="session")
def essays():
    return ["Texto para teste"]


@pytest.fixture(scope="session")
def predict_response():
    return {
        "enem_responses": {
            "1609": {
                "scores": ILETRUS_ENEM_SCORES,
                "comments": [
                    'Seu texto apresenta uma estrutura sintática razoável, com a maioria das orações em ordem direta, o que facilita a compreensão. No entanto, observei alguns desvios gramaticais e ortográficos que podem ser corrigidos, por exemplo, você cometeu um desvio na palavra "idependente", em que a sugestão correta é "independente" pois a forma correta da palavra inclui a letra "n" após o "i" inicial, formando "independente". Um outro desvio cometido foi na palavra "politícos", em que a sugestão correta é "políticos" pois o acento agudo deve ser colocado na primeira sílaba "lí" e não na segunda "tí", de acordo com a acentuação correta da palavra. Sugiro revisar a ortografia e a acentuação das palavras para aprimorar ainda mais sua escrita na próxima atividade.',
                    "Olá! Parabéns pelo seu esforço em abordar um tema tão relevante como o direito de votar. Você fez um bom trabalho ao destacar a evolução do voto no Brasil, mencionando momentos históricos importantes, como as Diretas Já e o fim da ditadura militar, o que demonstra uma compreensão do contexto social. No entanto, percebo que a sua argumentação poderia ser mais aprofundada em relação ao uso de repertório. Por exemplo, você menciona a troca de favores no voto, mas poderia incluir dados ou exemplos concretos que evidenciem essa prática, como estatísticas sobre corrupção eleitoral ou citações de especialistas que discutem a importância do voto consciente. Para melhorar na próxima atividade, sugiro que você busque incluir mais informações que sustentem suas ideias, como dados, exemplos ou opiniões de especialistas, para enriquecer sua argumentação e torná-la mais convincente. Continue assim, sua dedicação é visível!",
                    "Você demonstrou uma boa capacidade de selecionar e relacionar argumentos ao abordar a importância do voto e sua evolução histórica no Brasil. A menção às lutas pela democracia e a transformação do voto ao longo do tempo são pontos positivos que mostram seu entendimento sobre o tema. No entanto, a organização dos argumentos poderia ser aprimorada, pois algumas ideias parecem desconectadas, como a transição entre a importância do voto e a crítica à sua desvalorização. Para melhorar, sugiro que você estruture seus argumentos de forma mais clara, talvez agrupando as informações sobre a evolução do voto em um parágrafo e as críticas à sua utilização em outro, assim você poderá defender seu ponto de vista de maneira mais eficaz.",
                    "Parabéns pelo seu esforço em utilizar recursos coesivos na sua redação! Você fez uso de conectivos como 'entretanto' e 'além de que', que ajudam a articular suas ideias e a dar fluidez ao texto. No entanto, percebi que há algumas repetições e falta de coesão em certos trechos. Por exemplo, a frase 'o voto foi introduzindo no início da república' poderia ser reformulada para melhorar a clareza, e a expressão 'na maioria dos casos' poderia ser mais bem conectada ao contexto anterior. Para aprimorar sua próxima redação, sugiro que você busque variar mais os conectivos e evite repetições, utilizando sinônimos ou reformulando as frases para que a leitura fique mais agradável e coesa.",
                    "Olá! Parabéns pelo seu esforço em abordar a importância do voto e a consciência cidadã. Você destacou bem a evolução do direito ao voto no Brasil, mencionando momentos históricos como as Diretas Já e a transição para o voto secreto, o que demonstra um bom entendimento do tema. No entanto, sua proposta de intervenção carece de alguns elementos essenciais. Por exemplo, você não especificou claramente quem deve agir para promover essa mudança, nem como isso deve ser feito. Além disso, seria interessante incluir um resultado esperado e um exemplo concreto que ilustre sua proposta. Para melhorar na próxima atividade, sugiro que você estruture sua proposta de intervenção seguindo os cinco elementos obrigatórios: defina claramente a ação, o agente, o meio, o efeito e o detalhamento. Isso tornará sua proposta mais completa e convincente. Continue assim, você está no caminho certo!",
                    "Sua redação apresenta uma boa introdução ao tema, destacando a importância histórica do direito de votar no Brasil, o que demonstra um bom conhecimento do contexto. Na competência 1, você se saiu bem, mas atente-se a alguns erros de digitação, como 'inico' que deveria ser 'início' e 'idependente' que é 'independente'. Na competência 2, você abordou o tema de forma relevante, mas poderia ter aprofundado mais a relação entre o voto e as transformações sociais, trazendo exemplos concretos. Na competência 3, sua argumentação é clara, mas a conexão entre as ideias poderia ser mais robusta. Na competência 4, você utilizou coesão, mas algumas transições entre os parágrafos podem ser melhoradas para facilitar a leitura. Por fim, na competência 5, sua proposta de intervenção carece de detalhes; seria interessante especificar quem seriam os agentes, quais ações concretas poderiam ser tomadas e quais efeitos esperados. Para a próxima redação, busque desenvolver mais a proposta de intervenção e revisar a estrutura argumentativa, garantindo que cada parte do texto se conecte de forma fluida.",
                ],
                "services_predict_time": 6.29,
                "generative_predict_time": 6.29,
            }
        },
        "gm_responses": None,
    }


@pytest.fixture(scope="session")
def spellchecker_api_return():
    return [
        {
            "text": "Texto para teste",
            "created": "2024-09-10 15:07:02.745449",
            "config": {"api_version": "v1", "preprocessor_version": "v1"},
            "spellchecker": [
                {
                    "message": "Todo início de parágrafo e início de período (depois do ponto, por exemplo) deve ser escrito com a primeira letra maiúscula.",
                    "errorCategory": "DG_INICIAL_MAIUSCULA",
                    "errorDescription": "Inicial maiúscula",
                    "examples": [
                        "Incorreto: eu gosto de comer pizza. ele gosta de comer chocolate",
                        "Correto: Eu gosto de comer pizza. Ele gosta de comer chocolate",
                    ],
                    "suggestions": ["O"],
                    "label": "Ortografia",
                    "description": "Leve em consideração que se refere a desvios na escritas das palavras, como trocas de letras, uso inadequado de maiúsculas e minúsculas, confusão entre palavras similares e supressão de letras.",
                    "weight": 7,
                    "ruleId": "rule_WordBeginning",
                    "typeError": "spellchecker",
                    "boundaries": [0, 1],
                    "text": "o",
                    "errorText": "o",
                    "lemma": "o",
                    "pos": "ART",
                    "paragraph": 0,
                    "paragraph_boundaries": [0, 1],
                    "start_char": 0,
                    "end_char": 1,
                }
            ],
        }
    ]


@pytest.fixture(scope="session")
def legra_api_return():
    return [
        [
            {
                "paragraphs_boundaries": [1284, 1298],
                "paragraph": 0,
                "start": 1284,
                "end": 1298,
                "error_text": "muito difíceis",
                "comment": 'O termo "muito", quando indica um advérbio de intensidade, é uma palavra invariável, combinado? ',
                "category": "DO_GRAFIA_CONFUSAO",
                "rule_id": 182,
                "rule_version": 1,
                "suggestions": [],
                "label": "Ortografia",
                "description": "Leve em consideração que se refere a desvios na escritas das palavras, como trocas de letras, uso inadequado de maiúsculas e minúsculas, confusão entre palavras similares e supressão de letras.",
                "weight": 7,
                "examples": [
                    {
                        "incorrect": "As coisas estão muitos caras.",
                        "correct": ["As coisas estão muito caras."],
                    },
                    {
                        "incorrect": "As coisas estão muitos caras.",
                        "correct": ["As coisas estão muito caras."],
                    },
                ],
            },
        ]
    ]
