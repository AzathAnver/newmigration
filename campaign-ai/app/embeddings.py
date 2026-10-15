from pathlib import Path
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
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_embeddings_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunk_embeddings (
            chunk_id INTEGER PRIMARY KEY,
            embedding BLOB NOT NULL,
            dimensions INTEGER NOT NULL,
            model TEXT NOT NULL,
            FOREIGN KEY(chunk_id)
                REFERENCES chunks(id)
        )
    """)

    conn.commit()


# ---------------------------------------------------------
# Float vector serialization
# ---------------------------------------------------------

def serialize_embedding(vector):
    """
    Convert list[float] into compact SQLite BLOB.
    """

    return struct.pack(
        f"{len(vector)}f",
        *vector,
    )


def deserialize_embedding(blob):
    """
    Convert SQLite BLOB back into list[float].
    """

    dimensions = len(blob) // 4

    return list(
        struct.unpack(
            f"{dimensions}f",
            blob,
        )
    )


# ---------------------------------------------------------
# Get embedding
# ---------------------------------------------------------

def embed_text(text: str):
    response = ollama.embed(
        model=EMBED_MODEL,
        input=text,
    )

    embeddings = response["embeddings"]

    if not embeddings:
        raise RuntimeError(
            "Ollama returned no embedding."
        )

    return embeddings[0]


# ---------------------------------------------------------
# Build text for embedding
# ---------------------------------------------------------

def build_chunk_text(row):
    title = row["title"] or ""
    heading = row["heading"] or ""
    content = row["content"] or ""

    return f"""
Title: {title}

Heading: {heading}

Content:
{content}
""".strip()


# ---------------------------------------------------------
# Index embeddings
# ---------------------------------------------------------

def build_embeddings():
    conn = get_connection()

    try:

        create_embeddings_table(conn)

        rows = conn.execute("""
            SELECT
                chunks.id,
                chunks.heading,
                chunks.content,
                documents.title

            FROM chunks

            JOIN documents
                ON chunks.document_id = documents.id

            ORDER BY chunks.id
        """).fetchall()

        total = len(rows)

        print()
        print("=" * 80)
        print("BUILDING SEMANTIC EMBEDDINGS")
        print("=" * 80)

        print()
        print(
            f"Chunks to embed: {total}"
        )

        processed = 0

        for row in rows:

            existing = conn.execute(
                """
                SELECT chunk_id
                FROM chunk_embeddings
                WHERE chunk_id = ?
                AND model = ?
                """,
                (
                    row["id"],
                    EMBED_MODEL,
                ),
            ).fetchone()

            if existing:
                processed += 1

                print(
                    f"[SKIP] "
                    f"{processed}/{total}",
                    end="\r",
                )

                continue

            text = build_chunk_text(
                row
            )

            embedding = embed_text(
                text
            )

            blob = serialize_embedding(
                embedding
            )

            conn.execute(
                """
                INSERT OR REPLACE INTO
                chunk_embeddings (
                    chunk_id,
                    embedding,
                    dimensions,
                    model
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    row["id"],
                    blob,
                    len(embedding),
                    EMBED_MODEL,
                ),
            )

            conn.commit()

            processed += 1

            print(
                f"[EMBED] "
                f"{processed}/{total} "
                f"chunk {row['id']}",
                end="\r",
            )

        print()
        print()
        print(
            "Semantic embedding index complete."
        )

    finally:

        conn.close()


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    build_embeddings()
