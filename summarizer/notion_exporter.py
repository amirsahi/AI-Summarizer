from notion_client import Client
from typing import Mapping


def push_to_notion(summary: Mapping, token: str, parent_page_id: str):
    """
    Create a new Notion page under *parent_page_id* with the summary content.
    Requires an integration token with write access.
    """
    notion = Client(auth=token)

    notion.pages.create(
        parent={"page_id": parent_page_id},
        properties={
            "title": [
                {"text": {"content": summary["title"] or "Untitled summary"}}
            ]
        },
        children=[
            {"object": "paragraph", "paragraph": {"text": [
                {"type": "text", "text": {"content": f"URL: {summary['url']}"}}]}},
            {"object": "heading_2", "heading_2": {"text": [
                {"type": "text", "text": {"content": "Summary"}}]}},
            {"object": "paragraph", "paragraph": {"text": [
                {"type": "text", "text": {"content": summary["summary"]}}]}},
        ],
    )
