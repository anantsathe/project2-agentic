import re
import sqlite3

#GA-1, Q18
def solve_ga_1_q18(question):
    """Process SQL-related questions and return the SQL query or computed result."""

    if not question or not isinstance(question, str):
        return {"error": "Invalid input: Question text is missing or not in string format."}

    # If the question asks for SQL query
    if "tickets table" in question.lower() and "write sql" in question.lower():
        sql_query = """
        SELECT SUM(units * price) AS total_sales
        FROM tickets
        WHERE lower(trim(type)) = 'gold'
        LIMIT 1;
        """
        return {"sql_query": sql_query.strip()}  # Return SQL query

    # If the question asks for computed total sales of "Gold" tickets
    if "tickets table" in question.lower() and "total sales" in question.lower():
        table_data = re.findall(r"([\w\s]+)\s+(\d+)\s+([\d.]+)", question)

        if not table_data:
            return {"error": "Could not extract table data"}

        # Create an in-memory SQLite database
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        # Create the tickets table
        cursor.execute("""
        CREATE TABLE tickets (
            type TEXT,
            units INTEGER,
            price REAL
        )
        """)

        # Insert extracted data, cleaning up type names
        for ticket_type, units, price in table_data:
            cleaned_type = ticket_type.strip().lower()
            normalized_type = "Gold" if cleaned_type == "gold" else ticket_type.strip()
            cursor.execute("INSERT INTO tickets (type, units, price) VALUES (?, ?, ?)", (normalized_type, units, price))

        conn.commit()

        # Run SQL query to calculate total sales for "Gold" tickets (case-insensitive)
        cursor.execute("SELECT SUM(units * price) AS total_sales FROM tickets WHERE lower(trim(type)) = 'gold' LIMIT 1")
        total_sales = cursor.fetchone()[0]

        conn.close()

        return {"answer": str(total_sales) if total_sales else "0"}

    return {"error": "The question does not match the expected SQL-related format."}
