import csv
import requests
import urllib.parse
import logging
from dotenv import load_dotenv
import os
import threading
import time
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

# ---------------- CONFIG ----------------

OUTPUT_FILE_PATH = r"C:\Users\Azath.A\os\adduser\output\output.txt"
TENANT_ID = "b7f9b193-c2fd-4efe-afb0-6a9485a2437a"
CSV_FILE_PATH = "input.csv"
BASE_URL = "https://wpp.os.wpp.com"

WORKERS = 20
PATCH_BATCH_SIZE = 50

env_path = r"C:\Users\Azath.A\os\auth.env"

# ----------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

load_dotenv(dotenv_path=env_path, override=True)

EMAIL_PATTERN = re.compile(
    r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
)

_thread_local = threading.local()
cache_lock = threading.Lock()
print_lock = threading.Lock()

# caches
group_cache = {}
fragment_cache = {}
email_cache = {}
group_id_to_name = {}

group_users = defaultdict(set)

output_file = open(OUTPUT_FILE_PATH, "w", encoding="utf-8")


# ---------------- UTIL ----------------

def safe_print(*args):

    msg = " ".join(map(str, args))

    with print_lock:

        print(msg)

        output_file.write(msg + "\n")

        output_file.flush()


def is_valid_email(email):

    return bool(EMAIL_PATTERN.fullmatch(email))


def get_session():

    if getattr(_thread_local, "session", None) is None:

        s = requests.Session()

        s.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        bearer = os.getenv("BEARER_TOKEN")

        if bearer:
            s.headers["Authorization"] = f"Bearer {bearer}"

        cookie = os.getenv("SESSION_COOKIE")

        if cookie:

            name = os.getenv("SESSION_COOKIE_NAME") or "session"

            s.cookies.set(name, cookie, path="/")

        _thread_local.session = s

    return _thread_local.session


# ---------------- RETRY ----------------

def retry(max_retries=3, backoff=1):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for i in range(max_retries):

                try:

                    return func(*args, **kwargs)

                except requests.exceptions.RequestException as e:

                    wait = backoff * (2 ** i)

                    logger.warning(
                        f"{func.__name__} retry {i + 1}: {e}"
                    )

                    time.sleep(wait)

            raise

        return wrapper

    return decorator


# ---------------- API CALLS ----------------

@retry()
def api_get_groups(name):

    s = get_session()

    url = (
        f"{BASE_URL}/api/tenants/{TENANT_ID}/groups"
        f"?page=1&itemsPerPage=50"
        f"&filter%5Bsearch%5D={urllib.parse.quote(name)}"
    )

    r = s.get(url, timeout=30)

    if r.status_code >= 500:
        raise requests.HTTPError(r.text)

    r.raise_for_status()

    return r.json()


@retry()
def api_get_users(search):

    s = get_session()

    url = (
        f"{BASE_URL}/api/users"
        f"?offset=0&limit=50"
        f"&filter%5Bsearch%5D={urllib.parse.quote(search)}"
    )

    r = s.get(url, timeout=30)

    if r.status_code >= 500:
        raise requests.HTTPError(r.text)

    r.raise_for_status()

    return r.json()


@retry()
def api_patch(group_id, group_name, users):

    s = get_session()

    url = f"{BASE_URL}/api/az/groups/users"

    payload = {
        "create": [
            {
                "groupId": group_id,
                "userId": u
            }
            for u in users
        ],
        "delete": []
    }

    r = s.patch(url, json=payload, timeout=30)

    if r.status_code >= 500:
        raise requests.HTTPError(r.text)

    return (
        group_name,
        group_id,
        users,
        r.status_code,
        r.text
    )


# ---------------- GROUP RESOLUTION ----------------

def resolve_group(name):

    with cache_lock:

        if name in group_cache:
            return group_cache[name]

    data = api_get_groups(name)

    gid = None

    for g in data.get("data", []):

        if g.get("name", "").lower() == name.lower():

            gid = g.get("id")

            break

    with cache_lock:

        group_cache[name] = gid

        if gid:
            group_id_to_name[gid] = name

    if gid:

        safe_print("GROUP FOUND,", name)

    else:

        safe_print("GROUP NOT FOUND,", name)

    return gid


# ---------------- USER RESOLUTION ----------------

def resolve_email(email):

    with cache_lock:

        if email in email_cache:
            return email_cache[email]

    fragment = email.split("@")[0]

    with cache_lock:

        if fragment in fragment_cache:

            matches = fragment_cache[fragment]

        else:

            matches = None

    if matches is None:

        data = api_get_users(fragment)

        matches = [
            u.get("email").lower()
            for u in data.get("data", [])
            if u.get("email")
        ]

        with cache_lock:
            fragment_cache[fragment] = matches

    exact_match = [u for u in matches if u == email]

    used_fragment = False

    if not exact_match:

        result = matches

        used_fragment = True

    else:

        result = exact_match

    with cache_lock:
        email_cache[email] = result

    if result:

        if used_fragment:

            safe_print(
                "USER FOUND WITH FRAGMENT,",
                email,
                "->",
                ",".join(result)
            )

        else:

            safe_print(
                "USER FOUND,",
                email,
                "->",
                ",".join(result)
            )

    else:

        safe_print("USER NOT FOUND,", email)

    return result


# ---------------- PROCESS ROW ----------------

def process_row(group, email):

    gid = resolve_group(group)

    if not gid:
        return

    users = resolve_email(email)

    if not users:
        return

    with cache_lock:

        for u in users:

            group_users[gid].add(u)


# ---------------- SINGLE USER PATCH ----------------

def patch_users_one_by_one(group_id, group_name, users):

    for user in users:

        try:

            (
                _,
                _,
                _,
                status,
                response
            ) = api_patch(
                group_id,
                group_name,
                [user]
            )

            if status == 201:

                safe_print(
                    f"SINGLE PATCH SUCCESS,"
                    f"{group_name} -> {user},"
                    f"(status {status})"
                )

            else:

                safe_print(
                    f"SINGLE PATCH FAILED,"
                    f"{group_name} -> {user},"
                    f"(status {status}),"
                    f"response={response}"
                )

        except Exception as e:

            safe_print(
                f"SINGLE PATCH ERROR,"
                f"{group_name} -> {user},"
                f"{e}"
            )


# ---------------- PATCH ----------------

def run_patch():

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:

        futures = []

        for gid, users in group_users.items():

            users = list(users)

            group_name = group_id_to_name.get(gid, gid)

            for i in range(0, len(users), PATCH_BATCH_SIZE):

                batch = users[i:i + PATCH_BATCH_SIZE]

                futures.append(
                    executor.submit(
                        api_patch,
                        gid,
                        group_name,
                        batch
                    )
                )

        for f in futures:

            try:

                (
                    group_name,
                    gid,
                    users,
                    status,
                    response
                ) = f.result()

                if status == 201:

                    safe_print(
                        f"PATCH SUCCESS,"
                        f"{group_name} -> "
                        f"{len(users)} users,"
                        f"(status {status})"
                    )

                else:

                    safe_print(
                        f"BATCH PATCH FAILED,"
                        f"{group_name} -> "
                        f"{len(users)} users,"
                        f"(status {status}),"
                        f"response={response}"
                    )

                    match = re.search(
                        r"email='([^']+)'",
                        response
                    )

                    if match:

                        bad_email = match.group(1)

                        safe_print(
                            f"REMOVING INVALID USER,"
                            f"{bad_email}"
                        )

                        remaining_users = [
                            u for u in users
                            if u != bad_email
                        ]

                        if remaining_users:

                            try:

                                (
                                    _,
                                    _,
                                    _,
                                    retry_status,
                                    retry_response
                                ) = api_patch(
                                    gid,
                                    group_name,
                                    remaining_users
                                )

                                if retry_status == 201:

                                    safe_print(
                                        f"RETRY SUCCESS,"
                                        f"{group_name} -> "
                                        f"{len(remaining_users)} users"
                                    )

                                else:

                                    safe_print(
                                        f"RETRY FAILED,"
                                        f"{group_name},"
                                        f"status={retry_status},"
                                        f"response={retry_response}"
                                    )

                                    patch_users_one_by_one(
                                        gid,
                                        group_name,
                                        remaining_users
                                    )

                            except Exception as e:

                                safe_print(
                                    f"RETRY ERROR,"
                                    f"{group_name},"
                                    f"{e}"
                                )

                    else:

                        patch_users_one_by_one(
                            gid,
                            group_name,
                            users
                        )

            except Exception as e:

                safe_print("PATCH ERROR,", e)


# ---------------- MAIN ----------------

def main():

    safe_print("Row,Value,Status")

    rows = []

    with open(CSV_FILE_PATH, encoding="utf-8") as f:

        reader = csv.reader(f)

        for r in reader:

            if len(r) < 2:
                continue

            group = r[0].strip()

            email = r[1].strip().lower()

            if not group:
                continue

            if not is_valid_email(email):

                safe_print("INVALID ROW:", r)

                continue

            rows.append((group, email))

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:

        futures = []

        for group, email in rows:

            futures.append(
                executor.submit(
                    process_row,
                    group,
                    email
                )
            )

        for f in futures:
            f.result()

    run_patch()

    safe_print("DONE")

    output_file.close()


if __name__ == "__main__":

    main()