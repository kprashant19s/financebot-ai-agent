import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from tools.schema_reader import get_schema
from tools.sql_executor import execute_sql
from agent.prompts import get_system_prompt, get_human_prompt

load_dotenv()


def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )


def is_finance_question(question: str) -> bool:
    llm = get_llm()
    messages = [
        SystemMessage(content="""You are a classifier. 
Determine if the question is related to personal finance data such as 
transactions, spending, income, budgets, accounts, or categories.
Reply with only YES or NO."""),
        HumanMessage(content=f"Question: {question}")
    ]
    response = llm.invoke(messages)
    return response.content.strip().upper().startswith("YES")


def generate_sql(question: str, schema: str) -> str:
    llm = get_llm()
    messages = [
        SystemMessage(content=get_system_prompt(schema)),
        HumanMessage(content=get_human_prompt(question))
    ]
    response = llm.invoke(messages)
    sql = response.content.strip()

    # Clean up if model adds markdown code fences
    if sql.startswith("```"):
        sql = sql.split("```")[1]
        if sql.startswith("sql"):
            sql = sql[3:]
    return sql.strip()


def run_agent(question: str) -> dict:
    print(f"\nQuestion: {question}")
    print("-" * 50)

# Check if question is relevant
    if not is_finance_question(question):
        return {
            "question": question,
            "sql": None,
            "success": False,
            "error": "I can only answer questions about your finance data — spending, income, budgets, and accounts."
        }

    # Step 1: Get schema
    schema = get_schema()

    # Step 2: Generate SQL
    print("Generating SQL...")
    sql = generate_sql(question, schema)
    print(f"Generated SQL:\n{sql}\n")

    # Step 3: Execute SQL
    print("Executing SQL...")
    success, data, message = execute_sql(sql)
    print(f"Result: {message}")

    if not success:
        return {"question": question, "sql": sql, "success": False, "error": message}

    return {
        "question": question,
        "sql": sql,
        "success": True,
        "data": data,
        "message": message
    }


if __name__ == "__main__":
    result = run_agent(
        "Show total expenses by month for 2024")
    if result["success"]:
        print("\nData:")
        print(result["data"])
