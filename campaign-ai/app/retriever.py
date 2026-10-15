from pathlib import Path
import sqlite3
import re
from collections import defaultdict

from semantic_search import semantic_search


# =========================================================
# Configuration
# =========================================================

DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "campaign_knowledge.db"
)

DEFAULT_LIMIT = 10


# =========================================================
# Stop words
# =========================================================

STOP_WORDS = {
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
    "if",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "should",
    "that",
    "the",
    "this",
    "to",
    "was",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
    "you",
    "your",
}


# =========================================================
# Database
# =========================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# Tokenization
# =========================================================

def tokenize(text):
    if not text:
        return []

    tokens = re.findall(
        r"[A-Za-z0-9_.-]+",
        text.lower(),
    )

    return [
        token
        for token in tokens
        if token not in STOP_WORDS
        and len(token) > 1
    ]


# =========================================================
# FTS query builders
# =========================================================

def build_fts_query(query):
    tokens = tokenize(query)

    if not tokens:
        return ""

    return " AND ".join(
        '"' + token.replace('"', '""') + '"'
        for token in tokens
    )


def build_or_query(query):
    tokens = tokenize(query)

    if not tokens:
        return ""

    return " OR ".join(
        '"' + token.replace('"', '""') + '"'
        for token in tokens
    )


# =========================================================
# FTS search
# =========================================================

def fts_search(
    conn,
    fts_query,
    limit,
):
    if not fts_query:
        return []

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
            ) AS bm25_rank

        FROM chunks_fts

        JOIN chunks
            ON chunks_fts.rowid = chunks.id

        JOIN documents
            ON chunks.document_id = documents.id

        WHERE chunks_fts MATCH ?

        ORDER BY bm25_rank

        LIMIT ?
        """,
        (
            fts_query,
            limit,
        ),
    ).fetchall()

    return [
        dict(row)
        for row in rows
    ]


# =========================================================
# Phrase normalization
# =========================================================

def normalize_phrase(text):
    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    return text


# =========================================================
# Keyword score
# =========================================================

def keyword_score(
    query,
    result,
):
    query_lower = normalize_phrase(query)

    query_tokens = set(
        tokenize(query)
    )

    if not query_tokens:
        return 0.0

    title = normalize_phrase(
        result.get(
            "title",
            "",
        )
    )

    heading = normalize_phrase(
        result.get(
            "heading",
            "",
        )
    )

    content = result.get(
        "content",
        "",
    ).lower()

    score = 0.0

    # -----------------------------------------------------
    # Strong exact title / heading matching
    # -----------------------------------------------------

    if query_lower == title:
        score += 30.0

    elif query_lower in title:
        score += 20.0

    if query_lower == heading:
        score += 25.0

    elif query_lower in heading:
        score += 15.0

    # -----------------------------------------------------
    # Token matching
    # -----------------------------------------------------

    for token in query_tokens:

        if token in title:
            score += 8.0

        if token in heading:
            score += 5.0

        occurrences = content.count(
            token
        )

        score += min(
            occurrences,
            5,
        )

    # -----------------------------------------------------
    # Important phrase matching
    # -----------------------------------------------------

    important_phrases = [
        "not reflecting",
        "not syncing",
        "not sync",
        "sync to sap",
        "reflecting in sap",
        "monthly spend confirmation",
        "media plan",
        "reconciliation",
        "reconciled",
        "push back",
        "published stage",
        "confirmed spend",
        "plan line budget",
        "budget update",
    ]

    for phrase in important_phrases:

        if phrase in query_lower:

            if phrase in title:
                score += 12.0

            if phrase in heading:
                score += 8.0

            if phrase in content:
                score += 2.0

    return score


# =========================================================
# Intent score
# =========================================================

def intent_score(
    query,
    result,
):
    query_lower = query.lower()

    content = (
        result.get("title", "")
        + " "
        + result.get("heading", "")
        + " "
        + result.get("content", "")
    ).lower()

    score = 0.0

    intent_groups = [

        # -------------------------------------------------
        # Reconciliation / budget workflow
        # -------------------------------------------------

        (
            [
                "reconciliation",
                "reconcile",
                "ended",
                "campaign ended",
            ],
            [
                "reconciliation",
                "published",
                "budget",
                "plan line",
            ],
        ),

        # -------------------------------------------------
        # Budget
        # -------------------------------------------------

        (
            [
                "budget",
                "revised budget",
                "planned budget",
            ],
            [
                "budget",
                "plan line",
                "media plan",
            ],
        ),

        # -------------------------------------------------
        # Spend / MSC
        # -------------------------------------------------

        (
            [
                "actual spend",
                "spend",
                "msc",
                "monthly spend",
                "confirmed spend",
            ],
            [
                "confirmed spend",
                "actual spend",
                "monthly spend",
                "msc",
            ],
        ),

        # -------------------------------------------------
        # SAP
        # -------------------------------------------------

        (
            [
                "sap",
                "reflecting in sap",
                "sync to sap",
                "syncing to sap",
                "not reflecting",
            ],
            [
                "sap",
                "sync",
                "syncing",
                "reflecting",
                "integration",
            ],
        ),

        # -------------------------------------------------
        # Access
        # -------------------------------------------------

        (
            [
                "access",
                "permission",
                "permissions",
            ],
            [
                "access",
                "role",
                "permission",
            ],
        ),

        # -------------------------------------------------
        # Support / issue
        # -------------------------------------------------

        (
            [
                "support",
                "issue",
                "problem",
                "error",
                "not working",
                "not reflecting",
            ],
            [
                "support",
                "troubleshoot",
                "issue",
                "error",
                "problem",
            ],
        ),
    ]

    for query_terms, boost_terms in intent_groups:

        if any(
            term in query_lower
            for term in query_terms
        ):

            for boost_term in boost_terms:

                if boost_term in content:
                    score += 3.0

    return score


# =========================================================
# Normalize scores
# =========================================================

def normalize_scores(
    results,
    field,
):
    if not results:
        return

    values = [
        float(
            result.get(
                field,
                0.0,
            )
        )
        for result in results
    ]

    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:

        for result in results:

            result[
                f"{field}_normalized"
            ] = 1.0

        return

    for result in results:

        value = float(
            result.get(
                field,
                0.0,
            )
        )

        normalized = (
            (value - minimum)
            / (maximum - minimum)
        )

        result[
            f"{field}_normalized"
        ] = normalized


# =========================================================
# Exact title / heading boost
# =========================================================

def apply_exact_match_boost(
    query,
    results,
):
    query_normalized = normalize_phrase(
        query
    )

    if not query_normalized:
        return

    for result in results:

        title = normalize_phrase(
            result.get(
                "title",
                "",
            )
        )

        heading = normalize_phrase(
            result.get(
                "heading",
                "",
            )
        )

        # -------------------------------------------------
        # Exact title
        # -------------------------------------------------

        if query_normalized == title:

            result[
                "retrieval_score"
            ] += 0.50

            result[
                "exact_match"
            ] = True

            continue

        # -------------------------------------------------
        # Exact heading
        # -------------------------------------------------

        if query_normalized == heading:

            result[
                "retrieval_score"
            ] += 0.40

            result[
                "exact_match"
            ] = True

            continue

        # -------------------------------------------------
        # Query contained in title
        # -------------------------------------------------

        if query_normalized in title:

            result[
                "retrieval_score"
            ] += 0.30

            result[
                "exact_match"
            ] = True

            continue

        # -------------------------------------------------
        # Query contained in heading
        # -------------------------------------------------

        if query_normalized in heading:

            result[
                "retrieval_score"
            ] += 0.25

            result[
                "exact_match"
            ] = True


# =========================================================
# Hybrid retrieval
# =========================================================

def retrieve(
    query,
    limit=DEFAULT_LIMIT,
):
    if not query or not query.strip():
        return []

    conn = get_connection()

    try:

        # =================================================
        # FTS retrieval
        # =================================================

        and_query = build_fts_query(
            query
        )

        fts_results = fts_search(
            conn,
            and_query,
            limit * 5,
        )

        # -------------------------------------------------
        # Fall back to OR search
        # -------------------------------------------------

        if not fts_results:

            or_query = build_or_query(
                query
            )

            fts_results = fts_search(
                conn,
                or_query,
                limit * 5,
            )

        # =================================================
        # Score FTS results
        # =================================================

        for result in fts_results:

            bm25 = max(
                0.0,
                -float(
                    result.get(
                        "bm25_rank",
                        0,
                    )
                ),
            )

            keyword = keyword_score(
                query,
                result,
            )

            intent = intent_score(
                query,
                result,
            )

            result[
                "fts_score"
            ] = (
                bm25
                + keyword
                + intent
            )

        # =================================================
        # Semantic retrieval
        # =================================================

        semantic_results = semantic_search(
            query,
            limit=limit * 5,
        )

        # =================================================
        # Normalize ranking systems
        # =================================================

        normalize_scores(
            fts_results,
            "fts_score",
        )

        normalize_scores(
            semantic_results,
            "semantic_score",
        )

        # =================================================
        # Merge results
        # =================================================

        merged = {}

        # -------------------------------------------------
        # Add FTS results
        # -------------------------------------------------

        for result in fts_results:

            chunk_id = result[
                "chunk_id"
            ]

            merged[
                chunk_id
            ] = dict(
                result
            )

            merged[
                chunk_id
            ][
                "fts_normalized"
            ] = result.get(
                "fts_score_normalized",
                0.0,
            )

            merged[
                chunk_id
            ][
                "semantic_normalized"
            ] = 0.0

        # -------------------------------------------------
        # Add semantic results
        # -------------------------------------------------

        for result in semantic_results:

            chunk_id = result[
                "chunk_id"
            ]

            if chunk_id not in merged:

                merged[
                    chunk_id
                ] = dict(
                    result
                )

                merged[
                    chunk_id
                ][
                    "fts_normalized"
                ] = 0.0

            merged[
                chunk_id
            ][
                "semantic_normalized"
            ] = result.get(
                "semantic_score_normalized",
                0.0,
            )

        # =================================================
        # Hybrid score
        # =================================================

        for result in merged.values():

            fts_score = result.get(
                "fts_normalized",
                0.0,
            )

            semantic_score = result.get(
                "semantic_normalized",
                0.0,
            )

            result[
                "retrieval_score"
            ] = (
                0.45 * fts_score
                + 0.55 * semantic_score
            )

        # =================================================
        # Exact title / heading boost
        # =================================================

        apply_exact_match_boost(
            query,
            list(
                merged.values()
            ),
        )

        # =================================================
        # Sort
        # =================================================

        results = list(
            merged.values()
        )

        results.sort(
            key=lambda item:
                item.get(
                    "retrieval_score",
                    0.0,
                ),
            reverse=True,
        )

        # =================================================
        # Deduplicate
        # =================================================

        results = deduplicate_results(
            results
        )

        return results[:limit]

    finally:

        conn.close()


# =========================================================
# Deduplicate results
# =========================================================

def deduplicate_results(
    results,
):
    seen_chunks = set()

    seen_content = set()

    document_counts = defaultdict(
        int
    )

    cleaned = []

    for result in results:

        chunk_id = result[
            "chunk_id"
        ]

        if chunk_id in seen_chunks:
            continue

        normalized = re.sub(
            r"\s+",
            " ",
            result.get(
                "content",
                "",
            ).strip().lower(),
        )

        content_key = normalized[
            :500
        ]

        if content_key in seen_content:
            continue

        document_id = result[
            "document_id"
        ]

        if document_counts[
            document_id
        ] >= 3:
            continue

        seen_chunks.add(
            chunk_id
        )

        seen_content.add(
            content_key
        )

        document_counts[
            document_id
        ] += 1

        cleaned.append(
            result
        )

    return cleaned


# =========================================================
# Context builder
# =========================================================

def build_context(
    results,
    max_characters=18000,
):
    if not results:
        return ""

    sections = []

    total_characters = 0

    for index, result in enumerate(
        results,
        start=1,
    ):

        source = result.get(
            "source_type",
            "unknown",
        )

        title = result.get(
            "title",
            "",
        )

        heading = result.get(
            "heading",
            "",
        )

        content = result.get(
            "content",
            "",
        )

        url = result.get(
            "confluence_url"
        )

        section = [
            f"[SOURCE {index}]",
            f"Source type: {source}",
            f"Title: {title}",
        ]

        if heading:
            section.append(
                f"Heading: {heading}"
            )

        if url:
            section.append(
                f"URL: {url}"
            )

        section.append("")
        section.append(content)

        formatted = "\n".join(
            section
        )

        if (
            total_characters
            + len(formatted)
            > max_characters
        ):
            break

        sections.append(
            formatted
        )

        total_characters += len(
            formatted
        )

    return "\n\n".join(
        sections
    )


# =========================================================
# CLI test
# =========================================================

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:

        print(
            'Usage: python retriever.py "question"'
        )

        raise SystemExit(1)

    question = " ".join(
        sys.argv[1:]
    )

    results = retrieve(
        question,
        limit=10,
    )

    print()
    print("=" * 80)
    print("HYBRID RETRIEVAL")
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
            f"{result.get('title', '')}"
        )

        print(
            f"Hybrid score: "
            f"{result.get('retrieval_score', 0.0):.4f}"
        )

        if result.get(
            "exact_match",
            False,
        ):

            print(
                "Exact title/heading match: YES"
            )

        print(
            f"Heading: "
            f"{result.get('heading', '')}"
        )

        print()

        print(
            result.get(
                "content",
                "",
            )[:1200]
        )
