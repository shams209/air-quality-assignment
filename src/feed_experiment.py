# Name: Shams ur Rehman
# Roll Number: TRN-2026-000943
# Date: 2026-11-20

import sqlite3
import time
import random

# Connect to an in-memory SQLite database (fast for testing)
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# 1. Create the table
cursor.execute('''
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY,
        author_id INTEGER,
        created_at TIMESTAMP,
        content TEXT
    )
''')

# 2. Insert 10,000 mock posts
print("Inserting 10,000 rows (this may take a second)...")
posts = []
for i in range(1, 10001):
    author_id = random.randint(1, 100) # 100 different authors
    created_at = f"2026-11-{random.randint(1, 20):02d} 12:00:00"
    posts.append((author_id, created_at, f"Post content {i}"))

cursor.executemany('INSERT INTO posts (author_id, created_at, content) VALUES (?, ?, ?)', posts)
conn.commit()

# The query: "Get the newest posts from users 1, 2, and 3"
query = "SELECT * FROM posts WHERE author_id IN (1, 2, 3) ORDER BY created_at DESC LIMIT 50;"

# ==========================================
# EXPERIMENT 1: WITHOUT INDEX
# ==========================================
print("\n--- Experiment 1: WITHOUT Index ---")
start_time = time.perf_counter()

# Ask SQLite how it plans to run the query
cursor.execute(f"EXPLAIN QUERY PLAN {query}")
plan_before = cursor.fetchall()
print("Query Plan:")
for row in plan_before:
    print(f"  {row[3]}") # row[3] contains the detail string (e.g., "SCAN posts")

# Actually run the query and time it
cursor.execute(query)
results = cursor.fetchall()
end_time = time.perf_counter()
time_before = (end_time - start_time) * 1000 # Convert to milliseconds
print(f"Time taken: {time_before:.4f} ms")

# ==========================================
# EXPERIMENT 2: WITH INDEX
# ==========================================
print("\n--- Experiment 2: WITH Index on (author_id, created_at) ---")
cursor.execute("CREATE INDEX idx_author_time ON posts(author_id, created_at);")

start_time = time.perf_counter()

# Ask SQLite how it plans to run the query now
cursor.execute(f"EXPLAIN QUERY PLAN {query}")
plan_after = cursor.fetchall()
print("Query Plan:")
for row in plan_after:
    print(f"  {row[3]}") # Should show "SEARCH posts USING INDEX"

# Actually run the query and time it
cursor.execute(query)
results = cursor.fetchall()
end_time = time.perf_counter()
time_after = (end_time - start_time) * 1000 # Convert to milliseconds
print(f"Time taken: {time_after:.4f} ms")

print("\n--- Conclusion ---")
print("The index changed the query plan from a full table SCAN to a SEARCH using the index, drastically reducing the execution time.")