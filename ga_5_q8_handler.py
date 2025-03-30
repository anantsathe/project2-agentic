import json
import re

async def process_filtered_sorted_posts(question: str):
    """
    Extracts dynamic parameters from the question and returns a DuckDB SQL query.
    """
    
    # Regular expressions to extract parameters
    timestamp_match = re.search(r"after (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)", question)
    min_timestamp = timestamp_match.group(1) if timestamp_match else "2024-12-16T23:06:53.838Z"

    comments_match = re.search(r"at least (\d+) comment", question)
    min_comments = int(comments_match.group(1)) if comments_match else 1

    stars_match = re.search(r"(\d+) useful stars", question)
    min_stars = int(stars_match.group(1)) if stars_match else 5

    column_match = re.search(r"column called (\w+)", question)
    column_name = column_match.group(1) if column_match else "post_id"

    sort_match = re.search(r"sorted in (\w+) order", question)
    sort_order = "ASC" if sort_match and sort_match.group(1).lower() == "ascending" else "DESC"

    # Generate SQL query dynamically
    query = f"""
    SELECT {column_name}
    FROM (
        SELECT post_id
        FROM (
            SELECT post_id,
                   json_extract(comments, '$[*].stars.useful') AS useful_stars
            FROM social_media
            WHERE timestamp >= '{min_timestamp}'
        )
        WHERE EXISTS (
            SELECT 1 FROM UNNEST(useful_stars) AS t(value)
            WHERE CAST(value AS INTEGER) >= {min_stars}
        )
    )
    ORDER BY {column_name} {sort_order};
    """

    return {"query": query}
