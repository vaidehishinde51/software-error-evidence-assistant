# 🔎 Software Error Evidence Assistant

A local Retrieval-Augmented Generation (RAG) application that helps developers troubleshoot software errors using evidence retrieved from a technical knowledge base.

Instead of asking an LLM to answer a software troubleshooting question directly, the system first retrieves relevant evidence from a local knowledge base and then uses that evidence to generate a grounded response.

The application is designed to reduce unsupported troubleshooting suggestions and make the evidence behind an answer transparent to the user.

---

## 🎯 Problem Statement

Developers frequently encounter software errors such as:

- `ModuleNotFoundError`
- `NullPointerException`
- `MODULE_NOT_FOUND`
- `NameError`
- Docker daemon errors
- Port allocation errors

Finding the correct solution often requires searching through documentation, Stack Overflow discussions, GitHub issues, and other technical resources.

A conventional LLM chatbot can provide a plausible solution, but its response may not be grounded in a specific source.

This project addresses that problem by building an **evidence-first software troubleshooting assistant**.

The system:

1. Accepts a developer's software error or question.
2. Searches a local technical knowledge base using semantic similarity.
3. Retrieves the most relevant evidence.
4. Provides the retrieved evidence to a local LLM.
5. Generates a troubleshooting response grounded in that evidence.
6. Shows the evidence and similarity scores to the user.

---

# ✨ Features

- 🔍 Semantic search for software errors
- 📚 Local technical knowledge base
- 🧩 Document chunking
- 🧠 Sentence Transformer embeddings
- ⚡ FAISS vector similarity search
- 🤖 Local LLM inference using Ollama
- 🦙 Llama 3.2 support
- 📌 Evidence-grounded responses
- 📊 Similarity scores
- 🏷️ Confidence labels
- 📖 Source and error-type display
- 🚫 Handling of unsupported queries
- 🧪 Retrieval evaluation using Recall@3
- 🌐 Streamlit web interface
- 💰 No paid APIs or subscriptions required

---

# 🏗️ System Architecture

```text
                         USER
                           |
                           v
                  +----------------+
                  |   Streamlit    |
                  |      UI        |
                  +-------+--------+
                          |
                          v
                  +----------------+
                  | User Error /    |
                  | Question       |
                  +-------+--------+
                          |
                          v
                  +----------------+
                  | Query          |
                  | Embedding      |
                  | Sentence       |
                  | Transformer    |
                  +-------+--------+
                          |
                          v
                  +----------------+
                  |     FAISS      |
                  | Vector Search  |
                  +-------+--------+
                          |
                          v
                  +----------------+
                  | Relevant       |
                  | Evidence       |
                  +-------+--------+
                          |
                          v
                  +----------------+
                  | Context        |
                  | Construction   |
                  +-------+--------+
                          |
                          v
                  +----------------+
                  | Ollama         |
                  | Llama 3.2      |
                  +-------+--------+
                          |
                          v
                  +----------------+
                  | Grounded       |
                  | Answer         |
                  +-------+--------+
                          |
                          v
                  +----------------+
                  | Evidence +     |
                  | Sources        |
                  +----------------+


                 KNOWLEDGE BASE PIPELINE

              TXT / Markdown / PDF
                       |
                       v
                Document Loader
                       |
                       v
                 Text Extraction
                       |
                       v
                    Chunking
                       |
                       v
              Sentence Transformer
                       |
                       v
                   Embeddings
                       |
                       v
                 FAISS Index
                       |
                       v
                  Metadata