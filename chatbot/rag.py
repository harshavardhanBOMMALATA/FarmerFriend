import chromadb
import os

from pathlib import Path

from groq import Groq

from sentence_transformers import (
    SentenceTransformer
)


BASE_DIR = Path(__file__).resolve().parent.parent


model = None


client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_db")
)

collection = client.get_collection(
    "paddy_knowledge"
)


groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_paddy_bot(question, history):

    global model

    if model is None:

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    conversation = ""

    for item in history:

        conversation += f"""
User: {item['question']}
Assistant: {item['answer']}
"""

    query_embedding = model.encode(
        question
    )

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=3,
        include=[
            "documents",
            "distances"
        ]
    )

    documents = results["documents"][0]
    distances = results["distances"][0]

    context = "\n".join(
        documents
    )

    use_kb = False

    if distances:

        best_distance = distances[0]

        if best_distance < 1.0:

            use_kb = True

    if use_kb:

        prompt = f"""
You are a Paddy Agriculture Expert.

Previous Conversation:
{conversation}

Knowledge Base Context:
{context}

Current Question:
{question}

Instructions:
- Answer using the knowledge base context.
- Keep the answer clear and farmer-friendly.
- If relevant, provide practical recommendations.
"""

    else:

        prompt = f"""
You are a Paddy Agriculture Expert.

Previous Conversation:
{conversation}

Question:
{question}

The answer is not available in the knowledge base.

Use your general agricultural knowledge to answer.

Instructions:
- Give accurate and practical information.
- Keep the answer clear and farmer-friendly.
- If unsure, mention limitations.
"""

    response = groq_client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert agricultural assistant "
                    "specialized in paddy cultivation."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = (
        response
        .choices[0]
        .message
        .content
    )

    return answer
