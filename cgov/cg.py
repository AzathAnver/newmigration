import requests

# ==========================================
# CONFIG
# ==========================================

env_path = r"C:\Users\Azath.A\os\auth.env"

# ==========================================
# READ BEARER TOKEN
# ==========================================

token = None

with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if line.startswith("BEARER_TOKEN="):
            token = line.split("=", 1)[1].strip()
            break

if not token:
    raise Exception("BEARER_TOKEN not found in auth.env")

endpoint = input(
    "Endpoint (e.g. https://lvmh-apac.os.wpp.com): "
).strip().rstrip("/")

tenant_id = input("Tenant ID: ").strip()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# ==========================================
# GET ROOT ACCOUNT
# ==========================================

print("\nGetting hierarchy information...")

url = f"{endpoint}/api/v2/tenants/{tenant_id}/hierarchy-tree"

resp = requests.get(url, headers=headers)
resp.raise_for_status()

hierarchy = resp.json()
root_account_id = hierarchy["rootId"]

print(f"Root Account ID: {root_account_id}")

# ==========================================
# GET CGOV ROLES
# ==========================================

print("\nFetching CGOV roles...")

url = (
    f"{endpoint}/api/tenants/{tenant_id}/roles"
    "?page=1&itemsPerPage=50&sort=name&filter%5Bsearch%5D=CGOV"
)

resp = requests.get(url, headers=headers)
resp.raise_for_status()

roles = resp.json()["data"]

role_map = {}

for role in roles:
    role_map[role["name"]] = role["id"]

required_roles = {
    "CGOV_Standard": role_map.get("CGOV_Standard"),
    "CGOV_Manager": role_map.get("CGOV_Manager")
}

for role_name, role_id in required_roles.items():
    if not role_id:
        raise Exception(f"Could not find role {role_name}")

print("Roles discovered successfully.")

# ==========================================
# GET EXISTING GROUPS
# ==========================================

print("\nFetching existing groups...")

url = (
    f"{endpoint}/api/tenants/{tenant_id}/groups"
    "?page=1&itemsPerPage=50&sort=name"
)

resp = requests.get(url, headers=headers)
resp.raise_for_status()

groups_data = resp.json()["data"]

existing_groups = {}

for group in groups_data:
    existing_groups[group["name"]] = group["id"]

# ==========================================
# CREATE GROUP IF MISSING
# ==========================================

group_ids = {}

descriptions = {
    "CGOV_Standard": (
        "Users who can access Campaign Governance on the workspace."
    ),
    "CGOV_Manager": (
        "Users who can manage Campaign Governance on the workspace."
    )
}

for group_name in ["CGOV_Standard", "CGOV_Manager"]:

    if group_name in existing_groups:

        group_id = existing_groups[group_name]

        print(f"\n{group_name} already exists.")
        print(f"Group ID: {group_id}")

    else:

        print(f"\nCreating {group_name}...")

        payload = {
            "account_uid": root_account_id,
            "name": group_name,
            "description": descriptions[group_name],
            "custom_data": {}
        }

        url = f"{endpoint}/api/az/groups"

        resp = requests.post(
            url,
            headers=headers,
            json=payload
        )

        resp.raise_for_status()

        group_id = resp.json()["uid"]

        print(f"Created {group_name}")
        print(f"Group ID: {group_id}")

    group_ids[group_name] = group_id

# ==========================================
# ASSIGN ROLES
# ==========================================

print("\nAssigning roles...")

for group_name, group_id in group_ids.items():

    role_id = required_roles[group_name]

    payload = {
        "create": [
            {
                "group_id": group_id,
                "role_id": role_id,
                "account_id": root_account_id
            }
        ],
        "delete": []
    }

    url = f"{endpoint}/api/az/groups/roles"

    try:

        resp = requests.patch(
            url,
            headers=headers,
            json=payload
        )

        if resp.status_code in (200, 201):
            print(f"Role assigned to {group_name}")
        else:
            print(
                f"Role assignment response for "
                f"{group_name}: {resp.status_code}"
            )

    except Exception as e:
        print(f"Role assignment failed for {group_name}: {e}")

print("\nCompleted successfully.")