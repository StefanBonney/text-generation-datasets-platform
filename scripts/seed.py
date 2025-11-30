# scripts/seed.py

import random
import sqlite3
from werkzeug.security import generate_password_hash

db = sqlite3.connect("database/database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM datasets")
db.execute("DELETE FROM dataset_lines")
db.execute("DELETE FROM tags")          
db.execute("DELETE FROM dataset_tags")  

user_count = 3
dataset_count = 20
line_count = 2000

short_words = ["pip", "npm", "git", "api", "db", "io", "ai", "ml", "ui", "js"]
medium_words = ["numpy", "pandas", "flask", "django", "tensorflow", "pytorch", "requests"]
long_words = ["scikit-learn", "beautifulsoup4", "matplotlib", "sqlalchemy", "anthropic-sdk"]
special_chars = ["!", "@", "#", "$", "%", "&", "*", "()", "[]", "{}", "<>"]

for i in range(1, user_count + 1):
    password_hash = generate_password_hash("password123")
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               ["user" + str(i), password_hash])

for i in range(1, dataset_count + 1):
    user_id = random.randint(1, user_count)
    db.execute("INSERT INTO datasets (title, description, user_id) VALUES (?, ?, ?)",
               ["Dataset " + str(i), "Test dataset number " + str(i), user_id])

for i in range(1, line_count + 1):
    user_id = random.randint(1, user_count)
    dataset_id = random.randint(1, dataset_count)
    
    content_type = random.randint(1, 10)
    
    if content_type <= 3:
        content = random.choice(short_words)
    elif content_type <= 5:
        content = random.choice(medium_words)
    elif content_type <= 7:
        content = random.choice(long_words)
    elif content_type == 8:
        content = random.choice(short_words) + random.choice(special_chars)
    elif content_type == 9:
        content = random.choice(medium_words) + random.choice(special_chars) + str(random.randint(1, 100))
    else:
        content = f"variable_name_{random.randint(1, 1000)}_with_underscores"
    
    db.execute("""INSERT INTO dataset_lines (content, added_at, user_id, dataset_id)
                  VALUES (?, datetime('now'), ?, ?)""",
               [content, user_id, dataset_id])

tags = [
    "Package Names",
    "Variable Names", 
    "API Endpoints",
    "Function Names",
    "Product Names",
    "Repository Names"
]

for tag in tags:
    db.execute("INSERT INTO tags (name) VALUES (?)", [tag])

# Randomly assign tags to datasets
for dataset_id in range(1, dataset_count + 1):
    # Each dataset gets 1-3 random tags
    num_tags = random.randint(1, 3)
    selected_tags = random.sample(range(1, len(tags) + 1), num_tags)
    for tag_id in selected_tags:
        db.execute("INSERT INTO dataset_tags (dataset_id, tag_id) VALUES (?, ?)",
                   [dataset_id, tag_id])



db.commit()
db.close()

print(f"Created {user_count} users, {dataset_count} datasets, and {line_count} lines")
print("Data includes varied lengths and character types for filter testing")
print(f"Created {len(tags)} tags and assigned them randomly to datasets")

print(f"\nTest users: user1, user2, user3")
print("Password for all users: password123")