from playwright.sync_api import sync_playwright
import win32com.client
import time
import json
import os
import re
from datetime import datetime


# ============================================================
# CONFIG
# ============================================================

ZENDESK_URL = "https://choreographsupport.zendesk.com"

FILTER_URL = (
    "https://choreographsupport.zendesk.com/"
    "agent/filters/30062174420380"
)

VIEW_ID = "30062174420380"

SESSION_FILE = "zendesk_session.json"
CACHE_FILE = "zendesk_processed_tickets.json"


# ============================================================
# EMAIL
# ============================================================

MAIL_TO = "azath.a@choreograph.com"
MAIL_FROM = "azath.a@wppmedia.com"


# ============================================================
# YOUR ZENDESK ACCOUNT
# ============================================================

MY_NAME = "Azath"

MY_USER_ID = 21630914775964
MY_GROUP_ID = 4620379511964


# ============================================================
# MONITOR INTERVAL
# ============================================================

CHECK_EVERY = 10


# ============================================================
# API RATE LIMIT
# ============================================================

BACKOFF_BASE = 5
BACKOFF_MAX = 300

_consecutive_429 = 0
_next_allowed_at = 0.0


# ============================================================
# KEYWORDS
#
# DO NOT CHANGE THIS LOGIC
# ============================================================

KEYWORDS = [
    "placement",
    "placements",
    "mrf id",
    "mrfid",
    "mrfids",
    "mrf ids",
    "currency",
    "vendor",
    "vendors",
    "supplier",
    "suppliers",
    "geo-target"
]


# ============================================================
# CACHE
# ============================================================

def load_cache():
    """
    Cache format:

    {
        "last_updated": "...",
        "notified": ["123", "456"],
        "assigned": ["123"]
    }

    notified:
        Ticket notification email has been sent.

    assigned:
        IMPORTANT:
        Ticket was successfully assigned by automation.

        Once a ticket ID is in `assigned`, the script will
        NEVER automatically assign that ticket again.

        Even if you manually unassign the ticket later,
        it will remain protected.
    """

    if not os.path.exists(CACHE_FILE):

        print(
            "ℹ No cache file found. "
            "Starting with empty cache."
        )

        return set(), set()

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        notified = set(
            str(x)
            for x in data.get(
                "notified",
                []
            )
        )

        assigned = set(
            str(x)
            for x in data.get(
                "assigned",
                []
            )
        )

        print(
            f"✓ Cache loaded: "
            f"{len(notified)} notified, "
            f"{len(assigned)} permanently protected"
        )

        return notified, assigned

    except Exception as e:

        print(
            f"⚠ Cache could not be read: {e}"
        )

        print(
            "ℹ Starting with empty cache."
        )

        return set(), set()


def save_cache(
    notified,
    assigned
):

    try:

        data = {
            "last_updated":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "notified":
                sorted(notified),

            "assigned":
                sorted(assigned)
        }

        temp_file = CACHE_FILE + ".tmp"

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )

        os.replace(
            temp_file,
            CACHE_FILE
        )

        print(
            f"     💾 Cache saved "
            f"(notified={len(notified)}, "
            f"protected={len(assigned)})"
        )

    except Exception as e:

        print(
            f"     ✗ Cache save failed: {e}"
        )


# ============================================================
# OUTLOOK
# ============================================================

def send_outlook_email(
    subject,
    body
):

    try:

        outlook = win32com.client.Dispatch(
            "outlook.application"
        )

        mail = outlook.CreateItem(0)

        mail.To = MAIL_TO
        mail.Subject = subject
        mail.Body = body

        # ----------------------------------------------------
        # Select MAIL_FROM account
        # ----------------------------------------------------

        try:

            found_account = False

            for account in outlook.Session.Accounts:

                smtp_address = str(
                    account.SmtpAddress
                )

                if (
                    MAIL_FROM.lower()
                    in smtp_address.lower()
                ):

                    mail._oleobj_.Invoke(
                        *(64209, 0, 8, 0, account)
                    )

                    found_account = True
                    break

            if not found_account:

                print(
                    f"     ⚠ Outlook account "
                    f"{MAIL_FROM} not found."
                )

                print(
                    "     ℹ Using default account."
                )

        except Exception as account_error:

            print(
                f"     ⚠ Could not select "
                f"sending account: "
                f"{account_error}"
            )

        mail.Send()

        print(
            f"     ✓ Email sent: {subject}"
        )

        return True

    except Exception as e:

        print(
            f"     ✗ Outlook email error: {e}"
        )

        return False


# ============================================================
# NEW TICKET EMAIL
# ============================================================

def send_new_ticket_email(
    tid,
    subject
):

    email_subject = (
        f"New Zendesk Ticket #{tid}"
    )

    email_body = (
        "New ticket in your Zendesk view.\n\n"

        f"Ticket ID : {tid}\n"
        f"Subject   : {subject}\n"
        f"Time      : "
        f"{datetime.now():%Y-%m-%d %H:%M:%S}\n\n"

        f"Link: "
        f"{ZENDESK_URL}/agent/tickets/{tid}\n"
    )

    return send_outlook_email(
        email_subject,
        email_body
    )


# ============================================================
# ASSIGNMENT EMAIL
# ============================================================

def send_assignment_email(
    tid,
    subject,
    keyword
):

    email_subject = (
        f"Auto-assigned Zendesk Ticket #{tid}"
    )

    email_body = (
        "A Zendesk ticket has been "
        "automatically assigned to you.\n\n"

        f"Ticket ID : {tid}\n"
        f"Subject   : {subject}\n"
        f"Keyword   : {keyword}\n"
        f"Assigned  : {MY_NAME}\n"
        f"User ID   : {MY_USER_ID}\n"
        f"Group ID  : {MY_GROUP_ID}\n"
        f"Time      : "
        f"{datetime.now():%Y-%m-%d %H:%M:%S}\n\n"

        f"Link: "
        f"{ZENDESK_URL}/agent/tickets/{tid}\n"
    )

    return send_outlook_email(
        email_subject,
        email_body
    )


# ============================================================
# AUTHENTICATION ERROR EMAIL
# ============================================================

def send_authentication_error_email(
    status_code
):

    email_subject = (
        "⚠ Zendesk Authentication Needs Updating"
    )

    email_body = (
        "Zendesk API authentication has failed.\n\n"

        f"HTTP Status : {status_code}\n\n"

        "Possible cause:\n"
        "- Zendesk session expired\n"
        "- CSRF token expired\n"
        "- Zendesk authentication changed\n\n"

        "Please open Zendesk in the browser and "
        "log in again if required.\n\n"

        f"Session file: {SESSION_FILE}\n\n"

        f"Time: "
        f"{datetime.now():%Y-%m-%d %H:%M:%S}\n"
    )

    return send_outlook_email(
        email_subject,
        email_body
    )


# ============================================================
# CSRF TOKEN
# ============================================================

def get_csrf_token(page):

    try:

        token = page.locator(
            'meta[name="csrf-token"]'
        ).get_attribute(
            "content"
        )

        if token:
            return token

    except Exception as e:

        print(
            f"     ⚠ CSRF token error: {e}"
        )

    return None


# ============================================================
# CURRENT USER
# ============================================================

def get_current_user(page):

    try:

        response = page.request.get(
            f"{ZENDESK_URL}/api/v2/users/me.json",
            timeout=30000
        )

        if response.status in (
            401,
            403
        ):

            print(
                f"✗ Authentication failed: "
                f"HTTP {response.status}"
            )

            return None, response.status

        if not response.ok:

            print(
                f"✗ /users/me failed: "
                f"HTTP {response.status}"
            )

            return None, response.status

        data = response.json()

        return (
            data.get("user"),
            None
        )

    except Exception as e:

        print(
            f"✗ Could not get current user: {e}"
        )

        return None, None


# ============================================================
# ASSIGN TICKET VIA ZENDESK API
# ============================================================

def assign_ticket(
    page,
    csrf_token,
    ticket_id
):

    global _consecutive_429
    global _next_allowed_at

    url = (
        f"{ZENDESK_URL}"
        f"/api/v2/tickets/{ticket_id}.json"
    )

    payload = {
        "ticket": {
            "assignee_id": MY_USER_ID,
            "group_id": MY_GROUP_ID
        }
    }

    headers = {
        "X-CSRF-Token": csrf_token,
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json"
    }

    try:

        response = page.request.put(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=30000
        )

        # ----------------------------------------------------
        # RATE LIMIT
        # ----------------------------------------------------

        if response.status == 429:

            _consecutive_429 += 1

            wait_secs = min(
                BACKOFF_BASE * (
                    2 ** (
                        _consecutive_429 - 1
                    )
                ),
                BACKOFF_MAX
            )

            retry_after_hdr = (
                response.headers.get(
                    "retry-after",
                    ""
                )
            )

            if retry_after_hdr.isdigit():

                wait_secs = max(
                    wait_secs,
                    int(retry_after_hdr)
                )

            _next_allowed_at = (
                time.time() + wait_secs
            )

            print(
                f"     ⚠ Assignment API "
                f"rate limited: HTTP 429. "
                f"Back-off {wait_secs}s."
            )

            return False, 429

        # ----------------------------------------------------
        # AUTHENTICATION ERROR
        # ----------------------------------------------------

        if response.status in (
            401,
            403
        ):

            print(
                f"     ❌ Assignment authentication "
                f"failure: HTTP {response.status}"
            )

            return False, response.status

        # ----------------------------------------------------
        # OTHER API ERROR
        # ----------------------------------------------------

        if not response.ok:

            print(
                f"     ✗ Assignment failed "
                f"for #{ticket_id}"
            )

            print(
                f"       HTTP: {response.status}"
            )

            try:

                print(
                    f"       {response.text()[:1000]}"
                )

            except Exception:
                pass

            return False, response.status

        # ----------------------------------------------------
        # Successful API request
        # ----------------------------------------------------

        _consecutive_429 = 0

        data = response.json()

        ticket = data.get(
            "ticket",
            {}
        )

        returned_assignee = ticket.get(
            "assignee_id"
        )

        returned_group = ticket.get(
            "group_id"
        )

        # ----------------------------------------------------
        # VERIFY ASSIGNMENT
        # ----------------------------------------------------

        if (
            str(returned_assignee)
            == str(MY_USER_ID)
            and
            str(returned_group)
            == str(MY_GROUP_ID)
        ):

            print(
                f"     ✅ Ticket #{ticket_id} "
                f"assigned successfully."
            )

            return True, None

        # ----------------------------------------------------
        # Verification failed
        # ----------------------------------------------------

        print(
            "     ⚠ PUT succeeded but "
            "assignment verification failed."
        )

        print(
            f"       Expected assignee: "
            f"{MY_USER_ID}"
        )

        print(
            f"       Returned assignee: "
            f"{returned_assignee}"
        )

        print(
            f"       Expected group: "
            f"{MY_GROUP_ID}"
        )

        print(
            f"       Returned group: "
            f"{returned_group}"
        )

        return False, None

    except Exception as e:

        print(
            f"     ✗ Assignment exception: {e}"
        )

        return False, None


# ============================================================
# TICKET ID
# ============================================================

def get_ticket_id(ticket):

    tid = (
        ticket.get_attribute(
            "data-ticket-id"
        )
        or ticket.get_attribute(
            "data-id"
        )
        or ticket.get_attribute(
            "id"
        )
    )

    if tid:

        cleaned = re.sub(
            r"\D",
            "",
            str(tid)
        )

        if cleaned:
            return cleaned

        return str(tid)

    # --------------------------------------------------------
    # Fallback: inspect HTML
    # --------------------------------------------------------

    try:

        html = ticket.inner_html()

        patterns = [
            r"ticket[s]?[-/](\d+)",
            r"/tickets/(\d+)",
            r"ticket[_-]?id[\"'=:\s]+(\d+)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                html,
                re.IGNORECASE
            )

            if match:

                return match.group(1)

    except Exception:
        pass

    return None


# ============================================================
# SUBJECT
# ============================================================

def get_subject(ticket):

    selectors = [
        ".subject",
        '[data-test-id="subject"]',
        ".ticket-subject",
        ".event-title",
        '[data-test-id="ticket-subject"]'
    ]

    for selector in selectors:

        try:

            element = ticket.query_selector(
                selector
            )

            if element:

                text = (
                    element.inner_text()
                    .strip()
                )

                if text:

                    return text

        except Exception:
            pass

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    try:

        text = (
            ticket.inner_text()
            .strip()
        )

        if text:

            text = re.sub(
                r"\s+",
                " ",
                text
            )

            return text[:150]

    except Exception:
        pass

    return None


# ============================================================
# FIND TICKET ROWS
# ============================================================

def find_ticket_rows(page):

    selectors = [
        '[data-test-id="ticket-row"]',
        ".event-row",
        ".ticket-row",
        '[role="row"]'
    ]

    for selector in selectors:

        try:

            rows = page.query_selector_all(
                selector
            )

            if rows:

                return rows

        except Exception:
            pass

    return []


# ============================================================
# PROCESS TICKETS
# ============================================================

def process_tickets(
    page,
    csrf_token,
    notified,
    assigned
):

    # --------------------------------------------------------
    # Load Zendesk filter
    # --------------------------------------------------------

    try:

        page.goto(
            FILTER_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        time.sleep(3)

    except Exception as e:

        print(
            f"     ✗ Could not load filter: {e}"
        )

        return (
            notified,
            assigned
        )

    # --------------------------------------------------------
    # Find ticket rows
    # --------------------------------------------------------

    rows = find_ticket_rows(page)

    print(
        f"[{datetime.now():%Y-%m-%d %H:%M:%S}] "
        f"Rows found: {len(rows)} | "
        f"Notified: {len(notified)} | "
        f"Permanently protected: {len(assigned)}"
    )

    # --------------------------------------------------------
    # Snapshot rows
    # --------------------------------------------------------

    snapshot = []

    for row in rows:

        try:

            tid = get_ticket_id(row)
            subject = get_subject(row)

            if tid and subject:

                snapshot.append(
                    (
                        str(tid),
                        subject
                    )
                )

        except Exception as e:

            print(
                f"     ⚠ Could not read row: {e}"
            )

    # ========================================================
    # PROCESS EACH TICKET
    # ========================================================

    for tid, subject in snapshot:

        try:

            # ------------------------------------------------
            # KEYWORD MATCHING
            # ------------------------------------------------

            subject_lower = subject.lower()

            matched_keyword = next(
                (
                    keyword
                    for keyword in KEYWORDS
                    if keyword.lower()
                    in subject_lower
                ),
                None
            )

            # ------------------------------------------------
            # CACHE STATE
            # ------------------------------------------------

            already_notified = (
                tid in notified
            )

            already_assigned = (
                tid in assigned
            )

            # =================================================
            # PERMANENT PROTECTION
            #
            # THIS IS THE IMPORTANT PART.
            #
            # If automation previously assigned this ticket,
            # it is permanently protected.
            #
            # Even if you manually unassign it later,
            # this remains True.
            # =================================================

            if already_assigned:

                print()
                print("-" * 60)

                print(
                    f"🚫 Ticket #{tid} "
                    f"PERMANENTLY PROTECTED"
                )

                print(
                    f"   Subject : {subject}"
                )

                print(
                    "   Reason  : Previously assigned "
                    "by automation."
                )

                print(
                    "   Action  : NO reassignment."
                )

                # ------------------------------------------------
                # We still do NOT send another new-ticket email.
                # ------------------------------------------------

                continue

            # =================================================
            # NEW TICKET EMAIL
            # =================================================

            if not already_notified:

                print()
                print("-" * 60)

                print(
                    f"📩 NEW TICKET #{tid}"
                )

                print(
                    f"   Subject : {subject}"
                )

                print(
                    "   📧 Sending new ticket email..."
                )

                email_ok = (
                    send_new_ticket_email(
                        tid,
                        subject
                    )
                )

                if email_ok:

                    notified.add(tid)

                    save_cache(
                        notified,
                        assigned
                    )

                    print(
                        "   ✅ New ticket "
                        "notification saved."
                    )

                else:

                    print(
                        "   ⚠ New ticket email failed."
                    )

            # =================================================
            # NO KEYWORD
            # =================================================

            if not matched_keyword:

                print(
                    f"     ℹ Ticket #{tid}: "
                    f"no assignment keyword found."
                )

                continue

            # =================================================
            # KEYWORD MATCH
            #
            # Since we already checked `already_assigned`
            # above, reaching here means this ticket has
            # NEVER been successfully assigned by automation.
            # =================================================

            print()
            print("-" * 60)

            print(
                f"🎯 KEYWORD MATCH — Ticket #{tid}"
            )

            print(
                f"   Subject : {subject}"
            )

            print(
                f"   Keyword : {matched_keyword}"
            )

            print(
                f"   Action  : Assigning to {MY_NAME}"
            )

            # ------------------------------------------------
            # API ASSIGNMENT
            # ------------------------------------------------

            (
                assign_ok,
                error_status
            ) = assign_ticket(
                page,
                csrf_token,
                tid
            )

            # =================================================
            # AUTHENTICATION ERROR
            # =================================================

            if error_status in (
                401,
                403
            ):

                print(
                    "     ❌ Zendesk authentication "
                    "failed."
                )

                print(
                    "     ℹ Ticket was NOT added "
                    "to permanent cache."
                )

                continue

            # =================================================
            # RATE LIMIT
            # =================================================

            if error_status == 429:

                print(
                    "     ⚠ Assignment API "
                    "rate limited."
                )

                print(
                    "     ℹ Ticket was NOT added "
                    "to permanent cache."
                )

                print(
                    "     ℹ It will retry after "
                    "back-off."
                )

                continue

            # =================================================
            # SUCCESSFUL ASSIGNMENT
            # =================================================

            if assign_ok:

                # ------------------------------------------------
                # IMPORTANT:
                #
                # This is what makes the protection permanent.
                #
                # Once added, the ticket will NEVER be
                # automatically assigned again.
                # ------------------------------------------------

                assigned.add(tid)

                save_cache(
                    notified,
                    assigned
                )

                print()
                print(
                    f"     🔒 Ticket #{tid} is now "
                    f"PERMANENTLY PROTECTED."
                )

                print(
                    f"     ✓ Assigned to {MY_NAME}."
                )

                print(
                    "     ✓ If you manually unassign "
                    "it later, the script will NOT "
                    "reassign it."
                )

                # ------------------------------------------------
                # Assignment email
                # ------------------------------------------------

                print(
                    "     📧 Sending assignment email..."
                )

                assignment_email_ok = (
                    send_assignment_email(
                        tid,
                        subject,
                        matched_keyword
                    )
                )

                if assignment_email_ok:

                    print(
                        "     ✅ Assignment email sent."
                    )

                else:

                    print(
                        "     ⚠ Assignment email failed."
                    )

                    print(
                        "     ℹ Ticket remains permanently "
                        "protected."
                    )

            # =================================================
            # ASSIGNMENT FAILED
            # =================================================

            else:

                print(
                    f"     ✗ Could not assign "
                    f"ticket #{tid}."
                )

                print(
                    "     ℹ Ticket was NOT added "
                    "to permanent cache."
                )

                print(
                    "     ℹ It can retry on "
                    "the next cycle."
                )

        except Exception as e:

            print(
                f"     ✗ Error processing "
                f"ticket #{tid}: {e}"
            )

    return (
        notified,
        assigned
    )


# ============================================================
# MONITOR
# ============================================================

def monitor_zendesk_tickets():

    # --------------------------------------------------------
    # INITIAL CACHE
    # --------------------------------------------------------

    notified, assigned = load_cache()

    print()
    print("=" * 60)
    print("   ZENDESK TICKET MONITOR")
    print("=" * 60)

    print(
        f"Zendesk URL : {ZENDESK_URL}"
    )

    print(
        f"Filter URL  : {FILTER_URL}"
    )

    print(
        f"View ID     : {VIEW_ID}"
    )

    print(
        f"From        : {MAIL_FROM}"
    )

    print(
        f"To          : {MAIL_TO}"
    )

    print(
        f"User        : {MY_NAME}"
    )

    print(
        f"User ID     : {MY_USER_ID}"
    )

    print(
        f"Group ID    : {MY_GROUP_ID}"
    )

    print(
        f"Cache file  : {CACHE_FILE}"
    )

    print(
        f"Check every : {CHECK_EVERY} seconds"
    )

    print()
    print("Assignment rules:")
    print(
        "  • Keyword match → assign to Azath"
    )
    print(
        "  • Successful assignment → permanent protection"
    )
    print(
        "  • Manually unassigned later → NEVER reassign"
    )
    print(
        "  • Assigned to another agent → no automatic reassignment"
    )
    print(
        "  • Previously automated ticket → NEVER touch again"
    )
    print(
        "  • Failed assignment → retry"
    )
    print(
        "  • No keyword → no assignment"
    )
    print("=" * 60)
    print()

    # ========================================================
    # PLAYWRIGHT
    # ========================================================

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        # ----------------------------------------------------
        # Load session
        # ----------------------------------------------------

        if os.path.exists(
            SESSION_FILE
        ):

            print(
                "✓ Existing Zendesk session found."
            )

            context = browser.new_context(
                storage_state=SESSION_FILE
            )

        else:

            print(
                "ℹ No Zendesk session file found."
            )

            context = browser.new_context()

        page = context.new_page()

        # ====================================================
        # INITIAL ZENDESK ACCESS
        # ====================================================

        print(
            "Accessing Zendesk..."
        )

        try:

            page.goto(
                FILTER_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            time.sleep(5)

        except Exception as e:

            print(
                f"❌ Could not access Zendesk: {e}"
            )

            browser.close()

            return

        # ====================================================
        # LOGIN CHECK
        # ====================================================

        if any(
            x in page.url.lower()
            for x in (
                "login",
                "saml",
                "sso",
                "auth"
            )
        ):

            print()
            print(
                "⚠ MANUAL LOGIN REQUIRED"
            )

            print(
                "Please log in to Zendesk "
                "in the browser."
            )

            print()

            input(
                "Press ENTER after the "
                "ticket list is visible..."
            )

            # ------------------------------------------------
            # Save authenticated session
            # ------------------------------------------------

            try:

                context.storage_state(
                    path=SESSION_FILE
                )

                print(
                    "✓ Zendesk session saved."
                )

            except Exception as e:

                print(
                    f"⚠ Could not save session: {e}"
                )

        # ====================================================
        # RETURN TO FILTER
        # ====================================================

        try:

            page.goto(
                FILTER_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            time.sleep(5)

        except Exception as e:

            print(
                f"❌ Could not open filter: {e}"
            )

            browser.close()

            return

        # ====================================================
        # VERIFY AUTHENTICATION
        # ====================================================

        print()
        print(
            "Checking Zendesk authentication..."
        )

        current_user, user_error = (
            get_current_user(page)
        )

        if not current_user:

            print()
            print(
                "❌ Could not verify Zendesk "
                "authentication."
            )

            if user_error:

                print(
                    f"HTTP Status: {user_error}"
                )

            browser.close()

            return

        print(
            f"✓ Logged in as: "
            f"{current_user.get('name')}"
        )

        print(
            f"✓ User ID: "
            f"{current_user.get('id')}"
        )

        print(
            f"✓ Email: "
            f"{current_user.get('email')}"
        )

        # ====================================================
        # VERIFY USER ID
        # ====================================================

        if (
            str(current_user.get("id"))
            != str(MY_USER_ID)
        ):

            print()
            print(
                "❌ Logged-in user does not "
                "match MY_USER_ID."
            )

            print(
                f"Expected: {MY_USER_ID}"
            )

            print(
                f"Actual: "
                f"{current_user.get('id')}"
            )

            print(
                "The monitor will not continue."
            )

            browser.close()

            return

        print()
        print(
            f"✓ Logged-in user verified "
            f"as {MY_NAME}."
        )

        # ====================================================
        # CSRF TOKEN
        # ====================================================

        print()
        print(
            "Reading Zendesk CSRF token..."
        )

        csrf_token = get_csrf_token(
            page
        )

        if not csrf_token:

            print(
                "❌ CSRF token not found."
            )

            print(
                "The API assignment cannot "
                "continue safely."
            )

            browser.close()

            return

        print(
            "✓ CSRF token found."
        )

        # ====================================================
        # START MONITORING
        # ====================================================

        print()
        print("=" * 60)
        print("🚀 MONITORING STARTED")
        print("=" * 60)
        print()

        while True:

            try:

                # ------------------------------------------------
                # Reload cache every cycle.
                #
                # This means manual edits to the JSON file
                # are picked up while the monitor is running.
                # ------------------------------------------------

                notified, assigned = load_cache()

                # ------------------------------------------------
                # Process tickets
                # ------------------------------------------------

                (
                    notified,
                    assigned
                ) = process_tickets(
                    page,
                    csrf_token,
                    notified,
                    assigned
                )

                # ------------------------------------------------
                # Save cache
                # ------------------------------------------------

                save_cache(
                    notified,
                    assigned
                )

                # ------------------------------------------------
                # Sleep / rate limit
                # ------------------------------------------------

                now = time.time()

                if now < _next_allowed_at:

                    remaining = int(
                        _next_allowed_at - now
                    ) + 1

                    print()
                    print(
                        f"💤 Rate-limited. "
                        f"Next check in ~"
                        f"{remaining}s..."
                    )
                    print()

                    time.sleep(
                        remaining
                    )

                else:

                    print()
                    print(
                        f"💤 Sleeping "
                        f"{CHECK_EVERY} seconds..."
                    )
                    print()

                    time.sleep(
                        CHECK_EVERY
                    )

            # ----------------------------------------------------
            # Keyboard interrupt
            # ----------------------------------------------------

            except KeyboardInterrupt:

                print()
                print(
                    "🛑 Monitor stopped by user."
                )

                save_cache(
                    notified,
                    assigned
                )

                break

            # ----------------------------------------------------
            # Unexpected error
            # ----------------------------------------------------

            except Exception as e:

                print()
                print(
                    f"✗ Monitor loop error: {e}"
                )

                save_cache(
                    notified,
                    assigned
                )

                print(
                    "ℹ Retrying in 60 seconds..."
                )

                time.sleep(60)

        # ====================================================
        # CLOSE
        # ====================================================

        try:

            context.close()

        except Exception:
            pass

        try:

            browser.close()

        except Exception:
            pass


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("   ZENDESK TICKET MONITOR")
    print("=" * 60)
    print()

    monitor_zendesk_tickets()
