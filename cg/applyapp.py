import requests
import csv

# File paths
env_path = r"C:\Users\Azath.A\os\auth.env"
csv_path = r"C:\Users\Azath.A\os\test\test.csv"

# New API URL
url = "https://thebootsgroup.os.wpp.com/api/app-instances/bulk"


# Read token + session cookie
def get_env_values(file_path):
    token = None
    session_cookie = None

    with open(file_path, "r") as file:
        for line in file:
            if "BEARER_TOKEN" in line:
                token = line.strip().split("=", 1)[1]
            elif "SESSION_COOKIE" in line:
                session_cookie = line.strip().split("=", 1)[1]

    return token, session_cookie


token, session_cookie = get_env_values(env_path)

if not token:
    print("❌ Bearer token not found!")
    exit()


# Create session
session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://thebootsgroup.os.wpp.com",
    "Referer": "https://thebootsgroup.os.wpp.com/",
    "User-Agent": "Mozilla/5.0"
})

# Add session cookie if available
if session_cookie:
    session.cookies.set("session", session_cookie)


# Read CSV and call API
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        assignment_id = row["assignmentId"].strip()

        # Payload must be inside []
        payload = [
            {
                "name": None,
                "devhubAppId": "0a1c073c-9629-1222-8196-3392e2340002",
                "devhubAppVersionId": "f39411d8-0f5b-4dfa-bd94-e8d824b5410a",
                "assignmentId": assignment_id,
                "flags": {
                    "visible": True,
                    "accessRequestable": True
                },
                "assignmentType": "WORKSPACE",
                "description": None,
                "logoThumbnail": None,
                "logoOriginal": None
            }
        ]

        print("\n===================================")
        print(f"🚀 Assignment ID: {assignment_id}")

        try:
            response = session.post(url, json=payload)

            print(f"📡 Status Code: {response.status_code}")
            print(f"📩 Response: {response.text}")

        except Exception as e:
            print(f"❌ Error: {e}")