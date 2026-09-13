import streamlit as st

from backend.retriever import Retriever
from backend.generator import generate_answer


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Software Error Evidence Assistant",
    page_icon="🔎",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .evidence-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# LOAD RETRIEVER
# --------------------------------------------------

@st.cache_resource
def load_retriever():

    return Retriever()


retriever = load_retriever()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🔎 Software Error Evidence Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Diagnose software errors using evidence retrieved from a
    local knowledge base.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("About")

    st.write(
        """
        This application uses Retrieval-Augmented Generation (RAG)
        to retrieve relevant troubleshooting evidence before
        generating an answer.
        """
    )

    st.divider()

    st.subheader("Technologies")

    st.write("• Python")
    st.write("• FAISS")
    st.write("• Sentence Transformers")
    st.write("• Ollama")
    st.write("• Llama 3.2")

    st.divider()

    st.subheader("Supported knowledge base")

    st.write("• Python")
    st.write("• Java")
    st.write("• JavaScript / Node.js")
    st.write("• Docker")


# --------------------------------------------------
# QUERY INPUT
# --------------------------------------------------

query = st.text_area(
    "Describe your software error",
    placeholder=(
        "Example: Node.js cannot find a module"
    ),
    height=120
)


search_button = st.button(
    "🔍 Analyze Error",
    type="primary"
)


# --------------------------------------------------
# PROCESS QUERY
# --------------------------------------------------

if search_button:

    if not query.strip():

        st.warning(
            "Please describe a software error first."
        )

        st.stop()

    with st.spinner("Searching knowledge base..."):

        results = retriever.search(
            query,
            top_k=3
        )

    if not results:

        st.warning(
            "No sufficiently relevant evidence was found "
            "in the knowledge base."
        )

        st.info(
            "Try describing the error more specifically "
            "or use an error supported by the current knowledge base."
        )

        st.stop()

    # --------------------------------------------------
    # RETRIEVAL SUMMARY
    # --------------------------------------------------

    best_result = results[0]

    st.subheader("Retrieved Evidence")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Evidence chunks",
            len(results)
        )

    with col2:

        st.metric(
            "Best similarity",
            f"{best_result['score']:.4f}"
        )

    with col3:

        st.metric(
            "Confidence",
            best_result["confidence"]
        )


    # --------------------------------------------------
    # GENERATE ANSWER
    # --------------------------------------------------

    with st.spinner("Generating grounded answer..."):

        answer = generate_answer(
            query,
            results
        )


    st.subheader("Answer")

    st.markdown(answer)


    # --------------------------------------------------
    # EVIDENCE
    # --------------------------------------------------

    st.subheader("Evidence Used")

    for i, result in enumerate(
        results,
        start=1
    ):

        metadata = result["metadata"]

        with st.expander(
            f"Evidence {i}: {metadata['error_type']}"
        ):

            st.write(
                f"**Technology:** "
                f"{metadata['technology']}"
            )

            st.write(
                f"**Source:** "
                f"{metadata['source']}"
            )

            st.write(
                f"**Similarity:** "
                f"{result['score']:.4f}"
            )

            st.write(
                f"**Confidence:** "
                f"{result['confidence']}"
            )

            st.markdown("**Retrieved text:**")

            st.code(
                result["text"],
                language="text"
            )