import re
from collections import Counter

SECTION_NAMES = [
    "abstract", "introduction", "related work", "literature review",
    "methodology", "methods", "materials and methods", "experiments",
    "results", "discussion", "conclusion", "limitations", "future work",
    "references"
]

def analyze_text(text):
    words = re.findall(r"\b[A-Za-z][A-Za-z'-]{2,}\b", text.lower())
    stop = {
        "the","and","for","that","with","this","from","are","was","were",
        "have","has","into","using","based","their","they","which","these",
        "those","such","than","then","also","can","may","our","its","not",
        "but","all","between","within","been","being","more","most","other"
    }
    keywords = [w for w, _ in Counter(x for x in words if x not in stop).most_common(20)]
    lower = text.lower()
    sections = [name.title() for name in SECTION_NAMES if re.search(
        rf"(?im)^\s*(?:\d+(?:\.\d+)*\.?\s*)?{re.escape(name)}\s*$", text
    ) or re.search(rf"\b{re.escape(name)}\b", lower)]

    entities = []
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text[:200000])
        seen = set()
        for ent in doc.ents:
            key = (ent.text.strip(), ent.label_)
            if key not in seen:
                seen.add(key)
                entities.append({"Entity": ent.text, "Type": ent.label_})
    except (ImportError, OSError):
        pass

    return {
        "word_count": len(words),
        "keywords": keywords,
        "sections": sections,
        "entities": entities
    }
