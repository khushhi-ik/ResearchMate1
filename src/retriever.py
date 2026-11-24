from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TfidfRetriever:
    """Lightweight local retrieval baseline using TF-IDF and cosine similarity."""
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=50000)
        self.matrix = None
        self.chunks = []

    def fit(self, chunks):
        self.chunks = chunks
        corpus = [c["text"] for c in chunks]
        self.matrix = self.vectorizer.fit_transform(corpus)

    def search(self, query, top_k=4):
        if self.matrix is None or not self.chunks:
            return []
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix).ravel()
        ranked = scores.argsort()[::-1][:top_k]
        return [
            {"text": self.chunks[i]["text"], "page": self.chunks[i]["page"], "score": float(scores[i])}
            for i in ranked if scores[i] > 0
        ]
