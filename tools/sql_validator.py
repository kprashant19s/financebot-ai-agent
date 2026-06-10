import re

FORBIDDEN_KEYWORDS = [
    "DROP", "DELETE", "INSERT", "UPDATE", "TRUNCATE",
    "ALTER", "CREATE", "REPLACE", "GRANT", "REVOKE"
]


def validate_sql(sql: str) -> tuple[bool, str]:
    """
    Returns (is_safe, message)
    is_safe = True means query is allowed
    is_safe = False means query is blocked
    """
    sql_upper = sql.upper().strip()

    # Must start with SELECT
    if not sql_upper.startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    # Check for forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        pattern = r'\b' + keyword + r'\b'
        if re.search(pattern, sql_upper):
            return False, f"Query contains forbidden keyword: {keyword}"

    # Block multiple statements
    if ";" in sql.rstrip(";"):
        return False, "Multiple statements are not allowed."

    return True, "Query is safe."


if __name__ == "__main__":
    # Test cases
    tests = [
        "SELECT * FROM transactions",
        "DROP TABLE transactions",
        "SELECT * FROM transactions; DELETE FROM transactions",
        "UPDATE accounts SET balance = 0",
        "SELECT amount FROM transactions WHERE account_id = 1"
    ]

    for sql in tests:
        is_safe, message = validate_sql(sql)
        status = "✅ ALLOWED" if is_safe else "❌ BLOCKED"
        print(f"{status}: {sql[:50]}")
        print(f"         Reason: {message}\n")
