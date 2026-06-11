"""
Research Agent - Main FastAPI Application
Uses IBM Watson Machine Learning (Granite) + IBM Cloud Services
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

from services.granite_service import GraniteService
from services.search_service import SearchService
from services.citation_service import CitationService
from services.report_service import ReportService

app = FastAPI(
    title="Research Agent API",
    description="AI-powered research assistant using IBM Granite",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

granite = GraniteService()
search  = SearchService()
citation = CitationService()
report  = ReportService(granite)


# ── Request / Response Models ────────────────────────────────────────────────

class ResearchQuery(BaseModel):
    query: str
    max_results: Optional[int] = 10
    output_format: Optional[str] = "summary"   # summary | report | hypotheses

class SummarizeRequest(BaseModel):
    text: str
    style: Optional[str] = "academic"

class CitationRequest(BaseModel):
    title: str
    authors: List[str]
    year: int
    journal: Optional[str] = None
    url: Optional[str] = None
    format: Optional[str] = "APA"             # APA | MLA | IEEE

class ReportRequest(BaseModel):
    topic: str
    sections: Optional[List[str]] = None
    references: Optional[List[str]] = None


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Research Agent API is running", "model": "IBM Granite"}


@app.post("/api/research")
async def research(query: ResearchQuery):
    """
    Core endpoint: search literature + summarise with Granite.
    """
    try:
        papers = await search.search_papers(query.query, query.max_results)
        summaries = []
        for paper in papers:
            summary = await granite.summarize(paper["abstract"])
            summaries.append({**paper, "ai_summary": summary})

        if query.output_format == "hypotheses":
            hypotheses = await granite.generate_hypotheses(query.query, summaries)
            return {"query": query.query, "papers": summaries, "hypotheses": hypotheses}

        if query.output_format == "report":
            rpt = await report.generate(query.query, summaries)
            return {"query": query.query, "papers": summaries, "report": rpt}

        return {"query": query.query, "papers": summaries}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/summarize")
async def summarize(req: SummarizeRequest):
    """Summarize any text with IBM Granite."""
    try:
        result = await granite.summarize(req.text, style=req.style)
        return {"summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/hypotheses")
async def generate_hypotheses(query: ResearchQuery):
    """Generate research hypotheses for a given topic."""
    try:
        papers   = await search.search_papers(query.query, query.max_results)
        hyp      = await granite.generate_hypotheses(query.query, papers)
        return {"topic": query.query, "hypotheses": hyp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/citation")
async def format_citation(req: CitationRequest):
    """Format a citation in APA / MLA / IEEE."""
    try:
        cited = citation.format(
            title=req.title, authors=req.authors, year=req.year,
            journal=req.journal, url=req.url, fmt=req.format
        )
        return {"citation": cited, "format": req.format}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/report")
async def generate_report(req: ReportRequest):
    """Generate a full research report draft."""
    try:
        rpt = await report.generate_full(
            topic=req.topic,
            sections=req.sections,
            references=req.references
        )
        return {"topic": req.topic, "report": rpt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
def health():
    return {"status": "healthy", "granite": granite.is_ready()}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
