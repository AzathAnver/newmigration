import requests
import os
from dotenv import load_dotenv

GROUP_ID = "a681fdb4-4a2b-4fd4-a10b-360eea959420"
EMAIL = "azath.anver@wppmedia.com"

BASE_URL = "https://media.os.wpp.com"

env_path = r"C:\Users\Azath.A\os\auth.env"

load_dotenv(dotenv_path=env_path, override=True)

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

payload = {
    "create": [
        {
            "groupId": GROUP_ID,
            "userId": EMAIL
        }
    ],
    "delete": []
}

r = s.patch(
    f"{BASE_URL}/api/az/groups/users",
    json=payload,
    timeout=30
)

print("STATUS:", r.status_code)
print("RESPONSE:")
print(r.text)