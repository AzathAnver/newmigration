import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# File paths
env_path = r"C:\Users\Azath.A\os\auth.env"
csv_path = r"C:\Users\Azath.A\os\cg\input.csv"

# API URL
url = "https://dell.os.wpp.com/api/app-instances/templates/12915746-82ac-413a-8445-ff527ea1ff5b/apply/bulk"

MAX_WORKERS = 15
MAX_RETRIES = 5
RETRY_DELAY = 2  # seconds


# Read token + session
def get_env_values(file_path):
    token = None
    session_cookie = None

    with open(file_path, "r") as file:
        for line in file:
            if "BEARER_TOKEN" in line:
                token = line.strip().split("=", 1)[1]
            if "SESSION_COOKIE" in line:
                session_cookie = line.strip().split("=", 1)[1]

    return token, session_cookie


token, session_cookie = get_env_values(env_path)

if not token:
    print("❌ Bearer token not found!")
    exit()


def create_session():
    session = requests.Session()

    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": "https://dell.os.wpp.com",
        "Referer": "https://dell.os.wpp.com/",
        "User-Agent": "Mozilla/5.0"
    })

    if session_cookie:
        session.cookies.set("session", session_cookie)

    return session


def process_assignment(assignment_id):
    session = create_session()

    payload = {
        "appInstanceIds": [
            "f18ca484-6bca-4b30-b1b6-317167e0747e"
        ],
        "linkToHierarchy": True,
        "assignments": [
            {
                "assignmentId": assignment_id,
                "assignmentType": "WORKSPACE"
            }
        ]
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.post(url, json=payload, timeout=60)

            # Success
            if response.status_code < 500:
                return (
                    f"✅ {assignment_id} | "
                    f"Status={response.status_code} | "
                    f"{response.text}"
                )

            # Retry for 5XX
            print(
                f"🔄 Retry {attempt}/{MAX_RETRIES} "
                f"for {assignment_id} "
                f"(HTTP {response.status_code})"
            )

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

        except Exception as e:
            print(
                f"⚠️ Attempt {attempt}/{MAX_RETRIES} "
                f"failed for {assignment_id}: {e}"
            )

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                return f"❌ {assignment_id} | Error: {e}"

    return (
        f"❌ {assignment_id} | "
        f"Failed after {MAX_RETRIES} retries"
    )


# Read CSV
assignment_ids = []

with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        assignment_ids.append(row["assignmentId"].strip())

print(f"🚀 Processing {len(assignment_ids)} assignments with {MAX_WORKERS} workers")

# Run in parallel
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [
        executor.submit(process_assignment, assignment_id)
        for assignment_id in assignment_ids
    ]

    for future in as_completed(futures):
        print(future.result())

print("🎉 Completed")