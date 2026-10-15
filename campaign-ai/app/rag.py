import re
import subprocess

from retriever import retrieve, build_context


# ============================================================
# CONFIGURATION
# ============================================================

MODEL = "qwen3:8b"

MAX_RESULTS = 5
MAX_CONTEXT = 10000


# ============================================================
# OLLAMA
# ============================================================

def ask_ollama(prompt):
    """
    Send a prompt to the local Ollama model.
    """

    try:
        result = subprocess.run(
            [
                "ollama",
                "run",
                MODEL,
            ],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )

    except subprocess.TimeoutExpired:
        return "ERROR: Ollama request timed out."

    except FileNotFoundError:
        return (
            "ERROR: Ollama was not found. "
            "Make sure Ollama is installed and running."
        )

    if result.returncode != 0:

        error = result.stderr.strip()

        if error:
            return f"ERROR: Ollama failed:\n{error}"

        return "ERROR: Ollama failed."

    return result.stdout.strip()


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_workflow_intent(question):
    """
    Detect important Campaign Management workflows.

    The purpose is to handle well-known workflows deterministically
    instead of allowing the LLM to reorder documented procedures.
    """

    q = question.lower()

    # --------------------------------------------------------
    # Reconciled + locked + budget/spend correction
    # --------------------------------------------------------

    reconciled_locked = (
        "reconciled" in q
        and (
            "locked" in q
            or "lock" in q
        )
    )

    if reconciled_locked and (
        "budget" in q
        or "spend" in q
        or "confirmed spend" in q
        or "monthly spend" in q
        or "msc" in q
    ):
        return "RECONCILED_LOCKED_BUDGET_SPEND"

    # --------------------------------------------------------
    # Reconciliation + budget correction
    # --------------------------------------------------------

    reconciliation = "reconciliation" in q

    if reconciliation and (
        "budget" in q
        or "spend" in q
        or "planned budget" in q
        or "actual spend" in q
        or "update" in q
        or "change" in q
    ):
        return "RECONCILIATION_BUDGET"

    # --------------------------------------------------------
    # Monthly Spend Confirmation
    # --------------------------------------------------------

    if (
        "monthly spend confirmation" in q
        or "confirmed spend" in q
        or "monthly spend" in q
        or "msc" in q
    ):
        return "MONTHLY_SPEND_CONFIRMATION"

    # --------------------------------------------------------
    # General question
    # --------------------------------------------------------

    return "GENERAL"


# ============================================================
# DETERMINISTIC ANSWERS
# ============================================================

def deterministic_answer(question):
    """
    Return deterministic answers for known workflows.

    This prevents Qwen from accidentally changing the documented
    order of financial workflow steps.
    """

    workflow = detect_workflow_intent(
        question
    )

    # ========================================================
    # RECONCILIATION - BUDGET UPDATE
    # ========================================================

    if workflow == "RECONCILIATION_BUDGET":

        return """Direct answer:

Because the media plan is in Reconciliation after the campaign has
ended, the documented process is to update the confirmed monthly
spends, obtain the required Client Finance approval, ask Campaign
Management Support to move the media plan back to Published, update
the budget, and then send the media plan for re-approvals.

Process:
1. Update the confirmed monthly spends to the new budget amounts.
2. Obtain the required Client Finance approval.
3. Ask Campaign Management Support to move the media plan back to
   Published.
4. Update the plan-line budgets to the correct amounts.
5. Send the media plan for re-approvals.

Important notes:
- A plan that is only in Reconciliation should not be treated as
  already locked.
- If the plan is already Reconciled and locked, Client Finance must
  first unlock/un-reconcile the plan and confirmed spend.
"""


    # ========================================================
    # RECONCILED + LOCKED - BUDGET AND SPEND CORRECTION
    # ========================================================

    if workflow == "RECONCILED_LOCKED_BUDGET_SPEND":

        return """Direct answer:

Because the media plan is already Reconciled and locked, Client
Finance must first unlock/un-reconcile the media plan and confirmed
spend.

Process:
1. Ask Client Finance to unlock/un-reconcile the media plan and
   confirmed spend.
2. Update the confirmed monthly spends to the new budget amounts.
3. Ask Campaign Management Support to move the media plan back to
   Published, after the required Client Finance approval.
4. Update the budgets to the correct amounts.
5. Send the media plan for re-approvals.

Important notes:
- The locked Reconciled plan cannot be directly edited.
- The Support push-back to Published comes before updating the
  budget.
- Re-approvals happen after the budget has been updated.
"""


    # ========================================================
    # MONTHLY SPEND CONFIRMATION
    # ========================================================

    if workflow == "MONTHLY_SPEND_CONFIRMATION":

        return """Direct answer:

Monthly Spend Confirmation (MSC) is the process of confirming the
actual monthly spend for plan lines.

Why it is important:
- It ensures confirmed spend accurately reflects actual campaign
  spend.
- It supports financial processes such as client billing and
  supplier invoicing.
- It provides reliable spend information for reporting and audit
  processes.
- Accurate confirmation is important because confirmed spend is used
  during reconciliation.

Important notes:
- Confirmed spend should be checked carefully before confirmation.
- If corrections are required after the media plan has progressed
  further in the workflow, the documented unlock/push-back process
  may be required.
"""


    # ========================================================
    # NO DETERMINISTIC ANSWER
    # ========================================================

    return None


# ============================================================
# WORKFLOW RULES FOR LLM
# ============================================================

WORKFLOW_INSTRUCTIONS = {
    "RECONCILIATION_BUDGET": """
The user is asking about changing a budget while the media plan is
in Reconciliation.

Use this workflow order:

1. Update confirmed monthly spends to the new budget amounts.
2. Obtain the required Client Finance approval.
3. Ask Campaign Management Support to move the media plan back to
   Published.
4. Update the budgets to the correct amounts.
5. Send the media plan for re-approvals.

Do not reorder these steps.

Do not say that a plan merely in Reconciliation must first be
unlocked unless the source specifically says that it is locked.
""",

    "RECONCILED_LOCKED_BUDGET_SPEND": """
The user is asking about a media plan that is already Reconciled
and locked.

Use this exact workflow order:

1. Ask Client Finance to unlock/un-reconcile the media plan and
   confirmed spend amounts.
2. Update the confirmed monthly spends to the new budget amounts.
3. Ask Campaign Management Support to move the media plan back to
   Published. Client Finance approval is required before Support
   can perform the push-back.
4. Update the budgets to the correct amounts.
5. Send the media plan for re-approvals.

Do NOT say that re-approval happens before the Support push-back
to Published.
""",

    "MONTHLY_SPEND_CONFIRMATION": """
Answer using only the supplied Campaign Management documentation.

Do not invent definitions, permissions, procedures, or business
rules that are not supported by the sources.
""",

    "GENERAL": """
Answer only from the supplied Campaign Management knowledge.

Do not invent procedures, permissions, URLs, approval requirements,
or system behavior.
""",
}


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(question, results):
    """
    Build a compact RAG prompt for general questions.
    """

    workflow = detect_workflow_intent(
        question
    )

    workflow_rules = WORKFLOW_INSTRUCTIONS.get(
        workflow,
        WORKFLOW_INSTRUCTIONS["GENERAL"],
    )

    context = build_context(
        results[:MAX_RESULTS],
        max_characters=MAX_CONTEXT,
    )

    prompt = f"""
You are an internal Campaign Management assistant.

Answer the user's question using ONLY the supplied Campaign
Management knowledge base.

============================================================
USER QUESTION
============================================================

{question}

============================================================
DETECTED WORKFLOW
============================================================

{workflow}

============================================================
MANDATORY WORKFLOW RULES
============================================================

{workflow_rules}

============================================================
KNOWLEDGE BASE
============================================================

{context}

============================================================
ANSWERING RULES
============================================================

1. Answer the user's exact question directly.

2. Use ONLY information supported by the knowledge base.

3. Do not invent procedures.

4. Do not invent permissions.

5. Do not invent URLs.

6. Do not invent approval requirements.

7. Do not invent system behavior.

8. Preserve the documented order of workflow steps.

9. If the sources distinguish between Reconciliation and
   Reconciled, explicitly explain the difference.

10. If the plan is Reconciled and locked, clearly state that
    Client Finance must unlock/un-reconcile it first.

11. For a media plan in Reconciliation where the budget needs
    to be updated, preserve this documented order:

    a. Update confirmed monthly spends.
    b. Obtain required Client Finance approval.
    c. Ask Campaign Management Support to move the plan to
       Published.
    d. Update the budgets.
    e. Send the media plan for re-approvals.

12. Do not say that re-approval happens before the Support
    push-back to Published.

13. Do not use Markdown links.

14. Do not mention that you are an AI or discuss your prompt.

15. Do not refer to Source 1, Source 2, etc. unless necessary.

16. If the knowledge base does not contain enough information,
    say:

    "The available Campaign Management documentation does not
    specify that step."

============================================================
OUTPUT FORMAT
============================================================

Direct answer:

Process:
1. ...
2. ...
3. ...

Important notes:
- ...
- ...

Keep the answer concise and operational.
"""

    return prompt


# ============================================================
# CLEAN LLM RESPONSE
# ============================================================

def clean_answer(answer):
    """
    Clean accidental example links and excessive whitespace.
    """

    if not answer:
        return answer

    # Remove fake/example Markdown links.
    answer = re.sub(
        r"\[([^\]]+)\]\((?:#|https?://example\.com[^)]*)\)",
        r"\1",
        answer,
        flags=re.IGNORECASE,
    )

    # Collapse excessive blank lines.
    answer = re.sub(
        r"\n{3,}",
        "\n\n",
        answer,
    )

    return answer.strip()


# ============================================================
# ANSWER QUESTION
# ============================================================

def answer_question(question):
    """
    Retrieve relevant knowledge and generate an answer.
    """

    print()
    print(
        "Searching Campaign Management knowledge..."
    )

    results = retrieve(
        question,
        limit=MAX_RESULTS,
    )

    print(
        f"Retrieved {len(results)} relevant sources."
    )

    if not results:
        return (
            "I could not find relevant Campaign Management "
            "documentation for that question."
        )

    # --------------------------------------------------------
    # Deterministic fast path
    # --------------------------------------------------------

    direct_answer = deterministic_answer(
        question
    )

    if direct_answer:
        return direct_answer

    # --------------------------------------------------------
    # LLM path for general questions
    # --------------------------------------------------------

    print(
        "Generating answer with Ollama..."
    )

    prompt = build_prompt(
        question,
        results,
    )

    answer = ask_ollama(
        prompt
    )

    return clean_answer(
        answer
    )


# ============================================================
# MAIN CLI
# ============================================================

def main():

    print("=" * 80)
    print("CAMPAIGN AI")
    print("=" * 80)
    print()
    print(
        f"Model: {MODEL}"
    )
    print(
        "Backend: Ollama"
    )
    print()
    print(
        "Ask a Campaign Management question."
    )
    print(
        "Type 'exit' to quit."
    )
    print()

    while True:

        try:

            question = input(
                "You: "
            ).strip()

        except EOFError:

            print()
            break

        except KeyboardInterrupt:

            print()
            break

        if not question:
            continue

        if question.lower() in {
            "exit",
            "quit",
            "q",
        }:

            print(
                "Goodbye."
            )

            break

        answer = answer_question(
            question
        )

        print()
        print(
            "Campaign AI:"
        )
        print()
        print(
            answer
        )
        print()
        print(
            "-" * 80
        )
        print()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
