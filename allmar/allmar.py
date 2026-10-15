import requests
import csv
import json
import pandas as pd
from dotenv import load_dotenv
import os
import sys
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

# ============================================================
# Configuration
# ============================================================

OUTPUT_FILE_PATH = r"C:\Users\Azath.A\os\allmar\output\output.txt"
LOCAL_MARKETS_PATH = r"C:\Users\Azath.A\os\market.json"
ENV_PATH = r"C:\Users\Azath.A\os\auth.env"

MAX_WORKERS = 10
MAX_RETRIES = 3          # Initial attempt + 2 retries
RETRY_DELAY = 30         # seconds

# ============================================================
# Output file + thread-safe printing
# ============================================================

output_file = open(OUTPUT_FILE_PATH, "w", encoding="utf-8")

_original_print = print
_print_lock = threading.Lock()


def print(*args, **kwargs):
    """
    Thread-safe print to both console and output file.
    """
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")

    message = sep.join(map(str, args)) + end

    with _print_lock:
        _original_print(message, end="")
        output_file.write(message)
        output_file.flush()


# ============================================================
# Environment
# ============================================================

def get_bearer_token() -> Optional[str]:
    load_dotenv(dotenv_path=ENV_PATH, override=True)
    return os.getenv("BEARER_TOKEN")


def get_session_cookie() -> Optional[str]:
    load_dotenv(dotenv_path=ENV_PATH, override=True)
    return os.getenv("SESSION_COOKIE")


# ============================================================
# Constants
# ============================================================

tenant_id = "4c039217-7d17-4207-8314-98348983718a"

hierarchy_url = (
    f"https://media.os.wpp.com/api/v2/tenants/"
    f"{tenant_id}/hierarchy-tree"
)

create_url = (
    f"https://media.os.wpp.com/_apps/os-workspaces/api/tenants/"
    f"{tenant_id}/organization-units?disableTenantCache=true"
)


# ============================================================
# File Readers
# ============================================================

def read_clients_from_csv(filename="clients.csv"):
    items = []

    with open(filename, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, start=2):
            client = (
                row.get("client_name")
                or row.get("client")
                or ""
            ).strip()

            market = (
                row.get("market")
                or row.get("country")
                or row.get("market_name")
                or ""
            ).strip()

            if client and market:
                items.append({
                    "client_name": client,
                    "market": market
                })
            else:
                print(
                    f"⚠️ Skipping row {i}: "
                    f"need 'client_name' and 'market'. Row={row}"
                )

    return items


# ============================================================
# Load local markets file
# ============================================================

def load_local_markets(path=LOCAL_MARKETS_PATH):
    """
    Robust loader for market.json supporting:
    - proper JSON array
    - malformed repeated id/name blocks
    - line-by-line JSON
    """

    name_to_id = {}
    alt_to_id = {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            print(f"⚠️ Local markets file is empty: {path}")
            return name_to_id, alt_to_id

        # ----------------------------------------------------
        # 1. Try normal JSON first
        # ----------------------------------------------------

        try:
            parsed = json.loads(content)

            if isinstance(parsed, list):
                for item in parsed:
                    if not isinstance(item, dict):
                        continue

                    _id = item.get("id")
                    _name = item.get("name")

                    if _id and _name:
                        name_to_id[
                            _name.strip().lower()
                        ] = _id

                return name_to_id, alt_to_id

        except Exception:
            pass

        # ----------------------------------------------------
        # 2. Fallback: manually extract id/name pairs
        # ----------------------------------------------------

        parts = content.replace("\n", " ").split('"id"')

        for part in parts[1:]:
            try:
                q1 = part.find('"')
                q2 = part.find('"', q1 + 1)

                _id = part[q1 + 1:q2]

                name_idx = part.find('"name"')

                if name_idx != -1:
                    after = part[name_idx:]

                    nq1 = after.find(
                        '"',
                        after.find(":") + 1
                    )

                    nq2 = after.find('"', nq1 + 1)

                    _name = after[nq1 + 1:nq2]

                    if _id and _name:
                        name_to_id[
                            _name.strip().lower()
                        ] = _id

            except Exception:
                continue

        if not name_to_id:
            print(
                f"⚠️ Could not parse local markets file: {path}"
            )

    except FileNotFoundError:
        print(
            f"❌ Local markets file not found at: {path}"
        )

    except Exception as e:
        print(
            f"❌ Error loading local markets file: {e}"
        )

    return name_to_id, alt_to_id


_name_to_id_map, _alt_to_id_map = load_local_markets()


def get_market_md_id_local(
    market_name: str
) -> Optional[str]:

    if not market_name:
        return None

    key = market_name.strip().lower()

    if key in _name_to_id_map:
        return _name_to_id_map[key]

    if key in _alt_to_id_map:
        return _alt_to_id_map[key]

    for name, _id in _name_to_id_map.items():
        if key in name or name in key:
            return _id

    return None


# ============================================================
# Load CSV
# ============================================================

rows = read_clients_from_csv("clients.csv")

if not rows:
    print("❌ No valid rows found in clients.csv.")
    output_file.close()
    sys.exit(1)


# ============================================================
# Load hierarchy
# ============================================================

try:
    bearer_token = get_bearer_token()
    session_cookie_value = get_session_cookie()

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "python-requests/2.31"
    }

    cookies = {}

    if session_cookie_value:
        cookies["session"] = session_cookie_value

    resp = requests.get(
        hierarchy_url,
        headers=headers,
        cookies=cookies,
        timeout=30
    )

    resp.raise_for_status()

except requests.RequestException as e:
    print(f"❌ Failed to load hierarchy: {e}")
    output_file.close()
    sys.exit(1)


hierarchy = resp.json().get("mapping", {})


# ============================================================
# CLIENT-only AZID lookup
# ============================================================

client_org_by_name = {}

for item in hierarchy.values():

    if not isinstance(item, dict):
        continue

    raw_name = item.get("name")

    if raw_name and isinstance(raw_name, str):

        name = raw_name.strip().lower()

        if item.get("type") == "CLIENT" and name:
            client_org_by_name[name] = item


# ============================================================
# POST function with retries
# ============================================================

def create_org_unit(row):
    """
    Creates an organization unit.

    Retries on:
      - HTTP 4xx
      - HTTP 5xx
      - Network/RequestException

    Waits 30 seconds between retries.

    Returns a result dictionary.
    """

    client_name = row["client_name"]
    market_name = row["market"]

    print("=" * 60)
    print(
        f"🔍 Processing client: "
        f"{client_name} | market: {market_name}"
    )

    # --------------------------------------------------------
    # Find parent CLIENT
    # --------------------------------------------------------

    parent = client_org_by_name.get(
        client_name.strip().lower()
    )

    if not parent:
        message = (
            f"⚠️ Not found in hierarchy "
            f"(CLIENT type): {client_name}"
        )

        print(message)

        return {
            "success": False,
            "client": client_name,
            "market": market_name,
            "status": None,
            "message": message
        }

    parent_id = parent["azId"]

    # --------------------------------------------------------
    # Resolve market mdId
    # --------------------------------------------------------

    md_id = get_market_md_id_local(market_name)

    if not md_id:

        message = (
            f"❌ No mdId resolved for market "
            f"'{market_name}'. Skipping {client_name}."
        )

        print(message)

        return {
            "success": False,
            "client": client_name,
            "market": market_name,
            "status": None,
            "message": message
        }

    # --------------------------------------------------------
    # Payload
    # --------------------------------------------------------

    payload = {
        "type": "predefined",
        "parentId": parent_id,
        "categories": [],
        "data": {
            "mdId": md_id
        }
    }

    # --------------------------------------------------------
    # Headers / cookies
    # --------------------------------------------------------

    post_headers = {
        "Authorization": f"Bearer {get_bearer_token()}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "python-requests/2.31"
    }

    post_cookies = {}

    session_cookie_value = get_session_cookie()

    if session_cookie_value:
        post_cookies["session"] = session_cookie_value

    # --------------------------------------------------------
    # Retry loop
    # --------------------------------------------------------

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            print(
                f"🚀 Attempt {attempt}/{MAX_RETRIES}: "
                f"{client_name} -> {market_name}"
            )

            create_resp = requests.post(
                create_url,
                headers=post_headers,
                cookies=post_cookies,
                json=payload,
                timeout=30
            )

            status_code = create_resp.status_code

            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            if status_code == 201:

                print(
                    f"✅ Successfully created org-unit "
                    f"for {client_name} -> {market_name}"
                )

                return {
                    "success": True,
                    "client": client_name,
                    "market": market_name,
                    "status": status_code,
                    "message": "Created"
                }

            # ------------------------------------------------
            # ALREADY EXISTS
            # ------------------------------------------------

            elif status_code == 409:

                print(
                    f"ℹ️ Org-unit already exists for "
                    f"{client_name} -> {market_name}"
                )

                try:
                    print(create_resp.json())
                except Exception:
                    print(create_resp.text)

                return {
                    "success": True,
                    "client": client_name,
                    "market": market_name,
                    "status": status_code,
                    "message": "Already exists"
                }

            # ------------------------------------------------
            # 4xx / 5xx -> RETRY
            # ------------------------------------------------

            elif 400 <= status_code <= 599:

                print(
                    f"⚠️ HTTP {status_code} for "
                    f"{client_name} -> {market_name}"
                )

                try:
                    error_body = create_resp.json()
                    print(error_body)
                except Exception:
                    print(create_resp.text)

                # Retry if attempts remain
                if attempt < MAX_RETRIES:

                    print(
                        f"⏳ Retrying in {RETRY_DELAY} seconds..."
                    )

                    time.sleep(RETRY_DELAY)

                    continue

                # No retries left
                print(
                    f"❌ Failed after {MAX_RETRIES} attempts: "
                    f"{client_name} -> {market_name}"
                )

                return {
                    "success": False,
                    "client": client_name,
                    "market": market_name,
                    "status": status_code,
                    "message": "Failed after retries"
                }

            # ------------------------------------------------
            # Unexpected status
            # ------------------------------------------------

            else:

                print(
                    f"❌ Unexpected HTTP status "
                    f"{status_code} for "
                    f"{client_name} -> {market_name}"
                )

                try:
                    print(create_resp.json())
                except Exception:
                    print(create_resp.text)

                return {
                    "success": False,
                    "client": client_name,
                    "market": market_name,
                    "status": status_code,
                    "message": "Unexpected status"
                }

        # ----------------------------------------------------
        # Network error -> retry
        # ----------------------------------------------------

        except requests.RequestException as e:

            print(
                f"⚠️ Network error on attempt "
                f"{attempt}/{MAX_RETRIES} for "
                f"{client_name} -> {market_name}: {e}"
            )

            if attempt < MAX_RETRIES:

                print(
                    f"⏳ Retrying in {RETRY_DELAY} seconds..."
                )

                time.sleep(RETRY_DELAY)

                continue

            print(
                f"❌ Network request failed after "
                f"{MAX_RETRIES} attempts: "
                f"{client_name} -> {market_name}"
            )

            return {
                "success": False,
                "client": client_name,
                "market": market_name,
                "status": None,
                "message": str(e)
            }

    # Should never reach here
    return {
        "success": False,
        "client": client_name,
        "market": market_name,
        "status": None,
        "message": "Unknown error"
    }


# ============================================================
# Multithread processing
# ============================================================

print("=" * 60)
print(
    f"🚀 Starting processing of {len(rows)} rows "
    f"with {MAX_WORKERS} workers"
)
print(
    f"🔁 Max attempts per request: {MAX_RETRIES}"
)
print(
    f"⏱️ Retry delay: {RETRY_DELAY} seconds"
)
print("=" * 60)


results = []

with ThreadPoolExecutor(
    max_workers=MAX_WORKERS
) as executor:

    # Submit all jobs
    future_to_row = {
        executor.submit(create_org_unit, row): row
        for row in rows
    }

    # Collect completed jobs
    for future in as_completed(future_to_row):

        row = future_to_row[future]

        try:

            result = future.result()
            results.append(result)

        except Exception as e:

            print(
                f"❌ Unexpected worker error for "
                f"{row['client_name']} -> "
                f"{row['market']}: {e}"
            )

            results.append({
                "success": False,
                "client": row["client_name"],
                "market": row["market"],
                "status": None,
                "message": str(e)
            })


# ============================================================
# Summary
# ============================================================

successful = sum(
    1 for r in results
    if r.get("success")
)

failed = len(results) - successful

print("=" * 60)
print("🏁 Processing completed")
print(f"📊 Total rows : {len(rows)}")
print(f"✅ Successful : {successful}")
print(f"❌ Failed     : {failed}")
print("=" * 60)


if failed:
    print("\n❌ Failed items:")

    for result in results:

        if not result.get("success"):

            print(
                f"   - {result.get('client')} -> "
                f"{result.get('market')} | "
                f"HTTP={result.get('status')} | "
                f"{result.get('message')}"
            )


# ============================================================
# Close output
# ============================================================

output_file.close()