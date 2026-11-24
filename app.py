import streamlit as st
from dotenv import load_dotenv
import os

from src.pdf_processor import extract_pdf
from src.nlp_processor import analyze_text
from src.chunker import chunk_pages
from src.retriever import TfidfRetriever
from src.ai_engine import generate_summary, answer_question, explain_paper

load_dotenv()

st.set_page_config(page_title="ResearchMate", page_icon="📚", layout="wide")
st.title("📚 ResearchMate")
st.caption("An AI-powered research paper summarisation and learning assistant")

with st.sidebar:
    st.header("About")
    st.write("Upload a research-paper PDF to extract key information, explore NLP insights, and ask questions grounded in the document.")
    api_ready = bool(os.getenv("OPENAI_API_KEY"))
    st.write("AI mode:", "Connected" if api_ready else "Local fallback")
    if not api_ready:
        st.info("Add OPENAI_API_KEY to a .env file to enable generated summaries and explanations. PDF extraction, NLP analysis and document retrieval work without it.")

uploaded = st.file_uploader("Upload a research paper (PDF)", type=["pdf"])

if uploaded:
    try:
        pages = extract_pdf(uploaded)
        full_text = "\n\n".join(p["text"] for p in pages)
        if not full_text.strip():
            st.error("No selectable text was found. This may be a scanned PDF; OCR is not included in this prototype.")
            st.stop()

        chunks = chunk_pages(pages)
        retriever = TfidfRetriever()
        retriever.fit(chunks)
        st.success(f"Processed {len(pages)} pages and created {len(chunks)} searchable text chunks.")

        tab_summary, tab_nlp, tab_qa, tab_student = st.tabs(
            ["📝 Summary", "🔎 NLP Analysis", "💬 Ask the Paper", "🎓 Student Mode"]
        )

        with tab_summary:
            st.subheader("Structured research summary")
            if st.button("Generate summary", type="primary"):
                with st.spinner("Analysing the paper..."):
                    result = generate_summary(full_text)
                st.markdown(result)
                st.download_button("Download summary", result, file_name="researchmate_summary.md")

        with tab_nlp:
            st.subheader("NLP analysis")
            analysis = analyze_text(full_text)
            c1, c2, c3 = st.columns(3)
            c1.metric("Pages with text", len(pages))
            c2.metric("Words", analysis["word_count"])
            c3.metric("Detected sections", len(analysis["sections"]))
            st.markdown("**Detected sections**")
            st.write(", ".join(analysis["sections"]) if analysis["sections"] else "No standard section headings detected.")
            st.markdown("**Frequent keywords / noun phrases**")
            st.write(", ".join(analysis["keywords"]) if analysis["keywords"] else "No keywords detected.")
            st.markdown("**Named entities**")
            if analysis["entities"]:
                st.dataframe(analysis["entities"][:40], use_container_width=True)
            else:
                st.write("No named entities detected (spaCy model may not be installed).")

        with tab_qa:
            st.subheader("Ask a question about this paper")
            question = st.text_input("Example: What dataset did the authors use?")
            if st.button("Find answer") and question.strip():
                with st.spinner("Retrieving relevant passages..."):
                    results = retriever.search(question, top_k=4)
                    answer = answer_question(question, results)
                st.markdown("### Answer")
                st.markdown(answer)
                st.markdown("### Retrieved evidence")
                for item in results:
                    with st.expander(f"Page {item['page']} · relevance {item['score']:.2f}"):
                        st.write(item["text"])

        with tab_student:
            st.subheader("Explain the paper at your level")
            level = st.selectbox("Choose your level", ["Beginner", "Intermediate", "Advanced"])
            if st.button("Explain paper"):
                with st.spinner("Preparing an explanation..."):
                    explanation = explain_paper(full_text, level)
                st.markdown(explanation)

    except Exception as exc:
        st.error(f"Could not process this PDF: {exc}")
else:
    st.info("Start by uploading a research-paper PDF.")
    st.markdown("""
    **What this prototype includes**
    - PDF text extraction with page tracking
    - NLP keyword and named-entity analysis
    - Section-heading detection
    - TF-IDF document retrieval for question answering
    - Optional OpenAI-powered summaries, answers and explanations
    """)
