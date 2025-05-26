import pytest
from app.services.ai_agents import preprocess_kb


class TestSplitText:
    def test_split_text_basic(self):
        text = "par1\n\npar2\n\npar3"
        result = preprocess_kb.split_text(text, max_length=20)
        # Todos os parágrafos juntos cabem em um chunk só
        assert isinstance(result, list)
        assert len(result) == 1
        assert result == ["par1\n\npar2\n\npar3"]

    def test_split_text_long_paragraph(self):
        text = "a" * 1000
        result = preprocess_kb.split_text(text, max_length=500)
        # Um parágrafo muito longo deve ser um único chunk
        assert len(result) == 1
        assert result[0] == text

    def test_split_text_empty(self):
        result = preprocess_kb.split_text("", max_length=10)
        assert result == []

    def test_split_text_chunking(self):
        text = "a" * 200 + "\n\n" + "b" * 200 + "\n\n" + "c" * 200
        # max_length=300, cada parágrafo tem 200, então cada um vira um chunk
        result = preprocess_kb.split_text(text, max_length=300)
        assert len(result) == 3
        assert result[0] == "a" * 200
        assert result[1] == "b" * 200
        assert result[2] == "c" * 200
