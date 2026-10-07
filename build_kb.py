"""
Builds the vector knowledge base for the portfolio chatbot.

Reads every .md file in knowledge_base/, splits it into overlapping chunks,
and stores the chunks + embeddings in a local persistent ChromaDB collection.

Run this once locally (and again any time you edit the knowledge_base/ files):
    python build_kb.py
"""

import os
import re
import chromadb

KB_DIR = "knowledge_base"
DB_DIR = "chroma_db"
COLLECTION_NAME = "portfolio"

# Chunking settings — tuned for short case-study docs like these.
CHUNK_SIZE = 800       # characters per chunk
CHUNK_OVERLAP = 150    # overlap between consecutive chunks


def chunk_text(text: str, source: str):
    """Split text into overlapping chunks, breaking on paragraph boundaries
    where possible so chunks don't cut sentences in half."""
    # Split into paragraphs first
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 <= CHUNK_SIZE:
            current = f"{current}\n\n{para}" if current else para
        else:
            if current:
                chunks.append(current)
            # start new chunk, carrying a bit of overlap from the end of the previous chunk
            overlap = current[-CHUNK_OVERLAP:] if current else ""
            current = f"{overlap}\n\n{para}" if overlap else para

    if current:
        chunks.append(current)

    return chunks


def main():
    if not os.path.isdir(KB_DIR):
        raise SystemExit(f"Knowledge base folder '{KB_DIR}' not found.")

    client = chromadb.PersistentClient(path=DB_DIR)

    # Fresh build each run: drop the old collection if it exists
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    # Uses ChromaDB's built-in default embedding function (all-MiniLM-L6-v2,
    # runs locally via onnxruntime — no API key or heavy ML deps needed).
    collection = client.create_collection(name=COLLECTION_NAME)

    ids, documents, metadatas = [], [], []
    chunk_counter = 0

    for filename in sorted(os.listdir(KB_DIR)):
        if not filename.endswith(".md"):
            continue
        path = os.path.join(KB_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        source_name = filename.replace(".md", "").replace("_", " ").title()
        file_chunks = chunk_text(text, source_name)

        for chunk in file_chunks:
            ids.append(f"chunk_{chunk_counter}")
            documents.append(chunk)
            metadatas.append({"source": source_name, "filename": filename})
            chunk_counter += 1

        print(f"  {filename}: {len(file_chunks)} chunks")

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    print(f"\nDone. Indexed {chunk_counter} chunks from {KB_DIR}/ into '{DB_DIR}/'.")


if __name__ == "__main__":
    main()
