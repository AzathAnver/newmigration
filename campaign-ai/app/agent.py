from rag import answer_question


class CampaignAgent:

    def ask(
        self,
        question: str,
    ):

        return answer_question(
            question
        )


def main():

    agent = CampaignAgent()

    print()
    print("=" * 80)
    print("CAMPAIGN AI AGENT")
    print("=" * 80)

    print()
    print("Powered by Ollama + Qwen3")

    print()
    print("Ask a question or type 'exit'.")

    while True:

        try:

            question = input(
                "\nYou: "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError,
        ):

            print()
            break

        if not question:
            continue

        if question.lower() in {
            "exit",
            "quit",
            "q",
        }:

            break

        try:

            result = agent.ask(
                question
            )

            print()
            print("-" * 80)
            print("Campaign AI:")
            print("-" * 80)
            print()
            print(
                result["answer"]
            )

        except Exception as exc:

            print()
            print(
                f"[ERROR] {exc}"
            )


if __name__ == "__main__":
    main()
