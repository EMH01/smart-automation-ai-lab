"""Azure-first knowledge automation demo. Synthetic documents only.

The /ask endpoint is intentionally an authenticated-service integration exercise,
not a production payroll API. Protect ingress with Entra before real data.
"""
import logging
import os
import time
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

logger = logging.getLogger("hr_ai")
app = FastAPI(title="Azure-first Smart Automation Lab", version="0.1.0")

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)

class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    trace_id: str
    latency_ms: int

def retrieve(question: str) -> list[dict]:
    """Retrieve from the selected Azure AI Search index."""
    from src.search.retrieval import search_documents

    return search_documents(question)



