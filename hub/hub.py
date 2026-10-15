import os
import csv
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

GROUP_ID = "eb6a210f-ec73-4b48-b6c8-5ad1af3a5a91"
HUB_ID = "933a5e69-207c-446e-9c25-01ce754233ce"

BASE_URL = "https://media.os.wpp.com"
INPUT_CSV = "input.csv"

env_path = r"C:\Users\Azath.A\os\auth.env"
load_dotenv(dotenv_path=env_path, override=True)


def create_session():
    session = requests.Session()

    retry_strategy = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["PATCH"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })

    bearer = os.getenv("BEARER_TOKEN")
    if bearer:
        session.headers["Authorization"] = f"Bearer {bearer}"

    cookie = os.getenv("SESSION_COOKIE")
    if cookie:
        name = os.getenv("SESSION_COOKIE_NAME") or "session"
        session.cookies.set(name, cookie, path="/")

    return session


def add_user(email):
    session = create_session()

    # ---------------------------------------------------------
    # API 1: Add user to group
    # ---------------------------------------------------------
    group_payload = {
        "create": [
            {
                "groupId": GROUP_ID,
                "userId": email
            }
        ],
        "delete": []
    }

    try:
        group_response = session.patch(
            f"{BASE_URL}/api/az/groups/users",
            json=group_payload,
            timeout=30
        )

        group_result = {
            "status": group_response.status_code,
            "response": group_response.text
        }

    except Exception as e:
        return {
            "email": email,
            "group_status": "ERROR",
            "group_response": str(e),
            "hub_status": "NOT_RUN",
            "hub_response": "Skipped because group API failed"
        }

    # ---------------------------------------------------------
    # API 2: Set user's preferred hub
    # ---------------------------------------------------------
    hub_payload = {
        "userPreferredHub": [
            {
                "hubId": HUB_ID,
                "userEmail": email
            }
        ]
    }

    try:
        hub_response = session.patch(
            f"{BASE_URL}/api/users/hubs",
            json=hub_payload,
            timeout=30
        )

        hub_result = {
            "status": hub_response.status_code,
            "response": hub_response.text
        }

    except Exception as e:
        hub_result = {
            "status": "ERROR",
            "response": str(e)
        }

    return {
        "email": email,
        "group_status": group_result["status"],
        "group_response": group_result["response"],
        "hub_status": hub_result["status"],
        "hub_response": hub_result["response"]
    }


def read_emails(csv_file):
    emails = []

    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)

        for row in reader:
            if row and row[0].strip():
                emails.append(row[0].strip())

    return emails


def main():
    emails = read_emails(INPUT_CSV)

    print(f"Found {len(emails)} email(s)")
    print("Workers: 10")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(add_user, email): email
            for email in emails
        }

        for future in as_completed(futures):
            result = future.result()

            print("-" * 80)
            print("EMAIL:", result["email"])

            print("GROUP API")
            print("STATUS:", result["group_status"])
            print("RESPONSE:", result["group_response"])

            print("HUB API")
            print("STATUS:", result["hub_status"])
            print("RESPONSE:", result["hub_response"])


if __name__ == "__main__":
    main()
