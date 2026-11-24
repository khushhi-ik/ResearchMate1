# ResearchMate

ResearchMate is a student-facing research-paper assistant built with Streamlit, Python and NLP.

## Features
- Upload text-based research-paper PDFs.
- Extract page-level text using PyMuPDF.
- Analyse frequent terms, detect common paper sections and optionally identify named entities with spaCy.
- Split text into overlapping chunks while preserving page numbers.
- Retrieve relevant passages using a local TF-IDF + cosine-similarity baseline.
- Optionally use the OpenAI API for structured summaries, paper Q&A and student-level explanations.
- Run core PDF/NLP/retrieval features without an API key. Without a key, summaries use a simple extractive preview and Q&A displays retrieved evidence rather than inventing an answer.

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

If the spaCy model download fails, the app still runs; named-entity results will simply be unavailable.

## Configure the optional AI API

Copy `.env.example` to `.env` and add your own API key:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5-mini
```

Never commit `.env` or share your API key. API usage may incur charges.

## Run

```powershell
streamlit run app.py
```

The app opens in your browser, usually at `http://localhost:8501`.

## Important limitations
- Scanned/image-only PDFs are not OCR processed.
- Multi-column layouts, equations, tables and figures may not extract perfectly.
- TF-IDF is a lexical retrieval baseline, not a neural semantic embedding model.
- Page citations identify the page of the retrieved text; generated claims still require checking against the original paper.
- This is an educational prototype, not a substitute for reading or validating the source paper.

## Suggested evaluation
Create a test table with at least 10 distinct PDFs/questions, expected outputs, actual outputs and Pass/Fail results. Include normal, edge and invalid inputs. Record prompt versions and changes separately.
