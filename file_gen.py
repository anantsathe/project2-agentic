import duckdb
import json
import datetime
import random

# Define the output DuckDB file
db_file = "social_media.duckdb"

# Connect to DuckDB
conn = duckdb.connect(db_file)

# Drop table if it exists (to avoid conflicts on reruns)
conn.execute("DROP TABLE IF EXISTS social_media")

# Create the social_media table
conn.execute("""
CREATE TABLE social_media (
    post_id INTEGER PRIMARY KEY,
    username VARCHAR,
    timestamp TIMESTAMP,
    comments VARCHAR  -- JSON stored as string
)
""")

# Sample user data
usernames = ["alice", "bob", "charlie", "dave", "eve", "frank", "grace", "heidi"]

# Sample comment texts
comment_texts = [
    "Great post!", "Interesting read!", "I disagree.", "Well explained!",
    "Could use more details.", "Awesome work!", "Thanks for sharing!"
]

# Function to generate random comments (ensuring some have useful >= 5)
def generate_comments():
    num_comments = random.randint(1, 5)  # Each post can have 1-5 comments
    comments = []
    
    for _ in range(num_comments):
        useful_stars = random.randint(0, 10)

        # Ensure at least some comments have useful stars >= 5
        if random.random() < 0.3:  # 30% chance of making it >= 5
            useful_stars = random.randint(5, 10)

        comment = {
            "commenter": random.choice(usernames),
            "text": random.choice(comment_texts),
            "stars": {
                "funny": random.randint(0, 5),
                "useful": useful_stars
            }
        }
        comments.append(comment)
    
    return json.dumps(comments)  # Store JSON as a string

# Generate 100 posts with varying timestamps
posts = [
    (
        i, 
        random.choice(usernames), 
        datetime.datetime(2024, random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59)), 
        generate_comments()
    )
    for i in range(1, 101)
]

# Insert data into the table
conn.executemany("INSERT INTO social_media VALUES (?, ?, ?, ?)", posts)

# Close the connection
conn.close()

print(f"DuckDB database created successfully: {db_file}")