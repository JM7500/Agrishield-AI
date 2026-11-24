from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama


class RicePestAssistant:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.db = FAISS.load_local(
            "vectorstore",
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0.2,
            )

    def ask(self, question):

        docs = self.db.similarity_search_with_score(
            question,
            k=3
        )

        context = "\n\n".join(
            [doc.page_content for doc, score in docs]
        )

        prompt = f"""
You are an agricultural expert specializing ONLY in rice pest management.

Use ONLY the supplied context.

If the answer cannot be found, say:

"I could not find this information in the uploaded agricultural extension documents."

Context:
{context}

Question:
{question}

Answer in markdown.

Use headings.

Include:

🌾 Pest

🔍 Symptoms

🛠 Management

🛡 Prevention
"""

        response = self.llm.invoke(prompt)

        sources = []

        scores = []

        for doc, score in docs:

            sources.append({
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", 0) + 1,
                "content": doc.page_content
            })

            scores.append(score)

        return {
            "answer": response.content,
            "sources": sources,
            "scores": scores
        }