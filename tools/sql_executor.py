import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from tools.sql_validator import validate_sql
from urllib.parse import quote_plus

load_dotenv()


def get_engine():
    user = os.getenv("DB_USER")
    password = quote_plus(os.getenv("DB_PASSWORD"))
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    return create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")


def execute_sql(sql: str) -> tuple[bool, any, str]:
    """
    Returns (success, data, message)
    success = True means query ran successfully
    data = pandas DataFrame with results
    message = error or success message
    """

    # First validate the SQL
    is_safe, reason = validate_sql(sql)
    if not is_safe:
        return False, None, f"Query blocked: {reason}"

    try:
        engine = get_engine()
        with engine.connect() as connection:
            df = pd.read_sql(text(sql), connection)

        if df.empty:
            return True, df, "Query returned no results."

        return True, df, f"Query returned {len(df)} rows."

    except Exception as e:
        return False, None, f"Database error: {str(e)}"


if __name__ == "__main__":
    sql = "SELECT t.transaction_date, c.name as category, t.amount FROM transactions t JOIN categories c ON t.category_id = c.id LIMIT 5"

    success, data, message = execute_sql(sql)
    print(f"Status: {message}")
    if success and data is not None:
        print(data)
