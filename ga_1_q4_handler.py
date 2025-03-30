import re
import numpy as np
from fastapi import HTTPException

def evaluate_google_sheets_formula(question: str):
    """Detect and evaluate Google Sheets formulas like SEQUENCE and SUM."""
    if "Google Sheets" in question and "SEQUENCE" in question:
        match = re.search(r"=SUM\(ARRAY_CONSTRAIN\(SEQUENCE\((\d+), (\d+), (\d+), (\d+)\), (\d+), (\d+)\)\)", question)
        if match:
            rows, cols, start, step, constrain_rows, constrain_cols = map(int, match.groups())
            sequence_array = np.arange(start, start + (rows * cols * step), step).reshape(rows, cols)
            constrained_array = sequence_array[:constrain_rows, :constrain_cols]
            result = np.sum(constrained_array)
            return {"answer": str(result)}
    return None  # Not a Google Sheets formula

def solve_ga_1_q4(question: str):
    """
    Extracts the formula from the question, evaluates it programmatically,
    and returns the computed answer.
    """
    print("🎯 Executing `ga_1_q4_handler.py` to process Google Sheets formula!")
    
    if not question:
        raise HTTPException(status_code=400, detail="Question parameter is required for GA-1-Q4.")
    
    # Try Google Sheets formula evaluation first
    gs_result = evaluate_google_sheets_formula(question)
    if gs_result:
        return gs_result
    
    # Regular expression to extract the SEQUENCE formula parameters
    sequence_pattern = re.search(r'SEQUENCE\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', question)
    if not sequence_pattern:
        raise HTTPException(status_code=400, detail="Could not extract formula parameters from the question.")
    
    rows, cols, start, step = map(int, sequence_pattern.groups())
    
    # Generate the sequence matrix in NumPy
    sequence_matrix = np.arange(start, start + rows * cols * step, step).reshape(rows, cols)
    
    # Extract ARRAY_CONSTRAIN constraints
    array_constrain_pattern = re.search(r'ARRAY_CONSTRAIN\(.*?,\s*(\d+),\s*(\d+)\)', question)
    if array_constrain_pattern:
        max_rows, max_cols = map(int, array_constrain_pattern.groups())
        sequence_matrix = sequence_matrix[:max_rows, :max_cols]
    
    # Extract function type (default is SUM)
    function_pattern = re.search(r'=(\w+)\(', question)
    function_name = function_pattern.group(1).upper() if function_pattern else "SUM"
    
    # Compute result based on function type
    if function_name == "SUM":
        result = np.sum(sequence_matrix)
    elif function_name == "PRODUCT":
        result = np.prod(sequence_matrix)
    elif function_name == "AVERAGE":
        result = np.mean(sequence_matrix)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported function: {function_name}")
    
    return {"answer": str(result)}
