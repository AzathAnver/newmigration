#!/usr/bin/env python3

import os
import sys
import csv
import requests
from dotenv import load_dotenv


# ============================================================
# CONFIG
# ============================================================

INPUT_CSV = r"C:\Users\Azath.A\os\alexa\input.csv"
ENV_PATH = r"C:\Users\Azath.A\os\auth.env"

OUTPUT_FILE_PATH = (
    r"C:\Users\Azath.A\os\alexa\output\user_group_delete_output.txt"
)

TIMEOUT = 30

# ------------------------------------------------------------
# SAFETY SWITCH
#
# True  = show what would be deleted, but DO NOT delete
# False = actually perform DELETE requests
# ------------------------------------------------------------

DRY_RUN = False

USER_URL = (
    "https://media.os.wpp.com/api/az/users/email/{email}"
)

DELETE_URL = (
    "https://media.os.wpp.com/api/az/groups/"
    "{group_uid}/users/{user_id}"
)


# ============================================================
# OUTPUT
# ============================================================

os.makedirs(
    os.path.dirname(OUTPUT_FILE_PATH),
    exist_ok=True
)

output_file = open(
    OUTPUT_FILE_PATH,
    "w",
    encoding="utf-8"
)

_original_print = print


def print(*args, **kwargs):
    """
    Print to console and output file.
    """

    _original_print(*args, **kwargs)

    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")

    output_file.write(
        sep.join(map(str, args)) + end
    )

    output_file.flush()


# ============================================================
# AUTH
# ============================================================

load_dotenv(dotenv_path=ENV_PATH)

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
SESSION_COOKIE = os.getenv("SESSION_COOKIE")

headers = {
    "Accept": "application/json",
    "User-Agent": "python-requests/2.31",
}

if BEARER_TOKEN:
    headers["Authorization"] = (
        f"Bearer {BEARER_TOKEN}"
    )

cookies = {}

if SESSION_COOKIE:
    cookies["session"] = SESSION_COOKIE


# ============================================================
# HELPERS
# ============================================================

def norm(value):
    """
    Normalize strings for comparison.

    Example:

        ' Berlin-Chemie '
        'BERLIN-CHEMIE'

    Both become:

        'berlin-chemie'
    """

    return (value or "").strip().casefold()


# ============================================================
# READ CSV
# ============================================================

def read_input_csv(path):
    """
    Read:

        Company,Email

    Example:

        Berlin-Chemie,irena.matic@wppmedia.com
        Bolt,katarina.batur@wppmedia.com
        Bolton Group,katarina.batur@wppmedia.com

    The same email can occur multiple times.

    The result is grouped by email:

        {
            email: {
                normalized_group_name: original_group_name
            }
        }

    This prevents processing the same email multiple times.
    """

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Input CSV not found: {path}"
        )

    users = {}

    with open(
        path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as f:

        reader = csv.reader(f)

        for line_number, row in enumerate(
            reader,
            start=1
        ):

            if not row:
                continue

            # Ignore completely empty rows
            if not any(
                cell.strip()
                for cell in row
            ):
                continue

            if len(row) < 2:
                print(
                    f"WARNING: Skipping malformed "
                    f"line {line_number}: {row}"
                )
                continue

            company = row[0].strip()
            email = row[1].strip().lower()

            # ------------------------------------------------
            # Optional header detection
            # ------------------------------------------------

            if (
                line_number == 1
                and norm(company) in {
                    "company",
                    "client",
                    "name"
                }
                and norm(email) in {
                    "email",
                    "emailid",
                    "email_id",
                    "email address"
                }
            ):
                print(
                    "CSV header detected and skipped."
                )
                continue

            if not company or not email:
                print(
                    f"WARNING: Empty company/email "
                    f"on line {line_number}. Skipping."
                )
                continue

            company_key = norm(company)

            if email not in users:
                users[email] = {}

            # ------------------------------------------------
            # Deduplicate:
            #
            # Same email + same group only appears once.
            # ------------------------------------------------

            users[email][company_key] = company

    return users


# ============================================================
# GET USER
# ============================================================

def get_user_by_email(email):
    """
    Retrieve user information from OS.
    """

    url = USER_URL.format(
        email=email
    )

    print()
    print("-" * 80)
    print(f"GET USER: {email}")
    print(f"URL: {url}")

    response = requests.get(
        url,
        headers=headers,
        cookies=cookies,
        timeout=TIMEOUT
    )

    print(
        f"HTTP STATUS: {response.status_code}"
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# DELETE GROUP MEMBERSHIP
# ============================================================

def delete_group_membership(
    group_uid,
    user_id
):
    """
    Remove a user from a group.
    """

    url = DELETE_URL.format(
        group_uid=group_uid,
        user_id=user_id
    )

    print(
        f"DELETE URL: {url}"
    )

    if DRY_RUN:
        print(
            "DRY RUN: DELETE NOT EXECUTED"
        )
        return True

    response = requests.delete(
        url,
        headers=headers,
        cookies=cookies,
        timeout=TIMEOUT
    )

    print(
        f"DELETE HTTP STATUS: "
        f"{response.status_code}"
    )

    if response.status_code >= 400:
        print(
            "DELETE RESPONSE:"
        )
        print(
            response.text
        )

    response.raise_for_status()

    return True


# ============================================================
# PROCESS USER
# ============================================================

def process_user(
    email,
    csv_groups
):
    """
    Process one unique email.

    DESIRED ACCESS:

        1. OS Default Users
        2. Groups listed in input.csv for this email

    DELETE:

        Any membership whose JSON 'name' is NOT:

            OS Default Users

        AND NOT one of the CSV groups.

    IMPORTANT:

        account_name is completely ignored.

        Only membership['name'] is considered.
    """

    try:

        user = get_user_by_email(
            email
        )

    except requests.HTTPError as e:

        print(
            f"ERROR: GET failed for "
            f"{email}: {e}"
        )

        return {
            "email": email,
            "status": "GET_FAILED",
            "deleted": 0,
            "kept": 0,
        }

    except Exception as e:

        print(
            f"ERROR: Unexpected GET error "
            f"for {email}: {e}"
        )

        return {
            "email": email,
            "status": "GET_FAILED",
            "deleted": 0,
            "kept": 0,
        }

    # --------------------------------------------------------
    # User ID
    # --------------------------------------------------------

    user_id = user.get("id")

    if not user_id:

        print(
            f"ERROR: No user ID returned "
            f"for {email}"
        )

        return {
            "email": email,
            "status": "NO_USER_ID",
            "deleted": 0,
            "kept": 0,
        }

    # --------------------------------------------------------
    # Group memberships
    # --------------------------------------------------------

    memberships = (
        user.get("group_membership")
        or []
    )

    # --------------------------------------------------------
    # Desired groups
    #
    # ALWAYS keep OS Default Users.
    #
    # Plus all names from CSV for this email.
    # --------------------------------------------------------

    allowed_group_names = {
        "os default users",
        "Owners",
	"Contributors",
	"Viewers",
	"CGOV_Standard",
	"Paws & Tails Demo Users",
	"CEE User Group",
	"Hub Viewers",
	
    }

    allowed_group_names.update(
        csv_groups.keys()
    )

    print()
    print(
        f"USER ID: {user_id}"
    )

    print(
        "ALLOWED GROUP NAMES:"
    )

    for group_name in sorted(
        allowed_group_names
    ):
        print(
            f"  KEEP: {group_name}"
        )

    print()
    print(
        f"TOTAL API MEMBERSHIPS: "
        f"{len(memberships)}"
    )

    # --------------------------------------------------------
    # First determine what should be kept/deleted.
    #
    # We do NOT modify anything while inspecting.
    # --------------------------------------------------------

    groups_to_delete = []
    groups_to_keep = []

    for membership in memberships:

        # ----------------------------------------------------
        # ONLY THIS FIELD IS USED:
        #
        # membership["name"]
        #
        # account_name is intentionally ignored.
        # ----------------------------------------------------

        group_name = (
            membership.get("name")
            or ""
        ).strip()

        group_uid = (
            membership.get("uid")
            or ""
        ).strip()

        normalized_group_name = (
            norm(group_name)
        )

        print()
        print(
            "MEMBERSHIP:"
        )
        print(
            f"  name         : {group_name}"
        )
        print(
            f"  uid          : {group_uid}"
        )
        print(
            f"  account_name : "
            f"{membership.get('account_name', '')}"
        )

        # ----------------------------------------------------
        # KEEP if name is in allowed list.
        # ----------------------------------------------------

        if (
            normalized_group_name
            in allowed_group_names
        ):

            print(
                "  ACTION       : KEEP"
            )

            groups_to_keep.append(
                {
                    "name": group_name,
                    "uid": group_uid,
                }
            )

            continue

        # ----------------------------------------------------
        # Everything else gets deleted.
        # ----------------------------------------------------

        print(
            "  ACTION       : DELETE"
        )

        groups_to_delete.append(
            {
                "name": group_name,
                "uid": group_uid,
            }
        )

    # --------------------------------------------------------
    # Summary before DELETE
    # --------------------------------------------------------

    print()
    print("=" * 80)
    print(
        f"USER: {email}"
    )
    print("=" * 80)

    print()
    print("GROUPS TO KEEP:")

    if groups_to_keep:

        for group in groups_to_keep:

            print(
                f"  KEEP  | "
                f"{group['name']} | "
                f"{group['uid']}"
            )

    else:

        print(
            "  None"
        )

    print()
    print("GROUPS TO DELETE:")

    if groups_to_delete:

        for group in groups_to_delete:

            print(
                f"  DELETE | "
                f"{group['name']} | "
                f"{group['uid']}"
            )

    else:

        print(
            "  None"
        )

    # --------------------------------------------------------
    # Execute deletes
    # --------------------------------------------------------

    deleted_count = 0

    for group in groups_to_delete:

        group_uid = group["uid"]
        group_name = group["name"]

        # ----------------------------------------------------
        # Never attempt DELETE without UID.
        # ----------------------------------------------------

        if not group_uid:

            print()
            print(
                f"SKIP DELETE: "
                f"'{group_name}' has no UID."
            )

            continue

        print()
        print(
            f"PROCESSING DELETE:"
        )
        print(
            f"  User  : {email}"
        )
        print(
            f"  Group : {group_name}"
        )
        print(
            f"  UID   : {group_uid}"
        )

        try:

            delete_group_membership(
                group_uid=group_uid,
                user_id=user_id
            )

            deleted_count += 1

            if DRY_RUN:

                print(
                    "RESULT: WOULD DELETE"
                )

            else:

                print(
                    "RESULT: DELETE SUCCESSFUL"
                )

        except requests.HTTPError as e:

            print(
                f"RESULT: DELETE FAILED: {e}"
            )

        except Exception as e:

            print(
                f"RESULT: DELETE FAILED: {e}"
            )

    return {
        "email": email,
        "status": "PROCESSED",
        "deleted": deleted_count,
        "kept": len(groups_to_keep),
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 80)
    print(
        "WPP OS USER GROUP ACCESS CLEANUP"
    )
    print("=" * 80)

    print()

    if DRY_RUN:

        print(
            "MODE: DRY RUN"
        )
        print(
            "NO DELETE REQUESTS WILL BE SENT."
        )

    else:

        print(
            "MODE: LIVE DELETE"
        )
        print(
            "DELETE REQUESTS WILL BE SENT."
        )

    # --------------------------------------------------------
    # Read CSV
    # --------------------------------------------------------

    try:

        users = read_input_csv(
            INPUT_CSV
        )

    except Exception as e:

        print(
            f"INPUT ERROR: {e}",
            file=sys.stderr
        )

        sys.exit(1)

    # --------------------------------------------------------
    # CSV statistics
    # --------------------------------------------------------

    total_unique_emails = len(
        users
    )

    total_unique_email_groups = sum(
        len(groups)
        for groups in users.values()
    )

    print()
    print(
        f"Unique emails: "
        f"{total_unique_emails}"
    )

    print(
        f"Unique email/group combinations: "
        f"{total_unique_email_groups}"
    )

    # --------------------------------------------------------
    # Display deduplicated input
    # --------------------------------------------------------

    print()
    print("=" * 80)
    print(
        "DEDUPLICATED INPUT"
    )
    print("=" * 80)

    for email in sorted(users):

        print()
        print(
            f"{email}"
        )

        for group_name in sorted(
            users[email].values()
        ):

            print(
                f"  - {group_name}"
            )

    # --------------------------------------------------------
    # Process every UNIQUE email
    # --------------------------------------------------------

    results = []

    for email in sorted(users):

        result = process_user(
            email=email,
            csv_groups=users[email]
        )

        results.append(
            result
        )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print()
    print("=" * 80)
    print(
        "FINAL SUMMARY"
    )
    print("=" * 80)

    total_deleted = sum(
        result["deleted"]
        for result in results
    )

    total_kept = sum(
        result["kept"]
        for result in results
    )

    get_failures = sum(
        1
        for result in results
        if result["status"] == "GET_FAILED"
    )

    print(
        f"Unique emails processed : "
        f"{len(results)}"
    )

    print(
        f"GET failures            : "
        f"{get_failures}"
    )

    print(
        f"Groups kept              : "
        f"{total_kept}"
    )

    if DRY_RUN:

        print(
            f"Groups that WOULD DELETE: "
            f"{total_deleted}"
        )

        print()
        print(
            "DRY RUN COMPLETE."
        )

        print(
            "Review the output file."
        )

        print(
            "If everything is correct, "
            "set DRY_RUN = False and run again."
        )

    else:

        print(
            f"Groups actually deleted: "
            f"{total_deleted}"
        )

    print()
    print("=" * 80)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        main()

    finally:

        output_file.close()
