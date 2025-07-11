from bs4 import BeautifulSoup
import requests
from langchain.document_loaders import WebBaseLoader


def _scrape_metadata(url: str) -> dict:
    """Lightweight metadata extraction (title, author, published date)."""
    html = requests.get(url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")

    def _first(*queries):
        for q in queries:
            tag = soup.select_one(q)
            if tag:
                return tag.get("content") or tag.text.strip()
        return ""

    return {
        "title": _first("meta[property='og:title']", "title"),
        "author": _first("meta[name='author']"),
        "date": _first("meta[property='article:published_time']",
                       "meta[name='date']", "time"),
    }


def load_article(url: str):
    """Return (docs, metadata) ready for LangChain processing."""
    loader = WebBaseLoader(url)
    docs = loader.load()
    meta = _scrape_metadata(url)
    meta["url"] = url
    return docs, meta
