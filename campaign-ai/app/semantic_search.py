from pathlib import Path
import math
import sqlite3
import struct

import ollama


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "campaign_knowledge.db"
)

EMBED_MODEL = "nomic-embed-text"


# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

def get_connection():

    conn = sqlite3.connect(
        DB_PATH
    )

    conn.row_factory = sqlite3.Row

    return conn


# ---------------------------------------------------------
# Vector conversion
# ---------------------------------------------------------

def deserialize_embedding(blob):

    dimensions = len(blob) // 4

    return list(
        struct.unpack(
            f"{dimensions}f",
            blob,
        )
    )


# ---------------------------------------------------------
# Cosine similarity
# ---------------------------------------------------------

def cosine_similarity(
    vector_a,
    vector_b,
):
    if not vector_a or not vector_b:
        return 0.0

    if len(vector_a) != len(vector_b):
        return 0.0

    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0

    for a, b in zip(
        vector_a,
        vector_b,
    ):

        dot += a * b
        norm_a += a * a
        norm_b += b * b

    if norm_a == 0.0:
        return 0.0

    if norm_b == 0.0:
        return 0.0

    return (
        dot
        / (
            math.sqrt(norm_a)
            * math.sqrt(norm_b)
        )
    )


# ---------------------------------------------------------
# Query embedding
# ---------------------------------------------------------

def embed_query(query):

    response = ollama.embed(
        model=EMBED_MODEL,
        input=query,
    )

    embeddings = response["embeddings"]

    if not embeddings:
        raise RuntimeError(
            "Ollama returned no query embedding."
        )

    return embeddings[0]


# ---------------------------------------------------------
# Search
# ---------------------------------------------------------

def semantic_search(
    query,
    limit=10,
):

    query_embedding = embed_query(
        query
    )

    conn = get_connection()

    try:

        rows = conn.execute("""
            SELECT
                chunk_embeddings.chunk_id,
                chunk_embeddings.embedding,

                chunks.document_id,
                chunks.chunk_index,
                chunks.heading,
                chunks.content,

                documents.source_type,
                documents.source_file,
                documents.title,
                documents.page_id,
                documents.confluence_url,
                documents.relative_path,
                documents.modified_time

            FROM chunk_embeddings

            JOIN chunks
                ON chunk_embeddings.chunk_id = chunks.id

            JOIN documents
                ON chunks.document_id = documents.id

            WHERE chunk_embeddings.model = ?

        """, (
            EMBED_MODEL,
        )).fetchall()

        results = []

        for row in rows:

            embedding = deserialize_embedding(
                row["embedding"]
            )

            similarity = cosine_similarity(
                query_embedding,
                embedding,
            )

            result = dict(row)

            result.pop(
                "embedding",
                None,
            )

            result["semantic_score"] = (
                similarity
            )

            results.append(
                result
            )

        results.sort(
            key=lambda x: x[
                "semantic_score"
            ],
            reverse=True,
        )

        return results[:limit]

    finally:

        conn.close()


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:

        print(
            'Usage: python semantic_search.py "question"'
        )

        raise SystemExit(1)

    question = " ".join(
        sys.argv[1:]
    )

    results = semantic_search(
        question,
        limit=10,
    )

    print()
    print("=" * 80)
    print("SEMANTIC SEARCH")
    print("=" * 80)

    print()
    print(
        f"Question: {question}"
    )

    print(
        f"Results: {len(results)}"
    )

    for index, result in enumerate(
        results,
        start=1,
    ):

        print()
        print("-" * 80)

        print(
            f"[{index}] "
            f"{result['title']}"
        )

        print(
            f"Similarity: "
            f"{result['semantic_score']:.4f}"
        )

        print(
            f"Heading: "
            f"{result['heading']}"
        )

        print()

        print(
            result["content"][:1000]
        )
