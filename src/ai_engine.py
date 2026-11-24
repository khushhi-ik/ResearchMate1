import os

def _client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=key)
    except ImportError:
        return None

def _ask(prompt, fallback):
    client = _client()
    if client is None:
        return fallback
    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
            input=prompt
        )
        return response.output_text
    except Exception as exc:
        return fallback + f"\n\n**AI API note:** The API request could not be completed ({type(exc).__name__}). Check your API key, model access and network connection."

def generate_summary(text):
    prompt = f"""You are ResearchMate, an academic assistant. Summarise the research paper below.
Use only the supplied text. Do not invent datasets, metrics, results or limitations.
If a detail is absent, write 'Not clearly stated in the provided text'.
Use headings: Research problem, Objective, Methodology, Dataset, Models/Algorithms,
Key results, Contributions, Limitations, Future work, Simple explanation.
Keep the output clear for university students.

PAPER TEXT:
{text[:45000]}"""
    fallback = extractive_fallback(text)
    return _ask(prompt, fallback)

def answer_question(question, results):
    if not results:
        return "I could not retrieve a relevant passage. Try rephrasing the question or check whether the PDF contains selectable text."
    context = "\n\n".join(f"[Page {r['page']}]\n{r['text']}" for r in results)
    prompt = f"""Answer the student's question using ONLY the retrieved paper passages.
If the passages do not contain the answer, say so. Do not guess.
Cite page numbers in the answer.

PASSAGES:
{context}

QUESTION: {question}"""
    fallback = "I found these potentially relevant passages, but no AI API key is configured. Review the evidence below and use the page numbers to locate the answer in the paper."
    return _ask(prompt, fallback)

def explain_paper(text, level):
    prompt = f"""Explain this research paper to a {level.lower()} university student.
Use only the supplied text. Explain the problem, core idea, method and findings.
Define technical terms and use a simple analogy where useful. Do not invent facts.
If details are missing, say so.

PAPER:
{text[:35000]}"""
    return _ask(prompt, extractive_fallback(text) + "\n\nAdd an OPENAI_API_KEY to enable a tailored explanation.")

def extractive_fallback(text):
    """Simple no-API fallback: select early informative sentences."""
    import re
    sentences = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text))
    useful = [s.strip() for s in sentences if len(s.strip()) > 45]
    chosen = useful[:8]
    if not chosen:
        return "Not enough readable text was extracted to create a summary."
    return "### Local extractive preview (no API key configured)\\n\\n" + "\\n\\n".join(f"- {s}" for s in chosen)
