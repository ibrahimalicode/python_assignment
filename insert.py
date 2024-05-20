import sqlite3
import random

# Connect to the database
conn = sqlite3.connect("db/db.db")
cur = conn.cursor()

# Lorem Ipsum paragraphs with 60-80 words each
lorem_paragraphs = []


# SQL query to insert data
insert_query = "INSERT INTO answers (text, UID) VALUES (?, ?)"

# Insert each paragraph with a random UID
for paragraph in lorem_paragraphs:
    uid = random.randint(1, 5)
    cur.execute(insert_query, (paragraph, uid))

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
