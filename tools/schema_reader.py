import os
from dotenv import load_dotenv
import pymysql

load_dotenv()


def get_schema():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor()

    # Get all tables
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]

    schema_text = ""

    for table in tables:
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()

        col_definitions = []
        for col in columns:
            col_definitions.append(f"{col[0]} ({col[1]})")

        schema_text += f"Table: {table}\n"
        schema_text += f"Columns: {', '.join(col_definitions)}\n\n"

    cursor.close()
    connection.close()

    return schema_text


if __name__ == "__main__":
    print(get_schema())
