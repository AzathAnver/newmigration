from pathlib import Path
import sqlite3
import re
import sys


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "campaign_knowledge.db"
)

DEFAULT_LIMIT = 8


# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

def get_connection():
    """
    Open a read-only connection to the knowledge database.
    """

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# ---------------------------------------------------------
# Query cleaning
# ---------------------------------------------------------

def clean_query(query: str) -> str:
    """
    Convert a natural-language question into a safe FTS5 query.

    Example:

        How do I troubleshoot ED 2.0 feed issues?

    becomes something like:

        "How" AND "do" AND "I" AND "troubleshoot" ...
    """

    # Extract words, numbers, and useful identifiers.
    tokens = re.findall(
        r"[A-Za-z0-9_.-]+",
        query
    )

    if not tokens:
        return ""

    # Remove extremely common words that don't help much
    # with knowledge retrieval.
    stop_words = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "can",
        "could",
        "do",
        "does",
        "for",
        "from",
        "how",
        "i",
        "in",
        "is",
        "it",
        "me",
        "of",
        "on",
        "or",
        "the",
        "this",
        "to",
        "what",
        "when",
        "where",
        "which",
        "who",
        "why",
        "with",
        "you",
    }

    useful_tokens = [
        token
        for token in tokens
        if token.lower() not in stop_words
    ]

    # If everything was a stop word, use the original tokens.
    if not useful_tokens:
        useful_tokens = tokens

    # Quote every token so FTS5 operators such as
    # AND/OR/NOT don't accidentally alter the query.
    escaped = [
        '"' + token.replace('"', '""') + '"'
        for token in useful_tokens
    ]

    return " AND ".join(escaped)


# ---------------------------------------------------------
# Search
# ---------------------------------------------------------

def search(
    query: str,
    limit: int = DEFAULT_LIMIT
):
    """
    Search the knowledge base.

    Returns a list of dictionaries.
    """

    fts_query = clean_query(query)

    if not fts_query:
        return []

    conn = get_connection()

    try:

        rows = conn.execute(
            """
            SELECT
                chunks.id AS chunk_id,
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
                documents.modified_time,

                bm25(
                    chunks_fts,
                    5.0,
                    2.0
                ) AS rank

            FROM chunks_fts

            JOIN chunks
                ON chunks_fts.rowid = chunks.id

            JOIN documents
                ON chunks.document_id = documents.id

            WHERE chunks_fts MATCH ?

            ORDER BY rank

            LIMIT ?
            """,
            (
                fts_query,
                limit,
            ),
        ).fetchall()

        results = []

        for row in rows:

            results.append({
                "chunk_id": row["chunk_id"],
                "document_id": row["document_id"],
                "chunk_index": row["chunk_index"],
                "heading": row["heading"] or "",
                "content": row["content"],
                "source_type": row["source_type"],
                "source_file": row["source_file"],
                "title": row["title"] or "",
                "page_id": row["page_id"],
                "confluence_url": row["confluence_url"],
                "relative_path": row["relative_path"],
                "modified_time": row["modified_time"],
                "rank": row["rank"],
            })

        return results

    finally:
        conn.close()


# ---------------------------------------------------------
# Search with fallback
# ---------------------------------------------------------

def search_with_fallback(
    query: str,
    limit: int = DEFAULT_LIMIT
):
    """
    Search using the normal AND query first.

    If no results are found, retry using OR so that
    questions containing terminology variations can still
    return useful documents.
    """

    results = search(
        query=query,
        limit=limit
    )

    if results:
        return results

    # -----------------------------------------------------
    # Fallback OR search
    # -----------------------------------------------------

    tokens = re.findall(
        r"[A-Za-z0-9_.-]+",
        query
    )

    if not tokens:
        return []

    stop_words = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "can",
        "could",
        "do",
        "does",
        "for",
        "from",
        "how",
        "i",
        "in",
        "is",
        "it",
        "me",
        "of",
        "on",
        "or",
        "the",
        "this",
        "to",
        "what",
        "when",
        "where",
        "which",
        "who",
        "why",
        "with",
        "you",
    }

    useful_tokens = [
        token
        for token in tokens
        if token.lower() not in stop_words
    ]

    if not useful_tokens:
        useful_tokens = tokens

    escaped = [
        '"' + token.replace('"', '""') + '"'
        for token in useful_tokens
    ]

    fts_query = " OR ".join(escaped)

    conn = get_connection()

    try:

        rows = conn.execute(
            """
            SELECT
                chunks.id AS chunk_id,
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
                documents.modified_time,

                bm25(
                    chunks_fts,
                    5.0,
                    2.0
                ) AS rank

            FROM chunks_fts

            JOIN chunks
                ON chunks_fts.rowid = chunks.id

            JOIN documents
                ON chunks.document_id = documents.id

            WHERE chunks_fts MATCH ?

            ORDER BY rank

            LIMIT ?
            """,
            (
                fts_query,
                limit,
            ),
        ).fetchall()

        results = []

        for row in rows:

            results.append({
                "chunk_id": row["chunk_id"],
                "document_id": row["document_id"],
                "chunk_index": row["chunk_index"],
                "heading": row["heading"] or "",
                "content": row["content"],
                "source_type": row["source_type"],
                "source_file": row["source_file"],
                "title": row["title"] or "",
                "page_id": row["page_id"],
                "confluence_url": row["confluence_url"],
                "relative_path": row["relative_path"],
                "modified_time": row["modified_time"],
                "rank": row["rank"],
            })

        return results

    finally:
        conn.close()


# ---------------------------------------------------------
# Format results
# ---------------------------------------------------------

def print_results(
    query: str,
    results
):
    """
    Pretty-print search results.
    """

    print()
    print("=" * 80)
    print("SEARCH")
    print("=" * 80)

    print()
    print(f"Query: {query}")

    print()
    print(f"Results: {len(results)}")

    if not results:

        print()
        print("No results found.")

        return

    print()

    for index, result in enumerate(
        results,
        start=1
    ):

        print("-" * 80)

        print(
            f"[{index}] "
            f"{result['title']}"
        )

        if result["heading"]:

            print(
                f"Heading: "
                f"{result['heading']}"
            )

        print(
            f"Source: "
            f"{result['source_type']}"
        )

        print(
            f"Rank: "
            f"{result['rank']:.4f}"
        )

        print(
            f"File: "
            f"{result['relative_path']}"
        )

        if result["confluence_url"]:

            print(
                f"Confluence: "
                f"{result['confluence_url']}"
            )

        print()

        print(
            result["content"]
        )

        print()


# ---------------------------------------------------------
# Interactive search
# ---------------------------------------------------------

def interactive_search():

    print()
    print("=" * 80)
    print("CAMPAIGN KNOWLEDGE SEARCH")
    print("=" * 80)

    print()
    print(f"Database: {DB_PATH}")

    print()
    print("Type a question to search.")
    print("Type 'exit' or 'quit' to stop.")

    while True:

        print()

        try:

            query = input(
                "Question: "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError,
        ):

            print()
            print("Exiting.")

            break

        if not query:
            continue

        if query.lower() in {
            "exit",
            "quit",
            "q",
        }:

            print(
                "Goodbye."
            )

            break

        try:

            results = search_with_fallback(
                query=query,
                limit=DEFAULT_LIMIT,
            )

            print_results(
                query=query,
                results=results,
            )

        except Exception as exc:

            print()
            print(
                f"[ERROR] {exc}"
            )


# ---------------------------------------------------------
# Command-line search
# ---------------------------------------------------------

def command_line_search():

    if len(sys.argv) < 2:

        interactive_search()

        return

    query = " ".join(
        sys.argv[1:]
    )

    try:

        results = search_with_fallback(
            query=query,
            limit=DEFAULT_LIMIT,
        )

        print_results(
            query=query,
            results=results,
        )

    except Exception as exc:

        print(
            f"[ERROR] {exc}"
        )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    command_line_search()
