import subprocess

def solve_ga_1_q1():
    """
    Runs the 'code -s' command from WSL using cmd.exe and returns the output.
    """
    try:
        # ✅ Run the command using cmd.exe to ensure compatibility
        result = subprocess.run(
            ["cmd.exe", "/c", "code -s"],
            capture_output=True, text=True, timeout=5, check=True
        )

        # ✅ Clean and return the output
        return {"answer": result.stdout.strip()}

    except subprocess.TimeoutExpired:
        return {"answer": "Error: Command 'code -s' took too long to execute (timeout after 5s)."}

    except subprocess.CalledProcessError as e:
        return {"answer": f"Error: {e.stderr.strip()}"}

    except FileNotFoundError:
        return {"answer": "Error: VS Code is not installed or 'code' command is not recognized."}
