import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="AgriShield AI",
    page_icon="🌾",
    layout="wide",
)

# --------------------------
# CUSTOM CSS
# --------------------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#071A29,#102542,#1A365D);
}

.main{
    padding-top:1rem;
}

.big-title{
    font-size:42px;
    font-weight:700;
    color:white;
}

.subtitle{
    color:#B6C6D8;
    font-size:18px;
    margin-bottom:25px;
}

.status{
    background:#163A5F;
    padding:12px;
    border-radius:12px;
    color:white;
    border:1px solid #2F80ED;
}

.stChatMessage{
    border-radius:15px;
}

div[data-testid="stSidebar"]{
    background:#0D1B2A;
}

.sidebar-title{
    font-size:24px;
    font-weight:bold;
    color:white;
}

.sidebar-box{
    background:#163A5F;
    padding:15px;
    border-radius:15px;
    color:white;
}

.source-box{
    background:#14273d;
    border-radius:10px;
    padding:10px;
    margin-top:8px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# SIDEBAR
# --------------------------

with st.sidebar:

    st.markdown("<div class='sidebar-title'>🌾 AgriShield AI</div>",
                unsafe_allow_html=True)

    st.write("")

    st.markdown("""
<div class='sidebar-box'>

### Rice Pest Assistant

✅ Local AI

✅ RAG Powered

✅ Ollama + Llama 3.2

✅ FAISS Search

</div>
""", unsafe_allow_html=True)

    st.write("")

    st.info(
        """
### Sample Questions

• How to control stem borer?

• Symptoms of brown planthopper?

• How to prevent rice blast?

• Management of leaf folder?
"""
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --------------------------
# TITLE
# --------------------------

st.markdown("<div class='big-title'>🌾 AgriShield AI</div>",
            unsafe_allow_html=True)

st.markdown("<div class='subtitle'>AI-powered Rice Pest Management Assistant</div>",
            unsafe_allow_html=True)

st.markdown("""
<div class='status'>

🟢 Vector Database Loaded &nbsp;&nbsp;&nbsp;
🤖 Llama 3.2 Ready &nbsp;&nbsp;&nbsp;
📚 Agricultural Extension Documents Connected

</div>
""", unsafe_allow_html=True)

st.write("")

# --------------------------
# LOAD MODELS
# --------------------------

@st.cache_resource
def load_components():

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
        "vectorstore",
        embedding_model,
        allow_dangerous_deserialization=True
    )

    llm = ChatOllama(
        model="llama3.2",
        temperature=0.2
    )

    return db, llm


db, llm = load_components()

# --------------------------
# CHAT HISTORY
# --------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------
# CHAT INPUT
# --------------------------

question = st.chat_input("Ask anything about rice pests...")

if question:

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Searching agricultural documents..."):

            docs = db.similarity_search(question, k=3)

            context = "\n\n".join(
                [doc.page_content for doc in docs]
            )

            prompt = f"""
You are an expert agricultural assistant.

Use ONLY the context provided below.

If the answer cannot be found, reply exactly:

"I could not find this information in the uploaded agricultural extension documents."

Context:
{context}

Question:
{question}

Answer using this format:

### 🌾 Pest

### 🔍 Symptoms

### 🛠 Management

### 🛡 Prevention
"""

            response = llm.invoke(prompt)

            answer = response.content

            st.markdown(answer)

            with st.expander("📚 View Sources"):

                shown = set()

                for doc in docs:

                    source = doc.metadata.get("source", "Unknown")

                    page = doc.metadata.get("page", 0) + 1

                    key = (source, page)

                    if key not in shown:

                        st.markdown(f"""
<div class='source-box'>

📄 <b>{source}</b><br>

Page <b>{page}</b>

</div>
""", unsafe_allow_html=True)

                        shown.add(key)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )