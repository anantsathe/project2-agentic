import requests
import json
import os

def solve_ga_1_q2(
    url="https://httpbin.org/get",
    param_key="email",
    param_value="22f1001679@ds.study.iitm.ac.in",
    method="GET",
    headers=None
):
    """
    Sends an HTTP request with configurable parameters, returns JSON response properly,
    and saves it to a file in the same directory as main.py.
    """

    try:
        # ✅ Default headers (mimicking HTTPie behavior)
        if headers is None:
            headers = {"User-Agent": "HTTPie/3.2.4"}

        # ✅ Prepare request parameters
        params = {param_key: param_value}

        # ✅ Make the HTTP request based on the method
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=5)
        elif method.upper() == "POST":
            response = requests.post(url, data=params, headers=headers, timeout=5)
        else:
            return {"error": f"HTTP method {method} not supported."}

        # ✅ Ensure request was successful
        response.raise_for_status()

        # ✅ Parse response JSON properly
        json_body = response.json()

        # ✅ Save JSON response to a file in the same folder as main.py
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
        output_file_path = os.path.join(script_dir, "http_response.json")

        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(json_body, f, indent=2)

        print(f"✅ JSON response saved to {output_file_path}")

        # ✅ Return JSON response directly (without nesting in `"answer"`)
        return json_body  # ✅ This ensures a clean JSON response

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
