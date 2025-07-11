#!/usr/bin/env python3
from pathlib import Path
import argparse

from summarizer.config import require_env
from summarizer.summarizer import summarise, MODES
from summarizer.exporter import save_markdown, save_pdf
from summarizer.notion_exporter import push_to_notion


def main():
    p = argparse.ArgumentParser(prog="smart‑summarizer",
                                description="Summarise any web article with multiple output modes.")
    p.add_argument("url")
    p.add_argument("-m", "--mode", choices=MODES.__args__, default="detailed",
                   help="Summary style (default: detailed)")
    p.add_argument("--md", metavar="FILE.md", help="write Markdown here")
    p.add_argument("--pdf", metavar="FILE.pdf", help="write PDF here")
    p.add_argument("--notion", action="store_true", help="export to Notion page")
    p.add_argument("--model", default="gpt-4o-mini", help="OpenAI model")
    args = p.parse_args()

    summary = summarise(args.url, mode=args.mode, model=args.model)
    print("\n— SUMMARY —\n")
    print(summary["summary"])

    if args.md:
        save_markdown(summary, args.md)
        print(f"✓ Markdown saved → {args.md}")
    if args.pdf:
        save_pdf(summary, args.pdf)
        print(f"✓ PDF saved → {args.pdf}")
    if args.notion:
        push_to_notion(
            summary,
            token=require_env("NOTION_TOKEN"),
            parent_page_id=require_env("NOTION_PAGE_ID"),
        )
        print("✓ Posted to Notion")


if __name__ == "__main__":
    main()
