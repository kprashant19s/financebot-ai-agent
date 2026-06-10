import sys
from agent.agent import run_agent
from viz.chart_generator import generate_chart


def main():
    print("=" * 60)
    print("   FinanceBot — Autonomous Data Insights Agent")
    print("=" * 60)

    while True:
        print("\nAsk a question about your finance data.")
        print("Type 'exit' to quit.\n")

        question = input("Your question: ").strip()

        if question.lower() == 'exit':
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        # Run the agent
        result = run_agent(question)

        if not result["success"]:
            print(f"\nError: {result['error']}")
            continue

        # Show the data
        if result["data"].empty:
            print("\nNo data found for your question.")
            print("This might mean the time period has no transactions.")
            continue

        print("\nResults:")
        print(result["data"])

       # Generate chart
        rows, cols = result["data"].shape
        if rows == 1 and cols == 1:
            value = result["data"].iloc[0, 0]
            col_name = result["data"].columns[0]
            print(f"\nAnswer: {col_name} = {value:,.2f}")
        else:
            fig = generate_chart(result["data"], question)
            if fig:
                fig.show()
                print("\nChart opened in browser.")
            else:
                print("\nNo chart generated for this result shape.")


if __name__ == "__main__":
    main()
