"""
Unit tests for CitationService and SearchService (no IBM key needed).
"""

import pytest
from backend.services.citation_service import CitationService


# ── Citation Tests ────────────────────────────────────────────────────────────

cs = CitationService()

def test_apa_single_author():
    result = cs.format("Deep Learning", ["Yann LeCun"], 2015, "Nature", fmt="APA")
    assert "LeCun" in result
    assert "2015" in result
    assert "Deep Learning" in result

def test_apa_multiple_authors():
    result = cs.format("BERT", ["Jacob Devlin", "Ming-Wei Chang"], 2019, fmt="APA")
    assert "Devlin" in result
    assert "Chang" in result

def test_mla_format():
    result = cs.format("Attention Is All You Need", ["Ashish Vaswani"], 2017, fmt="MLA")
    assert "Vaswani" in result
    assert '"Attention Is All You Need."' in result

def test_ieee_format():
    result = cs.format("GPT-3", ["Tom Brown", "Benjamin Mann"], 2020, fmt="IEEE")
    assert "Brown" in result
    assert "2020" in result

def test_unknown_format_falls_back_to_apa():
    result = cs.format("Test Paper", ["Alice"], 2024, fmt="CHICAGO")
    assert "Alice" in result or "2024" in result

def test_with_url():
    result = cs.format("X", ["A B"], 2020, url="https://arxiv.org/abs/2001.0001", fmt="APA")
    assert "https://arxiv.org" in result


# ── Search Tests (mocked) ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_search_returns_list(monkeypatch):
    from backend.services.search_service import SearchService

    async def fake_semantic(self, query, limit):
        return [{"title": "Mock Paper", "abstract": "...", "authors": [], "year": 2024,
                 "url": "", "citations": 0, "source": "mock", "doi": ""}]

    monkeypatch.setattr(SearchService, "_semantic_scholar", fake_semantic)
    svc     = SearchService()
    results = await svc.search_papers("neural networks", limit=1)
    assert isinstance(results, list)
    assert results[0]["title"] == "Mock Paper"
