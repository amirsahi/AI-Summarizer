from fastapi import FastAPI, Query
from pydantic import BaseModel

from summarizer.summarizer import summarise, MODES

app = FastAPI(title="Smart Summarizer API")


class SummaryResponse(BaseModel):
    title: str
    author: str | None = None
    date: str | None = None
    url: str
    summary: str


@app.get("/summarize", response_model=SummaryResponse)
def summarize_endpoint(
    url: str = Query(..., description="Article URL"),
    mode: MODES = Query("detailed", description="Summary mode"),
):
    return summarise(url, mode=mode)
