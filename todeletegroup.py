import requests
import sys
import getpass


def delete_group(token: str):
    url = "https://media.os.wpp.com/api/az/groups/86514201-4dd8-4f39-9b96-7c780a2a0665"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    try:
        response = requests.delete(url, headers=headers, timeout=30)

        print(f"\nStatus Code: {response.status_code}")

        if response.status_code in [200, 202, 204]:
            print("✅ Delete successful")
        else:
            print("❌ Delete failed")
            print("Response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print("Error occurred:", str(e))

if __name__ == "__main__":
    bearer_token = getpass.getpass("Enter Bearer Token: ")
    delete_group(bearer_token)

    bearer_token = sys.argv[1]
    delete_group(bearer_token)