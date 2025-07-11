# 📰 Smart Summarizer

A command-line and API tool to summarize web articles using large language models. Easily fetch an article, generate summaries in various styles, and export them to Markdown, PDF, or even Notion.

## ✨ Features

* **Article Fetching:** Automatically pulls content from any public web article.
* **Multiple Summary Modes:**
    * `detailed`: A comprehensive summary of the article.
    * `tldr`: A concise, one-sentence "Too Long; Didn't Read" summary.
    * `bullet`: Key information presented as 5-7 bullet points.
    * `executive`: A summary tailored for executive-level understanding.
    * `action`: Actionable insights derived from the article.
* **Flexible Output:**
    * Print summaries directly to the console.
    * Save summaries as **Markdown (`.md`)** files.
    * Save summaries as **PDF (`.pdf`)** documents.
    * Export summaries directly to a **Notion page**.
* **API Integration:** Run as a FastAPI application for easy integration into other services.
* **LLM Agnostic (Configurable):** Supports Google Gemini out-of-the-box, with straightforward options to switch to OpenAI or even local models.

## 🚀 Getting Started

Follow these steps to set up and run the Smart Summarizer.

### Prerequisites

* Python 3.9+
* `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/amirsahi/AI-Summarizer.git](https://github.com/amirsahi/AI-Summarizer.git)
    cd smart-summarizer
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\Activate.ps1
    # On macOS/Linux:
    source ./.venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *If you encounter errors during installation (especially related to `numpy` or `langchain` conflicts), please refer to troubleshooting steps or ensure you have [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed for Windows.*

### API Keys and Configuration (`.env` file)

This project relies on API keys for language models and Notion integration.

1.  **Create a `.env` file** in the root directory of your project (the same directory as `cli.py` and `requirements.txt`).

2.  **Add your API keys to the `.env` file:**

    ```dotenv
    # Google Gemini API Key
    # Required for using Google's Gemini models
    GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"

    # Notion Integration Token
    # Required for exporting summaries to Notion
    # Get it from: [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
    NOTION_TOKEN="YOUR_NOTION_TOKEN_HERE"
    NOTION_PAGE_ID="YOUR_NOTION_PARENT_PAGE_ID_HERE" # The ID of the Notion page where new summaries will be added

    # Optional: OpenAI API Key (if you switch to OpenAI models)
    # Get it from: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
    ```
    * **Replace placeholders** (`YOUR_GEMINI_API_KEY_HERE`, etc.) with your actual keys and IDs.
    * **Google Gemini API Key:** You can obtain this from [Google AI Studio](https://aistudio.google.com/app). Note that the Gemini API has a free tier, but it also has usage limits (e.g., requests per minute). If you hit these limits, you may need to wait or upgrade your Google Cloud Project to a paid tier.
    * **Notion Integration Token:** Create a new internal integration at [Notion Integrations](https://www.notion.so/my-integrations). Grant it permissions to the parent page where you want the summaries to be created.
    * **Notion Parent Page ID:** Find this in the URL of your Notion page (e.g., `https://www.notion.so/yourworkspace/Your-Page-Title-**PAGE_ID_HERE**`).

### Choosing Your Language Model (`summarizer/summarizer.py`)

By default, the project is configured to use Google Gemini. If you want to use OpenAI or a different model, you'll need to make a small change in `summarizer/summarizer.py`.

1.  **Open `summarizer/summarizer.py`** in your code editor.

2.  **Locate the `summarise` function.** Inside this function, find the line where the `llm` object is initialized.

    **Current (Gemini):**
    ```python
    from langchain_google_genai import ChatGoogleGenerativeAI
    from .config import require_env # Ensure this is imported

    # ... inside summarise function ...
    llm = ChatGoogleGenerativeAI(model=model, temperature=temperature)
    ```

    **To switch to OpenAI (if you have `OPENAI_API_KEY` set):**
    ```python
    from langchain_openai import ChatOpenAI

    # ... inside summarise function ...
    llm = ChatOpenAI(model_name=model, temperature=temperature)
    ```
 
    **To use a Local LLM via Ollama (if you have Ollama installed and a model pulled):**
    ```python
    from langchain_community.chat_models import ChatOllama

    # ... inside summarise function ...
    llm = ChatOllama(model=model, temperature=temperature) # 'model' would be like "llama2" or "phi3"
    ```
    * You might need to adjust the `model` argument in `cli.py` or other entry points to match the Ollama model name (e.g., `--model llama2`).

## ⚙️ How to Run

### Command-Line Interface (CLI)

Use `cli.py` to summarize articles directly from your terminal.

```bash
python cli.py "YOUR_ARTICLE_URL_HERE" [OPTIONS]

### Example Usage:

* **Detailed summary to console:**
    ```bash
    python cli.py "[https://www.nature.com/articles/s41586-025-09341-z](https://www.nature.com/articles/s41586-025-09341-z)"
    ```
* **Bullet points summary, saved as Markdown:**
    ```bash
    python cli.py "[https://www.frontiersin.org/journals/water/articles/10.3389/frwa.2021.652100/full](https://www.frontiersin.org/journals/water/articles/10.3389/frwa.2021.652100/full)" --mode bullet --md my_summary.md
    ```
* **TL;DR summary, saved as PDF:**
    ```bash
    python cli.py "[https://example.com/a-long-article](https://example.com/a-long-article)" --mode tldr --pdf summary.pdf
    ```
* **Export to Notion:**
    ```bash
    python cli.py "[https://www.example.com/your-article](https://www.example.com/your-article)" --notion
    ```
* **Using a specific LLM model (e.g., `gemini-pro` for Gemini or `gpt-4` for OpenAI):**
    ```bash
    python cli.py "[https://www.example.com/your-article](https://www.example.com/your-article)" --model gemini-pro
    # Or for OpenAI (after switching the LLM initialization in summarizer.py)
    python cli.py "[https://www.example.com/your-article](https://www.example.com/your-article)" --model gpt-4-turbo
    ```

### CLI Options:

* `<url>` (positional argument): The URL of the web article to summarize.
* `-m`, `--mode <mode>`: Summary style. Choices: `detailed` (default), `tldr`, `bullet`, `executive`, `action`.
* `--md <FILE.md>`: Path to save the summary as a Markdown file.
* `--pdf <FILE.pdf>`: Path to save the summary as a PDF file.
* `--notion`: Export the summary to a new Notion page (requires `NOTION_TOKEN` and `NOTION_PARENT_PAGE_ID` in `.env`).
* `--model <model_name>`: Specify the language model to use (e.g., `gemini-1.5-flash`, `gpt-4o-mini`, `llama2` if using Ollama). Default is `gemini-1.5-flash` if you followed the Gemini setup.

### FastAPI Web API

You can run the summarizer as a local web API using Uvicorn.

1.  **Start the API server:**
    ```bash
    uvicorn api:app --reload --port 8000
    ```
2.  **Access the API:**
    * Open your browser to `http://127.0.0.1:8000/docs` to see the interactive API documentation (Swagger UI).
    * You can then make requests to the `/summarize` endpoint.

    **Example API Request (e.g., using `curl` or a tool like Postman/Insomnia):**
    ```bash
    curl -X 'GET' \
      '[http://127.0.0.1:8000/summarize?url=https%3A%2F%2Fwww.frontiersin.org%2Fjournals%2Fwater%2Farticles%2F10.3389%2Ffrwa.2021.652100%2Ffull&mode=bullet](http://127.0.0.1:8000/summarize?url=https%3A%2F%2Fwww.frontiersin.org%2Fjournals%2Fwater%2Farticles%2F10.3389%2Ffrwa.2021.652100%2Ffull&mode=bullet)' \
      -H 'accept: application/json'
    ```

### Streamlit Web App

You can also run a simple Streamlit web application for a user-friendly interface.

1.  **Start the Streamlit app:**
    ```bash
    streamlit run streamlit_app.py
    ```
2.  **Access the app:**
    * Your browser should automatically open to `http://localhost:8501`.

### ⚠️ Important Notes

* **API Quotas and Billing:** If you are using Google Gemini (or switch to OpenAI), be aware of their respective free tier limits and potential billing requirements. Repeatedly hitting rate limits will prevent the summarizer from working until your quota resets or you upgrade your plan.
* **Deprecation Warnings:** You might see deprecation warnings from LangChain. These indicate that certain parts of the library are being updated. While the code still functions, it's good practice to update your code to use the newer methods (e.g., `chain.invoke()` instead of `chain.run()`, and new import paths for `WebBaseLoader`). The `langchain_cli migrate` command can help automate some of these updates.
* **Long Articles:** Summarizing very long articles might consume more tokens and therefore be more prone to hitting API limits, or take longer to process, especially with local models.