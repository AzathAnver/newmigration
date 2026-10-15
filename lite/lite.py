import os
import sys
import csv
import json
import time
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from dotenv import load_dotenv

# =====================================================
# Output logging setup
# =====================================================
OUTPUT_FILE_PATH = r"C:\Users\Azath.A\os\lite\output\output.txt"
output_file = open(OUTPUT_FILE_PATH, "w", encoding="utf-8")

_original_print = print
print_lock = threading.Lock()

def print(*args, **kwargs):
    with print_lock:
        _original_print(*args, **kwargs)
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        output_file.write(sep.join(map(str, args)) + end)
        output_file.flush()

# =====================================================
# Static config
# =====================================================
TENANT_ID = "4c039217-7d17-4207-8314-98348983718a"
TEMPLATE_ID = "15207128-819e-4607-a036-9dc530032676"
BULK_URL = f"https://media.os.wpp.com/api/app-instances/templates/{TEMPLATE_ID}/apply/bulk"

INPUT_CSV = r"C:\Users\Azath.A\os\lite\clients.csv"
ENV_PATH = r"C:\Users\Azath.A\os\auth.env"

TIMEOUT = 30
MAX_WORKERS = 10
MAX_RETRIES = 3
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}

# =====================================================
# Helpers
# =====================================================
def norm(s: str) -> str:
    return (s or "").strip().lower()

def load_auth():
    load_dotenv(dotenv_path=ENV_PATH)
    bearer = os.getenv("BEARER_TOKEN")
    session_cookie = os.getenv("SESSION_COOKIE")

    if not bearer and not session_cookie:
        print("ERROR: Missing auth", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "python-requests/2.x",
    }
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"

    cookies = {"session": session_cookie} if session_cookie else {}
    return headers, cookies

def fetch_tree(headers, cookies):
    url = f"https://media.os.wpp.com/api/v2/tenants/{TENANT_ID}/hierarchy-tree"
    resp = requests.get(url, headers=headers, cookies=cookies, timeout=TIMEOUT)
    resp.raise_for_status()
    mapping = resp.json().get("mapping", {}) or {}
    return {
        az: ({**node, "azId": az} if "azId" not in node else node)
        for az, node in mapping.items()
    }

def find_client(nodes, client_name):
    client_n = norm(client_name)
    for n in nodes.values():
        if n.get("type") == "CLIENT" and norm(n.get("name")) == client_n:
            return n
    return None

def bfs_collect(nodes, start_ids, type_name=None, name=None):
    want_type = type_name.upper() if type_name else None
    want_name = norm(name) if name else None

    seen, out = set(), []
    q = deque(start_ids or [])

    while q:
        az = q.popleft()
        if az in seen:
            continue
        seen.add(az)

        node = nodes.get(az)
        if not node:
            continue

        if ((not want_type or node.get("type") == want_type) and
            (not want_name or norm(node.get("name")) == want_name)):
            out.append(node)

        q.extend(node.get("children") or [])

    return out

# =====================================================
# CATEGORY-INDEPENDENT BRAND RESOLUTION
# =====================================================
def resolve_brand_azid(nodes, market, client, brand):
    client_node = find_client(nodes, client)
    if not client_node:
        raise ValueError(f"Client not found: {client}")

    markets = bfs_collect(nodes, client_node.get("children"), "MARKET", market)
    if not markets:
        raise ValueError(f"Market not found: {market}")

    candidates = []
    for m in markets:
        brands = bfs_collect(nodes, m.get("children"), "BRAND", brand)
        candidates.extend(brands)

    if not candidates:
        raise ValueError(f"Brand not found: {brand}")

    return sorted(candidates, key=lambda x: x["azId"])[0]["azId"]

def read_csv_rows(path):
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for idx, r in enumerate(reader):
            rows.append((
                idx,
                r["Market"].strip(),
                r["Client"].strip(),
                r["Brand"].strip(),
                r["Category"].strip()  # kept for logging only
            ))
    return rows

# =====================================================
# API with retry
# =====================================================
def post_apply_bulk(headers, cookies, assignment_id):
    payload = {
        "linkToHierarchy": True,
        "assignments": [{"assignmentId": assignment_id, "assignmentType": "WORKSPACE"}]
    }

    for attempt in range(1, MAX_RETRIES + 1):
        resp = requests.post(
            BULK_URL,
            headers=headers,
            cookies=cookies,
            json=payload,
            timeout=TIMEOUT
        )

        if resp.status_code < 400:
            return payload, resp.status_code, resp.json(), attempt

        if resp.status_code not in RETRY_STATUS_CODES:
            break

        time.sleep(2 ** attempt)

    try:
        body = resp.json()
    except Exception:
        body = resp.text

    return payload, resp.status_code, body, attempt

# =====================================================
# Worker
# =====================================================
def process_row(row, headers, cookies, nodes):
    idx, market, client, brand, category = row
    start = time.time()

    try:
        azid = resolve_brand_azid(nodes, market, client, brand)
        payload, status, body, retries = post_apply_bulk(headers, cookies, azid)

        return idx, {
            "row": {"Market": market, "Client": client, "Brand": brand, "Category": category},
            "status": status,
            "retries": retries - 1,
            "time_sec": round(time.time() - start, 2),
            "response": body
        }

    except Exception as e:
        return idx, {
            "row": {"Market": market, "Client": client, "Brand": brand, "Category": category},
            "status": "FAILED",
            "error": str(e),
            "time_sec": round(time.time() - start, 2)
        }

# =====================================================
# Main
# =====================================================
def main():
    headers, cookies = load_auth()
    nodes = fetch_tree(headers, cookies)
    rows = read_csv_rows(INPUT_CSV)

    results = {}
    success = failure = 0

    print(f"🚀 Processing {len(rows)} rows with {MAX_WORKERS} workers")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as exe:
        futures = [exe.submit(process_row, r, headers, cookies, nodes) for r in rows]

        for f in as_completed(futures):
            idx, res = f.result()
            results[idx] = res

            if res.get("status") == 200:
                success += 1
            else:
                failure += 1

    print("\n📄 Ordered Results")
    for i in range(len(results)):
        print(json.dumps(results[i], ensure_ascii=False))

    print("\n📊 FINAL SUMMARY")
    print(json.dumps({
        "total": len(rows),
        "success": success,
        "failed": failure
    }, indent=2))

if __name__ == "__main__":
    main()
    output_file.close()
