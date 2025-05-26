import pytest
from app.services.faiss_service import preprocess_kb


class TestSplitTextFaiss:
    def test_split_text_basic(self):
        text = "par1\n\npar2\n\npar3"
        result = preprocess_kb.split_text(text, max_length=10, overlap=0)
        assert isinstance(result, list)
        assert len(result) == 3
        assert result == ["par1", "par2", "par3"]

    def test_split_text_empty(self):
        result = preprocess_kb.split_text("", max_length=10, overlap=0)
        assert result == []
