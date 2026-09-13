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

🧠 How the RAG Pipeline Works

1. Document Ingestion

Technical error documentation is placed inside:



data/raw/

The ingestion pipeline reads the supported documents and converts them into structured chunks.

Currently supported document formats include:

TXT

Markdown

PDF

2. Chunking

Large documents are divided into smaller meaningful pieces.

For this project, chunks represent specific software errors and their associated information.

Each chunk contains metadata such as:



source
file_type
document_path
technology
error_type

Example:



Technology:
JavaScript/Node.js

Error Type:
MODULE_NOT_FOUND

Source:
javascript_errors.txt

3. Embeddings

Each chunk is converted into a numerical vector using a Sentence Transformer model.

The project uses:



all-MiniLM-L6-v2

The model produces:



384-dimensional embeddings

This allows semantically similar queries and documents to be compared mathematically.

For example:



"Node.js cannot find a module"

can retrieve:



MODULE_NOT_FOUND

even though the wording is not exactly identical.

4. Vector Database

The generated embeddings are stored in a FAISS index.

FAISS performs efficient vector similarity search.

The current system uses the retrieved similarity score to determine how relevant a piece of evidence is to the user's query.

5. Retrieval

When a user submits a query:



Node.js cannot find a module

the query is converted into an embedding.

FAISS then searches for the most semantically similar chunks.

Example:



Query:
Node.js cannot find a module

Retrieved:

Error Type:
MODULE_NOT_FOUND

Technology:
JavaScript/Node.js

Similarity:
0.7982

6. Evidence Augmentation

The retrieved evidence is passed to the language model as context.

Instead of:



User Query → LLM → Answer

the system performs:



User Query
     |
     v
Retriever
     |
     v
Relevant Evidence
     |
     v
LLM
     |
     v
Grounded Answer

This is the core RAG architecture.

7. Generation

The project uses:



Ollama
    |
    └── Llama 3.2

The model runs locally rather than through a paid cloud API.

The generation step uses the retrieved evidence as the basis for the response.

8. Evidence Display

The application exposes the evidence used to generate the answer.

For each retrieved result, the user can see:

Error type

Technology

Source document

Similarity score

Confidence

Retrieved text

This makes the response more transparent and allows the user to inspect the information behind the answer.

📚 Current Knowledge Base

The initial knowledge base contains troubleshooting information for:

Python

ModuleNotFoundError

NameError

TypeError

IndexError

KeyError

Java

NullPointerException

ClassNotFoundException

ArrayIndexOutOfBoundsException

NumberFormatException

JavaScript / Node.js

MODULE_NOT_FOUND

TypeError

ReferenceError

SyntaxError

Docker

Permission denied

Port already allocated

Cannot connect to Docker daemon

No such file or directory

🛠️ Technologies Used

ComponentTechnology



Programming Language

Python

Embedding Model

all-MiniLM-L6-v2

Embedding Library

Sentence Transformers

Vector Database

FAISS

LLM

Llama 3.2

Local LLM Runtime

Ollama

PDF Processing

PyMuPDF

Web Interface

Streamlit

Evaluation

Custom Recall@3 evaluator

📁 Project Structure



software-error-evidence-assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
├── .gitignore
│
├── backend/
│   ├── __init__.py
│   ├── ingest.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── generator.py
│   └── rag_pipeline.py
│
├── data/
│   ├── raw/
│   │   ├── docker_errors.txt
│   │   ├── javascript_errors.txt
│   │   ├── java_errors.txt
│   │   └── python_errors.txt
│   │
│   └── processed/
│       └── chunks.json
│
├── vectorstore/
│   ├── faiss.index
│   └── metadata.json
│
└── evaluation/
    ├── test_queries.json
    └── evaluate_retrieval.py

⚙️ Installation

Prerequisites

Install:

Python 3.10+

Ollama

Git

No paid API subscription is required.

1. Clone the Repository



git clone <YOUR_GITHUB_REPOSITORY_URL>
cd software-error-evidence-assistant

2. Create a Virtual Environment

Windows:



python -m venv .venv

Activate it:



.venv\Scripts\activate

3. Install Python Dependencies



pip install -r requirements.txt

4. Verify Ollama

Check the installation:



ollama --version

Check installed models:



ollama list

The project currently uses:



llama3.2:latest

If it is not installed:



ollama pull llama3.2

▶️ Running the Project

Step 1 — Ingest Documents

Run:



python -m backend.ingest

Expected output:



==============================
INGESTION COMPLETE
==============================
Documents processed: 4
Total chunks: 17

Step 2 — Generate Embeddings

Run:



python -m backend.embeddings

Expected output:



Creating embeddings for 17 chunks...
Embedding dimension: 384

This creates:



vectorstore/faiss.index
vectorstore/metadata.json

Step 3 — Run the RAG Pipeline

For command-line testing:



python -m backend.rag_pipeline

Example:



Describe your software error:
> Node.js cannot find a module

The system retrieves evidence and generates a grounded answer.

Step 4 — Run the Web Application

Start Streamlit:



streamlit run app.py

The application will open in your browser.

🧪 Evaluation

The project contains a small manually labeled evaluation dataset:



evaluation/test_queries.json

The evaluator checks whether the expected error evidence appears within the top three retrieved results.

The metric used is:



Recall@3

Run:



python evaluation/evaluate_retrieval.py

Current evaluation result:



Correct retrievals: 8/8
Retrieval accuracy: 100.00%

This corresponds to:



Recall@3 = 100%

on the current eight-query evaluation dataset.

Note: This is a small manually constructed evaluation set and should not be interpreted as general-purpose retrieval accuracy.

🚫 Out-of-Knowledge Queries

The system is also designed to avoid producing evidence-backed troubleshooting advice when relevant evidence is not available.

For example:



How do I fix a Kubernetes CrashLoopBackOff error?

when Kubernetes documentation is not present in the knowledge base should result in no sufficiently relevant evidence being retrieved.

This is important because the goal of the project is not simply to generate an answer.

The goal is to generate an answer supported by retrieved evidence.

🔬 Example

Input



Node.js cannot find a module

Retrieved Evidence



Error Type:
MODULE_NOT_FOUND

Technology:
JavaScript/Node.js

Source:
javascript_errors.txt

Similarity:
0.7982

Generated Response



Error:
MODULE_NOT_FOUND

Likely cause:
The required package may not be installed,
the module path may be incorrect, or the
application may be running from an unexpected
directory.

Troubleshooting:
1. Check that the required package is installed.
2. Verify the module name and import path.
3. Check the current project directory.
4. Verify that the dependency is listed in package.json.

The response is generated using the retrieved evidence rather than relying only on the LLM's pretrained knowledge.

🧩 Important RAG Concepts Demonstrated

This project demonstrates the following fundamental RAG concepts:

Document Ingestion

Converting raw technical documents into usable data.

Chunking

Breaking documents into smaller retrieval units.

Embeddings

Representing text as numerical vectors.

Vector Search

Finding semantically similar documents.

Retrieval

Selecting relevant evidence for a query.

Context Augmentation

Providing retrieved evidence to the LLM.

Grounded Generation

Generating responses using retrieved evidence.

Similarity Thresholding

Avoiding weak or irrelevant retrievals.

Retrieval Evaluation

Measuring retrieval performance using Recall@3.

💡 Why This Project Uses Local Models

One of the project's requirements was to avoid paid subscriptions.

Therefore:



Embedding Model
      ↓
Runs locally

FAISS
      ↓
Runs locally

Llama 3.2
      ↓
Runs locally through Ollama

No paid LLM API is required.

This also makes the project useful for experimenting with RAG without incurring API costs.

🔐 Privacy

The application is designed to run locally.

User queries do not need to be sent to a third-party LLM API.

The knowledge base and vector store are also stored locally.

🚀 Future Improvements

Possible future extensions include:

Larger technical documentation collection

GitHub issue ingestion

Stack trace parsing

Code snippet analysis

Hybrid keyword + semantic retrieval

Reranking retrieved documents

Better chunking strategies

Conversation history

Multi-language programming support

Automated answer evaluation

More sophisticated confidence estimation

Kubernetes troubleshooting knowledge

Database error troubleshooting

Cloud infrastructure error troubleshooting

📈 Limitations

The current version has several limitations:

The knowledge base is relatively small.

Retrieval quality depends on the available documentation.

The evaluation dataset is small.

The system does not currently parse complete stack traces.

Generated answers are limited by the quality of retrieved evidence.

Confidence is based primarily on retrieval similarity rather than a calibrated probability.

These limitations provide clear directions for future improvements.

🎓 Learning Outcomes

By building this project, the following RAG concepts were implemented from scratch:

Data ingestion

Document processing

Chunking

Embedding generation

Vector indexing

Semantic retrieval

Similarity scoring

Retrieval evaluation

Context augmentation

Local LLM inference

Grounded generation

Evidence presentation

RAG application development