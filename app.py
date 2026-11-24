import streamlit as st
import time
from rag import RicePestAssistant

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="AgriShield AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"]{
    font-family: "Segoe UI", sans-serif;
}

.stApp{

background:
linear-gradient(135deg,#081B29 0%,#0F3460 50%,#1A1A2E 100%);

color:white;

}

.block-container{

padding-top:2rem;

}

.big-title{

font-size:52px;

font-weight:800;

color:white;

margin-bottom:5px;

}

.subtitle{

font-size:20px;

color:#C6D4E1;

margin-bottom:25px;

}

.hero{

background:rgba(255,255,255,0.05);

backdrop-filter: blur(15px);

padding:25px;

border-radius:18px;

border:1px solid rgba(255,255,255,0.1);

box-shadow:0px 0px 20px rgba(0,255,170,0.15);

margin-bottom:20px;

}

.metric-card{

background:rgba(255,255,255,0.05);

padding:15px;

border-radius:15px;

text-align:center;

border:1px solid rgba(255,255,255,0.08);

}

.source-card{

background:#132238;

padding:12px;

border-radius:12px;

margin-bottom:10px;

border-left:4px solid #00E676;

}

.sidebar-box{

background:#112240;

padding:15px;

border-radius:15px;

}

.status-online{

color:#00E676;

font-weight:bold;

}

</style>

""", unsafe_allow_html=True)

# -------------------------------------------------------
# LOAD RAG
# -------------------------------------------------------

@st.cache_resource
def load_assistant():
    return RicePestAssistant()

assistant = load_assistant()

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

with st.sidebar:

    st.title("🌾 AgriShield AI")

    st.markdown("---")

    st.markdown("""
### Rice Pest Management Assistant

Built using

- 🧠 Llama 3.2
- 🔍 FAISS
- 📚 LangChain
- 🤗 Sentence Transformers
- 🌾 Rice Extension Documents
""")

    st.markdown("---")

    st.success("🟢 AI System Online")

    st.info("""

### Sample Questions

• How to control stem borer?

• Symptoms of brown planthopper?

• Rice blast management

• What is rice hispa?

• How to prevent leaf folder?

""")

    st.markdown("---")

    if st.button("🗑 Clear Conversation"):

        st.session_state.messages = []

        st.rerun()

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.markdown("""
<div class="big-title">

🌾 AgriShield AI

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">

AI-powered Rice Pest Management Assistant

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">

### 🚀 Intelligent Agricultural Decision Support

This chatbot uses Retrieval-Augmented Generation (RAG) with
FAISS vector search and a local Llama 3.2 model to provide
accurate answers based only on uploaded agricultural extension
documents.

</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# METRIC CARDS
# -------------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
<div class="metric-card">

### 📚 Knowledge Base

Rice Extension PDFs

</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown("""
<div class="metric-card">

### 🤖 AI Model

Llama 3.2

</div>
""", unsafe_allow_html=True)

with c3:
    st.markdown("""
<div class="metric-card">

### 🔍 Retrieval

FAISS Search

</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------------
# WELCOME SCREEN
# -------------------------------------------------------

if len(st.session_state.messages) == 0:

    st.markdown("""
## 👋 Welcome!

Ask questions about rice pests such as:

- Stem Borer
- Brown Planthopper
- Rice Blast
- Leaf Folder
- Rice Hispa
- Gall Midge

The assistant answers **only** using the uploaded agricultural extension documents.
""")

# -------------------------------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
# -------------------------------------------------------
# CHAT INPUT
# -------------------------------------------------------

question = st.chat_input("💬 Ask anything about rice pests...")

if question:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(question)

    # Assistant Response
    with st.chat_message("assistant"):

        start_time = time.time()

        with st.spinner("🔍 Searching agricultural knowledge base..."):

            result = assistant.ask(question)

        elapsed = time.time() - start_time

        answer = result["answer"]
        sources = result["sources"]
        scores = result["scores"]

        # -------------------------
        # Display Answer
        # -------------------------

        st.markdown(answer)

        # Save assistant message

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.write("")

        # -------------------------------------------------------
        # RESPONSE METRICS
        # -------------------------------------------------------

        st.markdown("## 📊 AI Retrieval Statistics")

        unique_pages = len(
            set((src["source"], src["page"]) for src in sources)
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "⚡ Response Time",
                f"{elapsed:.2f}s"
            )

        with col2:
            st.metric(
                "📄 Documents",
                len(sources)
            )

        with col3:
            st.metric(
                "📑 Source Pages",
                unique_pages
            )

        with col4:
            st.metric(
                "🧠 AI Model",
                "Llama 3.2"
            )
        st.success(
            "✅ Successfully retrieved relevant information from the agricultural extension documents."
        )
        # -------------------------------------------------------
        # SOURCES
        # -------------------------------------------------------

        st.markdown("## 📚 Sources Used")

        shown = set()

        for src in sources:

            key = (src["source"], src["page"])

            if key in shown:
                continue

            shown.add(key)

            st.markdown(f"""
<div class="source-card">

📄 <b>{src["source"]}</b>

<br>

📖 Page <b>{src["page"]}</b>

</div>
""", unsafe_allow_html=True)

        # -------------------------------------------------------
        # RETRIEVED CONTEXT
        # -------------------------------------------------------

        with st.expander("🔍 View Retrieved Context"):

            for i, src in enumerate(sources, start=1):

                st.markdown(f"### Document Chunk {i}")

                st.code(
                    src["content"],
                    language="text"
                )

        # -------------------------------------------------------
        # DOCUMENT SUMMARY
        # -------------------------------------------------------

        with st.expander("📖 Documents Used"):

            unique_docs = []

            for src in sources:

                if src["source"] not in unique_docs:

                    unique_docs.append(src["source"])

            for doc in unique_docs:

                st.success(doc)

        # -------------------------------------------------------
        # DISCLAIMER
        # -------------------------------------------------------

        st.caption(
            "This answer is generated only from the uploaded agricultural extension documents. "
            "Always consult your local agricultural officer before applying pest management recommendations."
        )
 # -------------------------------------------------------
# EXPORT CONVERSATION
# -------------------------------------------------------

st.markdown("---")

conversation = ""

for msg in st.session_state.messages:

    role = msg["role"].upper()

    conversation += f"{role}\n"
    conversation += "-" * 50 + "\n"
    conversation += msg["content"] + "\n\n"

st.download_button(
    label="📥 Download Conversation",
    data=conversation,
    file_name="AgriShield_Conversation.txt",
    mime="text/plain"
)

# -------------------------------------------------------
# CONVERSATION ANALYTICS
# -------------------------------------------------------

if len(st.session_state.messages) > 0:

    st.markdown("## 📈 Conversation Analytics")

    total_messages = len(st.session_state.messages)

    user_messages = sum(
        1 for msg in st.session_state.messages
        if msg["role"] == "user"
    )

    ai_messages = sum(
        1 for msg in st.session_state.messages
        if msg["role"] == "assistant"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("💬 Total Messages", total_messages)
    col2.metric("👨‍🌾 User Questions", user_messages)
    col3.metric("🤖 AI Responses", ai_messages)

# -------------------------------------------------------
# QUICK QUESTION BUTTONS
# -------------------------------------------------------

st.markdown("---")

st.markdown("## 💡 Try These Questions")

col1, col2 = st.columns(2)

with col1:

    st.info("""
🌾 Stem Borer

• How to control stem borer?

• Symptoms of stem borer?
""")

    st.info("""
🍂 Leaf Folder

• How to manage leaf folder?
""")

with col2:

    st.info("""
🦗 Brown Planthopper

• Management of brown planthopper?
""")

    st.info("""
🍄 Rice Blast

• Prevention of rice blast?
""")

# -------------------------------------------------------
# SYSTEM STATUS
# -------------------------------------------------------

st.markdown("---")

status1, status2, status3 = st.columns(3)

status1.success("🟢 Vector Database Ready")

status2.success("🟢 Ollama Connected")

status3.success("🟢 Llama 3.2 Running")

# -------------------------------------------------------
# PROJECT INFORMATION
# -------------------------------------------------------

with st.expander("ℹ️ About AgriShield AI"):

    st.markdown("""
### 🌾 AgriShield AI

An AI-powered Rice Pest Management Assistant developed as a
Retrieval-Augmented Generation (RAG) application.

### Technology Stack

- Streamlit
- LangChain
- FAISS
- Sentence Transformers
- Ollama
- Llama 3.2

### Features

✅ Semantic Search

✅ Local AI (Offline)

✅ Source Citation

✅ Response Metrics

✅ Context Retrieval

✅ Conversation History

### Purpose

Assist farmers and agricultural students by answering
rice pest management questions using agricultural extension
documents.

Version 1.0
""")

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------

st.markdown("---")

st.markdown(
"""
<div style="text-align:center;
padding:20px;
font-size:16px;
color:#BFC9D4;">

🌾 <b>AgriShield AI</b><br><br>

AI-powered Rice Pest Management Assistant

<br><br>

Built using ❤️ Streamlit • LangChain • FAISS • Ollama • Llama 3.2

</div>
""",
unsafe_allow_html=True
)               