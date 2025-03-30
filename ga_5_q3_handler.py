import gzip
import re
from datetime import datetime
from fastapi import UploadFile

async def solve_ga_5_q3(file: UploadFile):
    """
    Count successful GET requests under /malayalam/ on Wednesdays between 00:00-06:00 (GMT-5)
    from a GZipped Apache log file.
    """
    try:
        content = await file.read()
        decompressed_data = gzip.decompress(content).decode("utf-8")

        # Define filters
        target_day = "Wed"
        target_time_range = (0, 6)
        target_path = "/malayalam/"

        # Regex pattern to extract relevant log components
        log_pattern = re.compile(
            r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] '
            r'"(?P<method>\w+) (?P<url>[^\s]+) (?P<protocol>[^"]+)" (?P<status>\d+)'
        )

        count = 0  # Counter for successful GET requests

        for line in decompressed_data.splitlines():
            match = log_pattern.search(line)
            if match:
                method = match.group("method")
                url = match.group("url")
                status = int(match.group("status"))
                timestamp = match.group("timestamp")

                # Convert timestamp to datetime object
                log_time = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")

                # Apply filters: Wednesday, 00:00-06:00, successful GET, correct URL
                if (
                    log_time.strftime("%a") == target_day
                    and target_time_range[0] <= log_time.hour < target_time_range[1]
                    and method == "GET"
                    and target_path in url
                    and 200 <= status < 300
                ):
                    count += 1

        return {"answer": str(count)}

    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}
