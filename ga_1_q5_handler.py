import re
import numpy as np
from fastapi import HTTPException

def evaluate_excel_formula(question: str):
    """Detect and evaluate Excel formulas like SUM, TAKE, and SORTBY."""
    if "Excel" in question and "SUM" in question:
        # Regex to extract the number array and sorting keys
        match = re.search(r"=SUM\(TAKE\(SORTBY\(\{([\d, ]+)\}, \{([\d, ]+)\}\), (\d+), (\d+)\)\)", question)
        if match:
            array_numbers = list(map(int, match.group(1).split(',')))
            sorting_keys = list(map(int, match.group(2).split(',')))
            take_rows = int(match.group(3))
            take_cols = int(match.group(4))
            
            # Convert lists to NumPy arrays
            data_array = np.array(array_numbers)
            sorting_array = np.array(sorting_keys)
            
            # Sort data array based on sorting array
            sorted_indices = np.argsort(sorting_array)
            sorted_data = data_array[sorted_indices]
            
            # Apply TAKE (select first `take_cols` elements)
            taken_data = sorted_data[:take_cols]
            
            # Compute SUM of selected values
            result = np.sum(taken_data)
            return {"answer": str(result)}
    
    return None  # Not an Excel formula

def solve_ga_1_q5(question: str):
    """Extracts the formula from the question, evaluates it programmatically, and returns the computed answer."""
    print("🎯 Executing `ga_1_q5_handler.py` to process Excel formula!")
    
    if not question:
        raise HTTPException(status_code=400, detail="Question parameter is required for GA-1-Q5.")
    
    # Try evaluating Excel formula
    excel_result = evaluate_excel_formula(question)
    if excel_result:
        return excel_result
    
    raise HTTPException(status_code=400, detail="Unsupported question format for GA-1-Q5.")
