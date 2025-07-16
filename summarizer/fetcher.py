from bs4 import BeautifulSoup
import requests
from langchain.docstore.document import Document
from newspaper import Article


def _scrape_metadata(url: str) -> dict:
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
        "date": _first("meta[property='article:published_time']", "meta[name='date']", "time"),
    }


def load_article(url: str):
    article = Article(url)
    article.download()
    article.parse()

    meta = {
        "title": article.title,
        "author": ", ".join(article.authors),
        "date": str(article.publish_date) if article.publish_date else "",
        "url": url,
    }

    docs = [Document(page_content=article.text, metadata=meta)]
    return docs, meta

