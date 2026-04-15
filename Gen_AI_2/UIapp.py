import streamlit as st
import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RAG Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root tokens ── */
:root {
    --bg:          #0d0f14;
    --surface:     #13161e;
    --surface2:    #1a1e2a;
    --border:      #252a38;
    --accent:      #5b8af0;
    --accent2:     #a78bfa;
    --gold:        #e2b96f;
    --text:        #e8eaf2;
    --muted:       #6b7280;
    --user-bubble: #1c2236;
    --ai-bubble:   #141825;
    --radius:      14px;
}

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}
.stApp { background-color: var(--bg); }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'DM Serif Display', serif;
    color: var(--gold);
}

/* ── Title area ── */
.rag-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    color: var(--text);
    letter-spacing: -0.5px;
    margin-bottom: 0;
    line-height: 1.15;
}
.rag-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: var(--accent);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.2rem;
    margin-bottom: 1.5rem;
}

/* ── Status badge ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    padding: 4px 12px;
    border-radius: 999px;
    letter-spacing: 0.06em;
}
.status-ready   { background: #14281e; color: #4ade80; border: 1px solid #166534; }
.status-warning { background: #2a1f0e; color: #fb923c; border: 1px solid #92400e; }

/* ── Chat bubbles ── */
.chat-wrapper { display: flex; flex-direction: column; gap: 1rem; }

.user-msg-wrap {
    display: flex;
    justify-content: flex-end;
}
.user-msg {
    background: var(--user-bubble);
    border: 1px solid var(--border);
    border-radius: var(--radius) var(--radius) 4px var(--radius);
    padding: 0.85rem 1.1rem;
    max-width: 72%;
    font-size: 0.93rem;
    line-height: 1.55;
}

.ai-msg-wrap { display: flex; gap: 0.75rem; align-items: flex-start; }
.ai-avatar {
    flex-shrink: 0;
    width: 32px; height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
}
.ai-msg {
    background: var(--ai-bubble);
    border: 1px solid var(--border);
    border-radius: 4px var(--radius) var(--radius) var(--radius);
    padding: 0.85rem 1.1rem;
    max-width: 82%;
    font-size: 0.93rem;
    line-height: 1.65;
}
.ai-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 4px;
}

/* ── Sources expander ── */
.sources-chip {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    padding: 2px 10px;
    border-radius: 999px;
    background: #151c30;
    border: 1px solid var(--border);
    color: var(--muted);
    margin-right: 6px;
    margin-top: 4px;
}

/* ── Input bar ── */
.stTextInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(91,138,240,0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.2s, transform 0.15s;
}
.stButton > button:hover { opacity: 0.88; transform: translateY(-1px); }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--surface2);
    border: 1px dashed var(--border);
    border-radius: var(--radius);
    padding: 0.5rem;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Select / number inputs ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* ── Slider ── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Lazy imports (keeps startup fast) ─────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_core_libs():
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_mistralai import ChatMistralAI
    from langchain_core.prompts import ChatPromptTemplate
    return GoogleGenerativeAIEmbeddings, Chroma, ChatMistralAI, ChatPromptTemplate


# ── Build / load vector store ──────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_vectorstore(persist_dir: str):
    GoogleGenerativeAIEmbeddings, Chroma, _, _ = load_core_libs()
    embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model,
    )


def ingest_files(uploaded_files, persist_dir: str, chunk_size: int, chunk_overlap: int):
    """Ingest uploaded files into a fresh Chroma collection."""
    from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, Docx2txtLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    GoogleGenerativeAIEmbeddings, Chroma, _, _ = load_core_libs()

    docs = []
    with tempfile.TemporaryDirectory() as tmp:
        for f in uploaded_files:
            path = os.path.join(tmp, f.name)
            with open(path, "wb") as out:
                out.write(f.read())
            ext = Path(f.name).suffix.lower()
            if ext == ".pdf":
                loader = PyMuPDFLoader(path)
            elif ext in (".txt", ".md"):
                loader = TextLoader(path)
            elif ext in (".docx", ".doc"):
                loader = Docx2txtLoader(path)
            else:
                st.warning(f"Unsupported file type: {f.name}")
                continue
            docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(docs)

    embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_dir,
    )
    return len(chunks)


# ── RAG query ──────────────────────────────────────────────────────────────────
def rag_query(query: str, vectorstore, k: int, fetch_k: int, lambda_mult: float):
    _, _, ChatMistralAI, ChatPromptTemplate = load_core_libs()

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "fetch_k": fetch_k, "lambda_mult": lambda_mult},
    )

    llm = ChatMistralAI(model="mistral-small-2506")

    prompt = ChatPromptTemplate.from_messages([
        ("system",
        "You are a helpful AI assistant.\n\n"
        "Use ONLY the provided context to answer the question.\n\n"
        "If the answer is not present in the context, "
        'say: "I could not find the answer in the document."'),
        ("human", "Context:\n{context}\n\nQuestion:\n{question}"),
    ])

    docs = retriever.invoke(query)
    context = "\n\n".join(d.page_content for d in docs)
    final_prompt = prompt.invoke({"context": context, "question": query})
    response = llm.invoke(final_prompt)
    return response.content, docs


# ── Session state defaults ─────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []          # [{role, content, sources}]
if "vs_dir" not in st.session_state:
    st.session_state.vs_dir = "chroma-db"
if "vs_ready" not in st.session_state:
    st.session_state.vs_ready = os.path.isdir("chroma-db")


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")

    # ── Document ingestion ──
    st.markdown("### 📂 Knowledge Base")

    mode = st.radio(
        "Source",
        ["Use existing Chroma DB", "Upload new documents"],
        index=0,
    )

    if mode == "Upload new documents":
        uploaded = st.file_uploader(
            "Drop files here",
            type=["pdf", "txt", "md", "docx"],
            accept_multiple_files=True,
        )
        with st.expander("Chunking options", expanded=False):
            chunk_size    = st.slider("Chunk size",    256, 2048, 512, 64)
            chunk_overlap = st.slider("Chunk overlap", 0,    512,  64, 16)

        custom_dir = st.text_input("Persist directory", value="chroma-db-custom")

        if st.button("🔄 Ingest & Index", use_container_width=True):
            if not uploaded:
                st.warning("Please upload at least one file.")
            else:
                with st.spinner("Indexing documents…"):
                    try:
                        n = ingest_files(uploaded, custom_dir, chunk_size, chunk_overlap)
                        st.session_state.vs_dir   = custom_dir
                        st.session_state.vs_ready = True
                        get_vectorstore.clear()
                        st.success(f"✅ Indexed {n} chunks from {len(uploaded)} file(s)")
                    except Exception as e:
                        st.error(f"Ingestion failed: {e}")
    else:
        db_path = st.text_input("Chroma DB path", value="chroma-db")
        if st.button("🔌 Load DB", use_container_width=True):
            if os.path.isdir(db_path):
                st.session_state.vs_dir   = db_path
                st.session_state.vs_ready = True
                get_vectorstore.clear()
                st.success("✅ Vector store loaded")
            else:
                st.error("Directory not found.")

    st.markdown("---")
    st.markdown("### 🔎 Retrieval")
    k           = st.slider("Results (k)",       1,  10, 4)
    fetch_k     = st.slider("Candidates (fetch_k)", k, 30, 10)
    lambda_mult = st.slider("Diversity (λ)",     0.0, 1.0, 0.5, 0.05,
                            help="0 = max diversity, 1 = max relevance")

    st.markdown("---")
    if st.button("🗑 Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # ── Status ──
    st.markdown("---")
    if st.session_state.vs_ready:
        st.markdown('<span class="status-badge status-ready">● DB ready</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-warning">● No DB loaded</span>', unsafe_allow_html=True)


# ── Main area ──────────────────────────────────────────────────────────────────
st.markdown('<div class="rag-title">Document Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="rag-subtitle">Retrieval-Augmented Generation · Mistral × Gemini Embeddings</div>', unsafe_allow_html=True)

# ── Chat history ───────────────────────────────────────────────────────────────
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="user-msg-wrap"><div class="user-msg">{msg["content"]}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'''<div class="ai-msg-wrap">
                    <div class="ai-avatar">✦</div>
                    <div>
                        <div class="ai-label">Assistant</div>
                        <div class="ai-msg">{msg["content"]}</div>
                    </div>
                    </div>''',
                unsafe_allow_html=True,
            )
            # Source snippets
            if msg.get("sources"):
                with st.expander(f"📎 {len(msg['sources'])} source chunk(s)", expanded=False):
                    for i, doc in enumerate(msg["sources"], 1):
                        src = doc.metadata.get("source", "unknown")
                        page = doc.metadata.get("page", "")
                        label = f"{Path(src).name}" + (f" · p.{page+1}" if page != "" else "")
                        st.markdown(f'<span class="sources-chip">#{i} {label}</span>', unsafe_allow_html=True)
                        st.caption(doc.page_content[:350] + ("…" if len(doc.page_content) > 350 else ""))
    st.markdown("</div>", unsafe_allow_html=True)


# ── Input (chat_input only fires once per submission — no loop bug) ────────────
query = st.chat_input("Ask anything about your documents…")

if query and query.strip():
    if not st.session_state.vs_ready:
        st.error("⚠️ No knowledge base loaded. Use the sidebar to load or ingest documents.")
    else:
        st.session_state.messages.append({"role": "user", "content": query.strip()})

        with st.spinner("Retrieving & generating…"):
            try:
                vs = get_vectorstore(st.session_state.vs_dir)
                answer, sources = rag_query(
                    query.strip(), vs, k, fetch_k, lambda_mult
                )
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"❌ Error: {e}",
                    "sources": [],
                })

        st.rerun()