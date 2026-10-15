from pathlib import Path
import re
import sqlite3
from datetime import datetime


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

COURSE_ROOT = Path(r"C:\Users\Azath.A\courses\Campaign_Management")
CONFLUENCE_ROOT = Path(r"C:\Users\Azath.A\confluence\SUP_notebooklm_v3")

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "campaign_knowledge.db"

CHUNK_SIZE = 1800
CHUNK_OVERLAP = 250


# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

def create_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    # Enable foreign keys.
    conn.execute("PRAGMA foreign_keys = ON")

    # -----------------------------------------------------
    # Documents table
    # -----------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type TEXT NOT NULL,
            source_file TEXT NOT NULL UNIQUE,
            title TEXT,
            page_id TEXT,
            confluence_url TEXT,
            relative_path TEXT,
            modified_time TEXT
        )
    """)

    # -----------------------------------------------------
    # Chunks table
    # -----------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL,
            heading TEXT,
            content TEXT NOT NULL,
            FOREIGN KEY(document_id) REFERENCES documents(id)
        )
    """)

    # -----------------------------------------------------
    # IMPORTANT:
    #
    # The old chunks_fts table may have a different schema.
    # SQLite CREATE TABLE IF NOT EXISTS does NOT update an
    # existing table.
    #
    # So remove the old FTS table and recreate it with the
    # current schema.
    # -----------------------------------------------------

    conn.execute("""
        DROP TABLE IF EXISTS chunks_fts
    """)

    conn.execute("""
        CREATE VIRTUAL TABLE chunks_fts
        USING fts5(
            content,
            heading
        )
    """)

    conn.commit()

    return conn


# ---------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------

def read_text(path: Path) -> str:
    raw = path.read_bytes()

    # Handle BOM-based Unicode files first.
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        try:
            text = raw.decode("utf-16")
        except UnicodeDecodeError:
            text = raw.decode("utf-16", errors="replace")

    elif raw.startswith(b"\xef\xbb\xbf"):
        text = raw.decode("utf-8-sig")

    else:
        encodings = [
            "utf-8",
            "cp1252",
            "latin-1",
        ]

        for encoding in encodings:
            try:
                text = raw.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            text = raw.decode(
                "utf-8",
                errors="replace",
            )

    # Repair common mojibake caused by UTF-8 decoded as cp1252.
    if "â" in text or "Ã" in text or "ð" in text:
        try:
            repaired = (
                text
                .encode("cp1252")
                .decode("utf-8")
            )
            text = repaired
        except (
            UnicodeEncodeError,
            UnicodeDecodeError,
        ):
            pass

    return text



# ---------------------------------------------------------
# Metadata
# ---------------------------------------------------------

def extract_title(text: str, path: Path) -> str:
    """
    Extract the first Markdown H1 as the title.
    If no H1 exists, use the first non-empty line.
    """

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("# "):
            return line[2:].strip()

        if line:
            return line[:200]

    return path.stem


def extract_confluence_metadata(text: str, path: Path):
    """
    Extract Confluence page ID and URL.
    """

    page_id = None
    url = None

    # Page ID from filename.
    # Example:
    # 123456789_My_Page.md
    match = re.match(r"^(\d+)_", path.name)

    if match:
        page_id = match.group(1)

    # URL from Markdown.
    # Example:
    # **Confluence page:** [Page Title](https://...)
    url_match = re.search(
        r"\*\*Confluence page:\*\*\s*\[.*?\]\((https?://[^)]+)\)",
        text,
        re.IGNORECASE,
    )

    if url_match:
        url = url_match.group(1)

    return page_id, url


# ---------------------------------------------------------
# Chunking
# ---------------------------------------------------------

def chunk_markdown(text: str):
    """
    Split Markdown into chunks while attempting to preserve
    heading context and maintain overlap between chunks.

    Returns:
        list[tuple[str, str]]
        [(heading, content), ...]
    """

    lines = text.splitlines()

    chunks = []

    current_heading = ""
    current_lines = []
    current_size = 0

    for line in lines:

        heading_match = re.match(
            r"^\s{0,3}#{1,6}\s+(.+)$",
            line
        )

        # -------------------------------------------------
        # New heading
        # -------------------------------------------------

        if heading_match:

            if current_lines:
                content = "\n".join(current_lines).strip()

                if content:
                    chunks.append(
                        (
                            current_heading,
                            content
                        )
                    )

            current_heading = heading_match.group(1).strip()

            current_lines = [line]
            current_size = len(line)

            continue

        # -------------------------------------------------
        # Normal line
        # -------------------------------------------------

        current_lines.append(line)
        current_size += len(line) + 1

        # -------------------------------------------------
        # Chunk reached target size
        # -------------------------------------------------

        if current_size >= CHUNK_SIZE:

            content = "\n".join(current_lines).strip()

            if content:
                chunks.append(
                    (
                        current_heading,
                        content
                    )
                )

            # -------------------------------------------------
            # Build character-based overlap.
            #
            # We keep the last CHUNK_OVERLAP characters from
            # the current chunk rather than always keeping
            # five lines.
            # -------------------------------------------------

            overlap_text = content[-CHUNK_OVERLAP:]

            # Start the next chunk with the overlap.
            current_lines = [overlap_text]
            current_size = len(overlap_text)

    # ---------------------------------------------------------
    # Add final chunk
    # ---------------------------------------------------------

    if current_lines:

        content = "\n".join(current_lines).strip()

        if content:

            chunks.append(
                (
                    current_heading,
                    content
                )
            )

    return chunks


# ---------------------------------------------------------
# Index one file
# ---------------------------------------------------------

def index_file(
    conn,
    path: Path,
    source_type: str,
    root: Path
):
    """
    Index a single Markdown/text file.
    """

    text = read_text(path)

    if not text.strip():
        return 0

    title = extract_title(
        text,
        path
    )

    page_id = None
    confluence_url = None

    if source_type == "confluence":

        page_id, confluence_url = (
            extract_confluence_metadata(
                text,
                path
            )
        )

    relative_path = str(
        path.relative_to(root)
    )

    modified_time = datetime.fromtimestamp(
        path.stat().st_mtime
    ).isoformat()

    # ---------------------------------------------------------
    # Insert or update document
    # ---------------------------------------------------------

    conn.execute(
        """
        INSERT INTO documents (
            source_type,
            source_file,
            title,
            page_id,
            confluence_url,
            relative_path,
            modified_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(source_file)
        DO UPDATE SET
            source_type = excluded.source_type,
            title = excluded.title,
            page_id = excluded.page_id,
            confluence_url = excluded.confluence_url,
            relative_path = excluded.relative_path,
            modified_time = excluded.modified_time
        """,
        (
            source_type,
            str(path),
            title,
            page_id,
            confluence_url,
            relative_path,
            modified_time,
        ),
    )

    # ---------------------------------------------------------
    # Get document ID
    # ---------------------------------------------------------

    row = conn.execute(
        """
        SELECT id
        FROM documents
        WHERE source_file = ?
        """,
        (str(path),),
    ).fetchone()

    if row is None:
        raise RuntimeError(
            f"Could not retrieve document ID for: {path}"
        )

    document_id = row[0]

    # ---------------------------------------------------------
    # Remove previous chunks
    # ---------------------------------------------------------

    conn.execute(
        """
        DELETE FROM chunks
        WHERE document_id = ?
        """,
        (document_id,),
    )

    # ---------------------------------------------------------
    # Create chunks
    # ---------------------------------------------------------

    chunks = chunk_markdown(text)

    # ---------------------------------------------------------
    # Insert chunks
    # ---------------------------------------------------------

    for index, (heading, content) in enumerate(chunks):

        conn.execute(
            """
            INSERT INTO chunks (
                document_id,
                chunk_index,
                heading,
                content
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                document_id,
                index,
                heading,
                content,
            ),
        )

    return len(chunks)


# ---------------------------------------------------------
# Rebuild FTS index
# ---------------------------------------------------------

def rebuild_fts(conn):
    """
    Rebuild the SQLite FTS5 search index from chunks.
    """

    print("Clearing FTS index...")

    conn.execute("""
        DELETE FROM chunks_fts
    """)

    print("Populating FTS index...")

    conn.execute("""
        INSERT INTO chunks_fts (
            rowid,
            content,
            heading
        )
        SELECT
            id,
            content,
            heading
        FROM chunks
    """)

    conn.commit()

    print("FTS index rebuilt successfully.")

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    conn = create_database()

    total_files = 0
    total_chunks = 0

    sources = [
        (
            COURSE_ROOT,
            "course"
        ),
        (
            CONFLUENCE_ROOT,
            "confluence"
        ),
    ]

    # -----------------------------------------------------
    # Scan sources
    # -----------------------------------------------------

    for root, source_type in sources:

        print()
        print("=" * 60)
        print(f"Scanning {source_type}")
        print(f"Root: {root}")
        print("=" * 60)

        if not root.exists():

            print(
                f"[WARNING] Directory does not exist: {root}"
            )

            continue

        for path in root.rglob("*"):

            if not path.is_file():
                continue

            if path.suffix.lower() not in {
                ".md",
                ".txt",
            }:
                continue

            try:

                chunks = index_file(
                    conn=conn,
                    path=path,
                    source_type=source_type,
                    root=root,
                )

                total_files += 1
                total_chunks += chunks

                print(
                    f"[OK] "
                    f"{source_type:10} "
                    f"{path.name[:70]} "
                    f"({chunks} chunks)"
                )

            except Exception as exc:

                print(
                    f"[ERROR] {path}: {exc}"
                )

    # -----------------------------------------------------
    # Commit document/chunk changes
    # -----------------------------------------------------

    conn.commit()

    # -----------------------------------------------------
    # Rebuild FTS
    # -----------------------------------------------------

    print()
    print("Rebuilding FTS index...")

    rebuild_fts(conn)

    # -----------------------------------------------------
    # Close database
    # -----------------------------------------------------

    conn.close()

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    print()
    print("=" * 60)
    print("INDEXING COMPLETE")
    print("=" * 60)

    print(
        f"Documents : {total_files}"
    )

    print(
        f"Chunks    : {total_chunks}"
    )

    print(
        f"Database  : {DB_PATH}"
    )


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
