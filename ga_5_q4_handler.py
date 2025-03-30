import gzip
import re
from collections import defaultdict
from datetime import datetime
from fastapi import UploadFile

async def solve_ga_5_q4(file: UploadFile):
    """
    Process an Apache log file (.gz) to find the IP with the highest total downloaded bytes
    for requests strictly under /tamil/ on 2024-05-20.
    """
    try:
        content = await file.read()
        decompressed_data = gzip.decompress(content).decode("utf-8")

        # Define target date and Tamil URL pattern (ensuring strict /tamil/ prefix)
        target_date = "20/May/2024"
        tamil_pattern = re.compile(r'^/tamil/', re.IGNORECASE)  # Match URLs starting with /tamil/

        # Apache log regex pattern
        log_pattern = re.compile(
            r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] '
            r'"(?P<method>GET) (?P<url>/tamil/[^\s]*) (?P<protocol>[^"]+)" '
            r'(?P<status>\d+) (?P<size>\S+)'
        )

        ip_downloads = defaultdict(int)
        filtered_requests = []

        # Step 1: Extract Tamil requests and sum bytes per IP
        for line in decompressed_data.splitlines():
            match = log_pattern.search(line)
            if match:
                ip = match.group("ip")
                url = match.group("url")
                status = int(match.group("status"))
                size = match.group("size")

                # Convert "-" size fields to 0, otherwise parse as int
                size = int(size) if size.isdigit() else 0

                # Extract date from timestamp and check conditions
                timestamp = match.group("timestamp")
                log_dt = datetime.strptime(timestamp[:11], "%d/%b/%Y").strftime("%d/%b/%Y")

                if log_dt == target_date and tamil_pattern.match(url) and 200 <= status < 300:
                    ip_downloads[ip] += size
                    filtered_requests.append((ip, url, size))  # Debugging logs

        # 🔍 Debugging Output
        print(f"✅ Filtered Tamil Requests ({len(filtered_requests)} entries):")
        for ip, url, size in filtered_requests:
            print(f"✔ IP={ip}, Bytes={size}, URL={url}")

        # Debug: Print aggregated data for verification
        print(f"📊 Aggregated data by IP: {dict(ip_downloads)}")

        # Step 3: Identify the top IP by download volume
        if ip_downloads:
            top_ip, max_bytes = max(ip_downloads.items(), key=lambda x: x[1])
            print(f"🏆 Top IP: {top_ip} with {max_bytes} bytes")
            return {"answer": str(max_bytes)}
        else:
            return {"answer": "0"}

    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}
