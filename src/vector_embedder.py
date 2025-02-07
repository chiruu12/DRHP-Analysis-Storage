import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer


class VectorEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def store_embeddings(self, companies: list, output_prefix: str) -> None:
        embeddings = []
        metadata = []
        for company in companies:
            for section in company.sections:
                text_to_embed = section.key_findings if section.key_findings.strip() else section.full_text
                if not text_to_embed.strip():
                    continue
                emb = self.model.encode(text_to_embed)
                embeddings.append(emb)
                metadata.append({
                    "company_name": company.company_name,
                    "section_number": section.section_number,
                    "chapter_name": section.chapter_name,
                    "key_findings": section.key_findings
                })
        if not embeddings:
            print("No embeddings generated.")
            return
        emb_np = np.array(embeddings).astype("float32")
        np.savez_compressed(f"{output_prefix}_embeddings.npz", embeddings=emb_np)
        with open(f"{output_prefix}_metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
