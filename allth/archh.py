import requests
from dotenv import load_dotenv
import os
import concurrent.futures
import threading
import time

# --- Configuration ---
TENANT_ID = "4c039217-7d17-4207-8314-98348983718a"
HIERARCHY_URL = f"https://media.os.wpp.com/api/v2/tenants/{TENANT_ID}/hierarchy-tree"
PATCH_URL = "https://media.os.wpp.com/api/az/groups/roles"

# The three roles you want to add (each will be its own PATCH call)
ROLE_IDS = [
    ("CGOV_STANDARD", "9e7c812c-c063-4613-9776-31f635bd1c03"),
    ("Architect User", "6948d8e6-eca6-4c12-9241-a47db34db467"),
    ("Hierarchy Access", "1544916c-0ce0-4042-a8e5-6e18042c73b7"),
]

STATIC_GROUP_ID = "fe4b90bd-0c38-4d5c-b0cb-8f8f9e791e39"

# Threading
MAX_WORKERS = 15

# --- Load environment ---
env_path = r"C:\Users\Azath.A\os\auth.env"
load_dotenv(dotenv_path=env_path)

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
SESSION_COOKIE = os.getenv("SESSION_COOKIE")

if not BEARER_TOKEN or not SESSION_COOKIE:
    raise ValueError("❌ Missing BEARER_TOKEN or SESSION_COOKIE in .env file")

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "python-requests/2.31"
}

COOKIES = {
    "session": SESSION_COOKIE
}

# --- Fetch hierarchy to get account_uid (azId) for each brand ---
print("🔍 Fetching hierarchy data...")
response = requests.get(HIERARCHY_URL, headers=HEADERS, cookies=COOKIES, timeout=30)

if response.status_code != 200:
    print(f"❌ Failed to fetch hierarchy: {response.status_code} - {response.text}")
    exit(1)

data = response.json()
mapping = data.get("mapping", {})

# --- Read brand names from file ---
txt_file_path = r"C:\Users\Azath.A\os\allth\brands.txt"
try:
    with open(txt_file_path, "r", encoding="utf-8") as file:
        brand_names = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print(f"❌ brands.txt not found at {txt_file_path}")
    exit(1)

print(f"📄 Loaded {len(brand_names)} brand(s) from file.")

# --- Build CLIENT-only lookup ---
client_org_by_name = {
    item.get("name", "").strip().lower(): item
    for item in mapping.values()
    if item.get("type") == "CLIENT" and item.get("name")
}

# --- Match brands (now treated as client names) to account_uids ---
accounts_to_assign = []

for brand in brand_names:
    matched_item = client_org_by_name.get(brand.strip().lower())

    if matched_item:
        account_uid = matched_item.get("azId")
        if account_uid:
            accounts_to_assign.append({
                "brand_name": brand,
                "account_id": account_uid
            })
            print(f"✅ Matched '{brand}' → account_uid: {account_uid}")
        else:
            print(f"⚠️ No azId found for brand: {brand}")
    else:
        print(f"⚠️ Brand '{brand}' not found in hierarchy.")

if not accounts_to_assign:
    print("🚫 No valid accounts found to assign. Exiting.")
    exit(0)

# --- Thread-safe counters and storage ---
lock = threading.Lock()
summary = {
    "total_role_calls": 0,
    "success": 0,
    "skipped_422": 0,
    "failed": 0,
    "details": []  # optional list of dicts with per-call detail
}

def patch_role_for_account(group_id: str, role_id: str, account_id: str, brand_name: str, max_retries=2):
    """
    Make a single PATCH call to assign one role to one account.
    Returns tuple(status: str, http_code: int, response_text_or_json)
    status is one of: "success", "skipped", "failed"
    """
    payload = {
        "create": [{
            "group_id": group_id,
            "role_id": role_id,
            "account_id": account_id
        }],
        "delete": []
    }

    attempt = 0
    while attempt <= max_retries:
        attempt += 1
        try:
            resp = requests.patch(PATCH_URL, headers=HEADERS, cookies=COOKIES, json=payload, timeout=30)
        except requests.RequestException as e:
            # Network issue — retry
            if attempt <= max_retries:
                wait = 1.5 * attempt
                print(f"⚠️ Network error for {brand_name} role {role_id} (attempt {attempt}/{max_retries}). Retrying in {wait}s...")
                time.sleep(wait)
                continue
            else:
                return ("failed", None, f"Network error after {attempt} attempts: {e}")

        code = resp.status_code
        if code == 201:
            try:
                result = resp.json()
            except Exception:
                result = resp.text
            return ("success", code, result)
        elif code == 422:
            # already exists or validation error
            try:
                err = resp.json().get("message", resp.text)
            except Exception:
                err = resp.text
            return ("skipped", code, err)
        elif 500 <= code < 600 and attempt <= max_retries:
            # server error — retry
            wait = 1.5 * attempt
            print(f"⚠️ Server error {code} for {brand_name} role {role_id} (attempt {attempt}/{max_retries}). Retrying in {wait}s...")
            time.sleep(wait)
            continue
        else:
            # Other client errors or unhandled codes
            return ("failed", code, resp.text)

    return ("failed", None, "Exceeded retries")

def process_account(item):
    brand = item["brand_name"]
    account_id = item["account_id"]
    per_account_results = []

    print(f"\n➡️ Worker starting: {brand} (account_id: {account_id})")

    for role_name, role_id in ROLE_IDS:
        with lock:
            summary["total_role_calls"] += 1

        status, code, info = patch_role_for_account(STATIC_GROUP_ID, role_id, account_id, brand)

        # thread-safe summary updates
        with lock:
            entry = {
                "brand": brand,
                "account_id": account_id,
                "role_name": role_name,
                "role_id": role_id,
                "status": status,
                "http_code": code,
                "info": info
            }
            summary["details"].append(entry)
            per_account_results.append(entry)

            if status == "success":
                summary["success"] += 1
                print(f"  ✅ [{role_name}] Assigned to {brand} (role_id: {role_id})")
            elif status == "skipped":
                summary["skipped_422"] += 1
                print(f"  🔶 [{role_name}] Already exists or validation issue for {brand}: {info}")
            else:
                summary["failed"] += 1
                print(f"  ❌ [{role_name}] FAILED for {brand} (code={code}) — {info}")

    return per_account_results

# --- Run multithreaded processing ---
print(f"\n🚀 Starting assignments in parallel with {MAX_WORKERS} workers...")

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(process_account, acct) for acct in accounts_to_assign]
    # Optionally iterate as they complete to show progress
    for fut in concurrent.futures.as_completed(futures):
        # we don't need the return value here because details are stored in summary
        try:
            _ = fut.result()
        except Exception as e:
            with lock:
                summary["failed"] += 1
            print(f"❌ Worker raised exception: {e}")

# --- Final Summary ---
print("\n" + "="*60)
print("✅ ASSIGNMENT SUMMARY:")
print(f"   Brands processed: {len(accounts_to_assign)}")
print(f"   Total role PATCH calls attempted: {summary['total_role_calls']}")
print(f"   Success: {summary['success']}")
print(f"   Skipped (422): {summary['skipped_422']}")
print(f"   Failed: {summary['failed']}")
print("="*60)

# Optional: write detailed log to file
log_file = r"C:\Users\Azath.A\os\allth\assignment_details.log"
try:
    with open(log_file, "w", encoding="utf-8") as lf:
        import json
        json.dump(summary, lf, ensure_ascii=False, indent=2)
    print(f"📝 Detailed per-call log written to: {log_file}")
except Exception as e:
    print(f"⚠️ Could not write log file: {e}")
