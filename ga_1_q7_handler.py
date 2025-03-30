from datetime import datetime, timedelta
import re

def solve_ga_1_q7(question: str):
    """
    Function to count the number of Wednesdays in a given date range.

    :param question: The input question containing the date range.
    :return: JSON response with the count of Wednesdays.
    """
    try:
        # Extract dates using regex
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        dates = re.findall(date_pattern, question)

        if len(dates) != 2:
            return {"error": "Invalid date range format in question."}

        start_date = datetime.strptime(dates[0], "%Y-%m-%d")
        end_date = datetime.strptime(dates[1], "%Y-%m-%d")

        # Ensure start date is before end date
        if start_date > end_date:
            return {"error": "Start date cannot be after end date."}

        # Count Wednesdays (where weekday() == 2)
        count = sum(1 for i in range((end_date - start_date).days + 1)
                    if (start_date + timedelta(days=i)).weekday() == 2)

        return {"answer": str(count)}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
