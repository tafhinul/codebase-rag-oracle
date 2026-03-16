# 🤖 Codebase Oracle — AI-Powered Code Q&A Agent

> Ask questions about your own codebase in plain English and get intelligent, context-aware answers — powered by Google Gemini, LangGraph, and local vector search.

---

## 🧠 What Is This?

**Codebase Oracle** is a local RAG (Retrieval-Augmented Generation) agent that lets you **chat with your codebase**. Instead of manually reading through files to understand how something works, you simply ask — and the AI searches your code, retrieves the most relevant snippets, and explains them clearly.

It uses:
- 🔍 **Semantic search** to find relevant code based on meaning, not just keywords
- 🧩 **LangGraph ReAct Agent** that decides *when* to search and *how* to answer
- 💬 **Google Gemini** to generate beginner-friendly, accurate explanations
- 🌐 **Streamlit** for a clean, interactive chat UI

---

## 🏗️ Architecture

```
Your Codebase (.py files)
        │
        ▼
  [ ingest.py ]  ──► Chunks code by syntax (functions, classes)
        │
        ▼
  [ ChromaDB ]   ──► Stores vector embeddings locally
        │
        ▼
  [ agent.py ]   ──► LangGraph ReAct Agent
        │              ├── Tool: search_codebase (retrieves top-3 relevant chunks)
        │              └── LLM: Google Gemini (generates the answer)
        ▼
  [ app.py ]     ──► Streamlit Chat UI (with session memory)
```

**Embedding Model:** `all-MiniLM-L6-v2` (runs 100% locally, no API needed)  
**LLM:** `gemini-2.0-flash-lite` via Google AI Studio  
**Vector DB:** ChromaDB (persisted locally in `./chroma_db`)

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/tafhinul/codebase-rag-oracle.git
cd codebase-rag-oracle
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install langchain-community langchain-huggingface langchain-chroma \
            langchain-google-genai langchain-core langgraph \
            langchain-text-splitters streamlit python-dotenv
```

### 4. Set up your API key
Copy `.env.example` to `.env` and add your Gemini API key:
```bash
cp .env.example .env
```
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```
> Get a free key at [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 5. Add your codebase
Create a folder called `codebase_to_scan` and paste the Python project you want to explore:
```
codebase-rag-oracle/
├── codebase_to_scan/
│   └── your_project/
│       └── *.py files
```

### 6. Ingest your codebase (run once)
```bash
python ingest.py
```
This scans all `.py` files, splits them by function/class, generates embeddings, and saves to ChromaDB.

### 7. Launch the Streamlit app
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) and start asking questions!

---

## 💬 Example Questions You Can Ask

| Question | What it does |
|---|---|
| `"What libraries are used for PDF handling?"` | Finds all PDF-related imports and explains them |
| `"How is the password encryption implemented?"` | Locates encryption logic and explains the flow |
| `"What does the get_pass() function do?"` | Finds the function and gives a plain-English explanation |
| `"List all the external modules used in this project"` | Aggregates imports across all files |

---

## 📁 Project Structure

```
codebase-rag-oracle/
│
├── ingest.py          # Scans code, creates vector embeddings, saves to ChromaDB
├── retrieve.py        # CLI tool for raw semantic search (no LLM)
├── agent.py           # LangGraph ReAct Agent + Gemini LLM setup
├── app.py             # Streamlit chat UI
│
├── .env               # Your API key (NOT committed to git)
├── .env.example       # Template for .env
├── .gitignore         # Excludes .env, chroma_db/, .venv/, codebase_to_scan/
│
├── chroma_db/         # Auto-generated vector database (gitignored)
└── codebase_to_scan/  # Your project's code goes here (gitignored)
```

---

## 🛠️ Tech Stack

| Component | Library/Tool |
|---|---|
| **LLM** | Google Gemini (`gemini-2.0-flash-lite`) |
| **Agent Framework** | LangGraph (ReAct agent) |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` |
| **Vector Database** | ChromaDB |
| **LLM Orchestration** | LangChain |
| **Web UI** | Streamlit |
| **Language** | Python 3.11+ |

---

## ⚙️ How It Works (Under the Hood)

1. **Ingest phase** — `ingest.py` uses `GenericLoader` + `LanguageParser` to parse Python files by syntax (preserving function/class boundaries). `RecursiveCharacterTextSplitter` chunks the code intelligently, and `HuggingFaceEmbeddings` converts each chunk into a 384-dimensional vector saved to ChromaDB.

2. **Query phase** — When you ask a question, the LangGraph agent:
   - Decides to call the `search_codebase` tool
   - The tool runs a cosine similarity search in ChromaDB to retrieve the top 3 most relevant code snippets
   - These snippets are injected into the Gemini prompt as context
   - Gemini generates a clear, beginner-friendly explanation

3. **Memory** — The Streamlit UI maintains per-session chat history using `st.session_state`.

---

## 🔐 Security Notes

- Your API key is stored in `.env` which is **gitignored** — it will never be pushed to GitHub
- The `codebase_to_scan/` directory is also gitignored — your private code stays local
- ChromaDB data is stored locally and never sent anywhere except when a query is made to Gemini

---

## 📄 License

MIT License — feel free to use, modify, and share.

---

*Built with ❤️ using LangChain, LangGraph, and Google Gemini*
