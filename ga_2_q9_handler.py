import re


# GA-2 Q9
def solve_ga_2_q9 (question: str):     #  extract_api_url
    match = re.search(r"http://\S+", question)
    if match:
        return {"answer": match.group(0)}
    return None


# ✅ Sample student data
students_data = [
    {"name": "Alice", "class": "1A"},
    {"name": "Bob", "class": "1B"},
    {"name": "Charlie", "class": "1A"},
    {"name": "David", "class": "2A"},
]