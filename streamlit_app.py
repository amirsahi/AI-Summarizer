import streamlit as st
from summarizer.summarizer import summarise, MODES
from summarizer.exporter import save_markdown, save_pdf
from summarizer.config import require_env
from summarizer.notion_exporter import push_to_notion
from summarizer.summarizer import summarise_text
import fitz

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


def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

st.title("Smart Summarizer")

# Choose between URL or PDF upload
mode = st.radio("Choose input method", ["URL", "Upload PDF"])

if mode == "URL":
    url = st.text_input("Enter the article URL:")
    if st.button("Summarize URL"):
        try:
            from summarizer.summarizer import summarise
            result = summarise(url, mode="url")
            st.success("Summary:")
            st.write(result["summary"])
        except Exception as e:
            st.error(f"Failed to summarize URL: {e}")

elif mode == "Upload PDF":
    uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_pdf is not None:
        with st.spinner("Extracting text and summarizing..."):
            try:
                full_text = extract_text_from_pdf(uploaded_pdf)
                result = summarise_text(full_text)  # You should define this
                st.success("Summary:")
                st.write(result["summary"])
            except Exception as e:
                st.error(f"Failed to summarize PDF: {e}")