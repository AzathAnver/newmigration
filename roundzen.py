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

# YOUR NEW VIEW URL
FILTER_URL = (
    "https://choreographsupport.zendesk.com/"
    "agent/filters/30585319540380"
)


# ============================================================
# CACHE FILE
#
# This is a NEW cache file specifically for this monitor.
# ============================================================

CACHE_FILE = "zendesk_hold_monitor_cache.json"


# ============================================================
# EMAIL
# ============================================================

MAIL_TO = "azath.a@choreograph.com"
MAIL_FROM = "azath.a@wppmedia.com"


# ============================================================
# MONITOR TIMING
# ============================================================

# Refresh the Zendesk view every 1 minute
CHECK_EVERY = 60

# Put ticket On-hold after 5 minutes
HOLD_AFTER_SECONDS = 5 * 60


# ============================================================
# ZENDESK SESSION
# ============================================================

SESSION_FILE = "zendesk_session.json"


# ============================================================
# API RATE LIMIT
# ============================================================

BACKOFF_BASE = 5
BACKOFF_MAX = 300

_consecutive_429 = 0
_next_allowed_at = 0.0


# ============================================================
# CACHE
#
# IMPORTANT:
#
# A ticket is stored ONLY while it is waiting for the
# 5-minute timer.
#
# Example:
#
# {
#     "123456": {
#         "first_seen": "2026-09-25 22:30:00",
#         "notified": true
#     }
# }
#
# Once the ticket is successfully put On-hold:
#
#     del tickets_cache["123456"]
#
# This is intentional.
#
# If the customer later replies and the ticket becomes Open
# again, it will appear in the view again and get a NEW
# 5-minute timer.
# ============================================================

def load_cache():

    if not os.path.exists(CACHE_FILE):

        print(
            "ℹ No hold-monitor cache found."
        )

        print(
            "ℹ Starting with empty cache."
        )

        return {}

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        tickets = data.get(
            "tickets",
            {}
        )

        print(
            f"✓ Cache loaded: "
            f"{len(tickets)} active timers"
        )

        return tickets

    except Exception as e:

        print(
            f"⚠ Cache could not be read: {e}"
        )

        print(
            "ℹ Starting with empty cache."
        )

        return {}


def save_cache(tickets):

    try:

        data = {
            "last_updated":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "tickets":
                tickets
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
            f"({len(tickets)} active timers)"
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
        "New ticket detected in your "
        "Zendesk view.\n\n"

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
# ON-HOLD EMAIL
# ============================================================

def send_hold_email(
    tid,
    subject
):

    email_subject = (
        f"Zendesk Ticket #{tid} Put On-hold"
    )

    email_body = (
        "A Zendesk ticket has been "
        "automatically put On-hold.\n\n"

        f"Ticket ID : {tid}\n"
        f"Subject   : {subject}\n"
        f"Status    : On-hold\n"
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
# PUT TICKET ON-HOLD
# ============================================================

def put_ticket_on_hold(
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

    # --------------------------------------------------------
    # Zendesk API status:
    #
    #     "hold"
    #
    # This corresponds to "Submit as On-hold".
    # --------------------------------------------------------

    payload = {
        "ticket": {
            "status": "hold"
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

        # ====================================================
        # RATE LIMIT
        # ====================================================

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
                f"     ⚠ API rate limited "
                f"(HTTP 429). "
                f"Back-off {wait_secs}s."
            )

            return False, 429

        # ====================================================
        # AUTHENTICATION
        # ====================================================

        if response.status in (
            401,
            403
        ):

            print(
                f"     ❌ Authentication failure "
                f"while putting #{ticket_id} "
                f"On-hold: HTTP "
                f"{response.status}"
            )

            return False, response.status

        # ====================================================
        # OTHER ERROR
        # ====================================================

        if not response.ok:

            print(
                f"     ✗ Could not put "
                f"#{ticket_id} On-hold."
            )

            print(
                f"       HTTP: "
                f"{response.status}"
            )

            try:

                print(
                    f"       "
                    f"{response.text()[:1000]}"
                )

            except Exception:
                pass

            return False, response.status

        # ====================================================
        # SUCCESS
        # ====================================================

        _consecutive_429 = 0

        try:

            data = response.json()

            ticket = data.get(
                "ticket",
                {}
            )

            returned_status = ticket.get(
                "status"
            )

            if returned_status:

                print(
                    f"     ✓ Zendesk returned "
                    f"status: {returned_status}"
                )

        except Exception:
            pass

        print(
            f"     ✅ Ticket #{ticket_id} "
            f"successfully put On-hold."
        )

        return True, None

    except Exception as e:

        print(
            f"     ✗ On-hold API exception: "
            f"{e}"
        )

        return False, None


# ============================================================
# PROCESS TICKETS
# ============================================================

def process_tickets(
    page,
    csrf_token,
    tickets_cache
):

    # --------------------------------------------------------
    # Open / refresh the view
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
            f"     ✗ Could not load view: {e}"
        )

        return tickets_cache

    # --------------------------------------------------------
    # Find ticket rows
    # --------------------------------------------------------

    rows = find_ticket_rows(page)

    print()
    print(
        f"[{datetime.now():%Y-%m-%d %H:%M:%S}] "
        f"Tickets currently in view: {len(rows)}"
    )

    # --------------------------------------------------------
    # Snapshot current tickets
    # --------------------------------------------------------

    snapshot = []

    for row in rows:

        try:

            tid = get_ticket_id(row)
            subject = get_subject(row)

            if tid:

                if not subject:

                    subject = (
                        f"Zendesk Ticket #{tid}"
                    )

                snapshot.append(
                    (
                        str(tid),
                        subject
                    )
                )

        except Exception as e:

            print(
                f"     ⚠ Could not read row: "
                f"{e}"
            )

    # ========================================================
    # PROCESS CURRENT TICKETS
    # ========================================================

    now = datetime.now()

    for tid, subject in snapshot:

        try:

            # =================================================
            # FIRST TIME WE SEE THIS TICKET
            # =================================================

            if tid not in tickets_cache:

                first_seen = now.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                tickets_cache[tid] = {
                    "first_seen": first_seen,
                    "notified": False
                }

                print()
                print("-" * 60)

                print(
                    f"🆕 NEW OPEN TICKET #{tid}"
                )

                print(
                    f"   Subject    : {subject}"
                )

                print(
                    f"   First seen : {first_seen}"
                )

                print(
                    "   Timer      : 5 minutes"
                )

                # ------------------------------------------------
                # Send notification email
                # ------------------------------------------------

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

                    tickets_cache[tid][
                        "notified"
                    ] = True

                    print(
                        "   ✓ Email notification recorded."
                    )

                else:

                    print(
                        "   ⚠ Email failed."
                    )

                save_cache(
                    tickets_cache
                )

            # =================================================
            # EXISTING TICKET
            # =================================================

            ticket_data = tickets_cache.get(
                tid
            )

            if not ticket_data:

                continue

            # =================================================
            # RETRY EMAIL IF PREVIOUS ATTEMPT FAILED
            # =================================================

            if not ticket_data.get(
                "notified",
                False
            ):

                print(
                    f"     📧 Retrying email "
                    f"for #{tid}..."
                )

                email_ok = (
                    send_new_ticket_email(
                        tid,
                        subject
                    )
                )

                if email_ok:

                    ticket_data[
                        "notified"
                    ] = True

                    save_cache(
                        tickets_cache
                    )

                    print(
                        "     ✓ Email sent."
                    )

            # =================================================
            # GET FIRST-SEEN TIME
            # =================================================

            first_seen_string = (
                ticket_data.get(
                    "first_seen"
                )
            )

            try:

                first_seen = datetime.strptime(
                    first_seen_string,
                    "%Y-%m-%d %H:%M:%S"
                )

            except Exception:

                print(
                    f"     ⚠ Invalid timer "
                    f"for #{tid}."
                )

                # Reset timer safely
                ticket_data[
                    "first_seen"
                ] = now.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                save_cache(
                    tickets_cache
                )

                continue

            # =================================================
            # CALCULATE AGE
            # =================================================

            age_seconds = (
                now - first_seen
            ).total_seconds()

            age_minutes = (
                age_seconds / 60
            )

            # =================================================
            # LESS THAN 5 MINUTES
            # =================================================

            if age_seconds < HOLD_AFTER_SECONDS:

                remaining_seconds = (
                    HOLD_AFTER_SECONDS
                    - age_seconds
                )

                remaining_minutes = (
                    remaining_seconds / 60
                )

                print(
                    f"     ⏳ #{tid} "
                    f"open for "
                    f"{age_minutes:.1f} min "
                    f"— "
                    f"{remaining_minutes:.1f} min "
                    f"remaining."
                )

                continue

            # =================================================
            # 5 MINUTES REACHED
            # =================================================

            print()
            print("-" * 60)

            print(
                "⏰ 5-MINUTE LIMIT REACHED"
            )

            print(
                f"   Ticket  : #{tid}"
            )

            print(
                f"   Subject : {subject}"
            )

            print(
                f"   Age     : "
                f"{age_minutes:.1f} minutes"
            )

            print(
                "   Action  : Submit as On-hold"
            )

            # =================================================
            # CHECK API BACKOFF
            # =================================================

            if time.time() < _next_allowed_at:

                remaining = int(
                    _next_allowed_at
                    - time.time()
                ) + 1

                print(
                    f"   ⚠ API back-off active."
                )

                print(
                    f"   Will retry in "
                    f"{remaining}s."
                )

                continue

            # =================================================
            # PUT ON-HOLD
            # =================================================

            (
                hold_ok,
                error_status
            ) = put_ticket_on_hold(
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
                    "   ❌ Authentication failed."
                )

                print(
                    "   Ticket remains in cache "
                    "and will retry."
                )

                continue

            # =================================================
            # RATE LIMIT
            # =================================================

            if error_status == 429:

                print(
                    "   ⚠ API rate limited."
                )

                print(
                    "   Ticket remains in cache "
                    "and will retry."
                )

                continue

            # =================================================
            # SUCCESSFUL ON-HOLD
            # =================================================

            if hold_ok:

                # ------------------------------------------------
                # THIS IS THE IMPORTANT PART
                #
                # REMOVE FROM CACHE.
                #
                # There is NO permanent protection.
                #
                # If the customer later replies and Zendesk
                # makes the ticket Open again, it will appear
                # in the view as a new ticket occurrence and
                # receive a fresh 5-minute timer.
                # ------------------------------------------------

                if tid in tickets_cache:

                    del tickets_cache[tid]

                save_cache(
                    tickets_cache
                )

                print()
                print(
                    f"     🗑 Ticket #{tid} "
                    f"removed from timer cache."
                )

                print(
                    "     ✓ If it opens again later, "
                    "a new 5-minute timer will start."
                )

                # ------------------------------------------------
                # Send On-hold email
                # ------------------------------------------------

                print(
                    "     📧 Sending On-hold email..."
                )

                hold_email_ok = (
                    send_hold_email(
                        tid,
                        subject
                    )
                )

                if hold_email_ok:

                    print(
                        "     ✓ On-hold email sent."
                    )

                else:

                    print(
                        "     ⚠ On-hold email failed."
                    )

            # =================================================
            # FAILED ON-HOLD
            # =================================================

            else:

                print(
                    f"     ✗ Could not put "
                    f"#{tid} On-hold."
                )

                print(
                    "     Ticket remains in cache "
                    "and will retry."
                )

        except Exception as e:

            print(
                f"     ✗ Error processing "
                f"#{tid}: {e}"
            )

    return tickets_cache


# ============================================================
# MONITOR
# ============================================================

def monitor_zendesk_tickets():

    tickets_cache = load_cache()

    print()
    print("=" * 65)
    print("        ZENDESK ON-HOLD MONITOR")
    print("=" * 65)

    print(
        f"Zendesk URL : {ZENDESK_URL}"
    )

    print(
        f"View URL    : {FILTER_URL}"
    )

    print(
        f"Email From  : {MAIL_FROM}"
    )

    print(
        f"Email To    : {MAIL_TO}"
    )

    print(
        f"Cache File  : {CACHE_FILE}"
    )

    print(
        f"Refresh     : every {CHECK_EVERY} seconds"
    )

    print(
        f"On-hold     : after "
        f"{HOLD_AFTER_SECONDS // 60} minutes"
    )

    print()
    print("Rules:")
    print(
        "  • View contains the tickets to monitor"
    )

    print(
        "  • No assignee checks"
    )

    print(
        "  • No group checks"
    )

    print(
        "  • No keyword checks"
    )

    print(
        "  • No SLA checks"
    )

    print(
        "  • First appearance → start 5-minute timer"
    )

    print(
        "  • First appearance → send email"
    )

    print(
        "  • 5 minutes → Submit as On-hold"
    )

    print(
        "  • Successful On-hold → remove from cache"
    )

    print(
        "  • Reopened later → NEW 5-minute timer"
    )

    print("=" * 65)
    print()

    # ========================================================
    # PLAYWRIGHT
    # ========================================================

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        # ----------------------------------------------------
        # Load existing Zendesk session
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
        # INITIAL ACCESS
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
                "ticket view is visible..."
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
        # OPEN VIEW AGAIN
        # ====================================================

        try:

            page.goto(
                FILTER_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            time.sleep(3)

        except Exception as e:

            print(
                f"❌ Could not open ticket view: {e}"
            )

            browser.close()

            return

        # ====================================================
        # GET CSRF TOKEN
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
                "Cannot safely update ticket status."
            )

            browser.close()

            return

        print(
            "✓ CSRF token found."
        )

        # ====================================================
        # START MONITOR
        # ====================================================

        print()
        print("=" * 65)
        print("🚀 ON-HOLD MONITOR STARTED")
        print("=" * 65)
        print()

        while True:

            try:

                # ------------------------------------------------
                # Reload cache from disk
                #
                # This allows the cache to remain persistent
                # if the script is restarted.
                # ------------------------------------------------

                tickets_cache = load_cache()

                # ------------------------------------------------
                # Process current view
                # ------------------------------------------------

                tickets_cache = (
                    process_tickets(
                        page,
                        csrf_token,
                        tickets_cache
                    )
                )

                # ------------------------------------------------
                # Save cache
                # ------------------------------------------------

                save_cache(
                    tickets_cache
                )

                # ------------------------------------------------
                # Wait one minute
                # ------------------------------------------------

                now = time.time()

                if now < _next_allowed_at:

                    remaining = int(
                        _next_allowed_at
                        - now
                    ) + 1

                    print()
                    print(
                        f"💤 API rate limit active. "
                        f"Waiting {remaining}s..."
                    )

                    time.sleep(
                        remaining
                    )

                else:

                    print()
                    print(
                        f"🔄 Refreshing view again "
                        f"in {CHECK_EVERY} seconds..."
                    )

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
                    tickets_cache
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
                    tickets_cache
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
    print("=" * 65)
    print("        ZENDESK ON-HOLD MONITOR")
    print("=" * 65)
    print()

    monitor_zendesk_tickets()
