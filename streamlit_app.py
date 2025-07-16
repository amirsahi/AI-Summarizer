import streamlit as st
from summarizer.summarizer import summarise, MODES
from summarizer.exporter import save_markdown, save_pdf
from summarizer.config import require_env
from summarizer.notion_exporter import push_to_notion

st.title("📰 Smart Summarizer")

url = st.text_input("Article URL")
mode = st.radio("Summary style", list(MODES.__args__), horizontal=True)
run = st.button("Summarize")

if run and url:
    with st.spinner("Crunching..."):
        result = summarise(url, mode=mode)
    st.subheader("summary")
    st.write(result)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.download_button("⬇️  Markdown", file_name="summary.md",
                              data=save_markdown(result, "temp.md").read_text()):
            st.success("Markdown ready!")
    with col2:
        if st.download_button("⬇️  PDF", file_name="summary.pdf",
                              data=open(save_pdf(result, "temp.pdf"), "rb").read()):
            st.success("PDF ready!")
    with col3:
        if st.button("📤 Send to Notion"):
            push_to_notion(
                result,
                token=require_env("NOTION_TOKEN"),
                parent_page_id=require_env("NOTION_PAGE_ID"),
            )
            st.success("Pushed to Notion!")
