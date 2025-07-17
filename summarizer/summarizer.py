from __future__ import annotations
from pathlib import Path
from typing import Literal

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from .fetcher import load_article

MODES = Literal["detailed", "tldr", "bullet", "executive", "action"]


def _base_summary(docs, llm):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " "],
    )
    doc_chunks = splitter.split_documents(docs)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    return chain.invoke({"input_documents": doc_chunks})["output_text"].strip()


def summarise(
    url: str,
    mode: MODES = "detailed",
    model: str = "gpt-4o-mini",
    temperature: float = 0.3,
) -> dict:
    """
    Summarise *url* in the requested mode. Returns dict with metadata + summary.
    """
    docs, meta = load_article(url)

    if not docs or not docs[0].page_content.strip():
        return {
            "summary": "⚠️ Article content could not be extracted.",
            "meta": meta,
            "content": "",
        }

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=temperature)

    if mode == "detailed":
        summary = _base_summary(docs, llm)
    else:
        base = _base_summary(docs, llm)

        prompts = {
            "tldr": f"Give a one‑sentence TL;DR for the following:\n\n{base}",
            "bullet": f"Convert the text below into 5–7 concise bullet points:\n\n{base}",
            "executive": (
                f"Rewrite the text below as an executive summary: "
                f"high‑level insights in 3–5 bullets.\n\n{base}"
            ),
            "action": (
                f"List concrete action items a reader could take based on "
                f"the following summary:\n\n{base}"
            ),
        }

        summary = llm.invoke(prompts[mode]).content.strip()

    return {
        "summary": summary,
        "meta": meta,
        "content": docs[0].page_content,
    }


def summarise_text(
    text: str,
    mode: MODES = "detailed",
    model: str = "gpt-4o-mini",
    temperature: float = 0.3,
) -> dict:
    """
    Summarise raw text (e.g., extracted from a PDF). Returns summary dict.
    """
    if not text.strip():
        return {
            "summary": "⚠️ Provided text is empty.",
            "meta": {},
            "content": "",
        }

    docs = [Document(page_content=text)]

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=temperature)

    if mode == "detailed":
        summary = _base_summary(docs, llm)
    else:
        base = _base_summary(docs, llm)

        prompts = {
            "tldr": f"Give a one‑sentence TL;DR for the following:\n\n{base}",
            "bullet": f"Convert the text below into 5–7 concise bullet points:\n\n{base}",
            "executive": (
                f"Rewrite the text below as an executive summary: "
                f"high‑level insights in 3–5 bullets.\n\n{base}"
            ),
            "action": (
                f"List concrete action items a reader could take based on "
                f"the following summary:\n\n{base}"
            ),
        }

        summary = llm.invoke(prompts[mode]).content.strip()

    return {
        "summary": summary,
        "meta": {},
        "content": text,
    }


