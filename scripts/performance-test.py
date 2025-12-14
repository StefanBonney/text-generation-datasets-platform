# scripts/performance-test.py
"""
Performance testing script.
1. Seeds database with large dataset (with timing)
2. Tests endpoint response times
"""

import random
import sqlite3
import time
import requests
from werkzeug.security import generate_password_hash

BASE_URL = "http://127.0.0.1:5000"

def seed_database():
    """Seed database with large dataset for performance testing"""
    print("\n" + "=" * 60)
    print("DATABASE SEEDING FOR PERFORMANCE TESTING")
    print("=" * 60)
    print("WARNING: This will delete existing data!")
    print("This creates 100 users, 500 datasets, and 50,000 lines.")
    response = input("Continue? (yes/no): ")
    
    if response.lower() != "yes":
        print("Aborted.")
        return False
    
    start_time = time.time()
    db = sqlite3.connect("database/database.db")
    
    print("\nDeleting existing data...")
    db.execute("DELETE FROM users")
    db.execute("DELETE FROM datasets")
    db.execute("DELETE FROM dataset_lines")
    db.execute("DELETE FROM tags")
    db.execute("DELETE FROM dataset_tags")
    
    # Configuration
    user_count = 100
    dataset_count = 500
    line_count = 50000
    
    # Create users
    print(f"\nCreating {user_count} users...")
    user_start = time.time()
    for i in range(1, user_count + 1):
        password_hash = generate_password_hash("password123")
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                   [f"perfuser{i}", password_hash])
        if i % 50 == 0:
            print(f"  Created {i} users...")
    user_time = time.time() - user_start
    
    # Create datasets
    print(f"\nCreating {dataset_count} datasets...")
    dataset_start = time.time()
    for i in range(1, dataset_count + 1):
        user_id = random.randint(1, user_count)
        db.execute("INSERT INTO datasets (title, description, user_id) VALUES (?, ?, ?)",
                   [f"Performance Dataset {i}", f"Large test dataset number {i}", user_id])
        if i % 100 == 0:
            print(f"  Created {i} datasets...")
    dataset_time = time.time() - dataset_start
    
    # Create lines
    print(f"\nCreating {line_count} lines...")
    short_words = ["pip", "npm", "git", "api", "db", "io", "ai", "ml", "ui", "js"]
    medium_words = ["numpy", "pandas", "flask", "django", "tensorflow", "pytorch", "requests"]
    long_words = ["scikit-learn", "beautifulsoup4", "matplotlib", "sqlalchemy", "anthropic-sdk"]
    special_chars = ["!", "@", "#", "$", "%", "&", "*", "()", "[]", "{}", "<>"]
    
    line_start = time.time()
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
        
        if i % 10000 == 0:
            print(f"  Created {i} lines...")
    line_time = time.time() - line_start
    
    # Create tags
    print("\nCreating tags...")
    tag_start = time.time()
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
    
    print("Assigning tags to datasets...")
    for dataset_id in range(1, dataset_count + 1):
        num_tags = random.randint(1, 3)
        selected_tags = random.sample(range(1, len(tags) + 1), num_tags)
        for tag_id in selected_tags:
            db.execute("INSERT INTO dataset_tags (dataset_id, tag_id) VALUES (?, ?)",
                       [dataset_id, tag_id])
        if dataset_id % 100 == 0:
            print(f"  Processed {dataset_id} datasets...")
    tag_time = time.time() - tag_start
    
    db.commit()
    db.close()
    
    total_time = time.time() - start_time
    
    # Print results
    print("\n" + "=" * 60)
    print("DATABASE SEEDING COMPLETE")
    print("=" * 60)
    print(f"Users: {user_count} (created in {user_time:.2f}s)")
    print(f"Datasets: {dataset_count} (created in {dataset_time:.2f}s)")
    print(f"Lines: {line_count} (created in {line_time:.2f}s)")
    print(f"  Average: {line_count/line_time:.0f} lines/second")
    print(f"Tags: {len(tags)} + assignments (created in {tag_time:.2f}s)")
    print(f"\nTotal seeding time: {total_time:.2f} seconds")
    print("=" * 60)
    
    return True

def measure_request(url, description):
    """Measure response time for a GET request"""
    start = time.time()
    response = requests.get(url, timeout=10)
    end = time.time()
    elapsed = (end - start) * 1000  # Convert to milliseconds
    
    print(f"{description}: {elapsed:.0f}ms (Status: {response.status_code})")
    return elapsed

def test_endpoints():
    """Test endpoint response times"""
    print("\n" + "=" * 60)
    print("ENDPOINT PERFORMANCE TESTING")
    print("=" * 60)
    print()
    
    results = {}
    
    # Test homepage
    print("Testing Homepage...")
    results['homepage'] = measure_request(f"{BASE_URL}/", "Homepage (page 1)")
    results['homepage_p5'] = measure_request(f"{BASE_URL}/5", "Homepage (page 5)")
    print()
    
    # Test search
    print("Testing Search...")
    results['search'] = measure_request(f"{BASE_URL}/search?query=test", "Search for 'test'")
    results['search_empty'] = measure_request(f"{BASE_URL}/search?query=xyz123", "Search (no results)")
    print()
    
    # Test dataset pages
    print("Testing Dataset Pages...")
    results['dataset_1'] = measure_request(f"{BASE_URL}/dataset/1", "Dataset #1")
    results['dataset_10'] = measure_request(f"{BASE_URL}/dataset/10", "Dataset #10")
    print()
    
    # Test user pages
    print("Testing User Pages...")
    results['user_1'] = measure_request(f"{BASE_URL}/user/1", "User #1 profile")
    print()
    
    print("=" * 60)
    print("ENDPOINT TESTING SUMMARY")
    print("=" * 60)
    avg_time = sum(results.values()) / len(results)
    print(f"Average response time: {avg_time:.0f}ms")
    print(f"Slowest endpoint: {max(results, key=results.get)} ({results[max(results, key=results.get)]:.0f}ms)")
    print(f"Fastest endpoint: {min(results, key=results.get)} ({results[min(results, key=results.get)]:.0f}ms)")

if __name__ == "__main__":
    print("=" * 60)
    print("PERFORMANCE TESTING")
    print("=" * 60)
    print("\nThis script will:")
    print("1. Seed database with 100 users, 500 datasets, 50,000 lines")
    print("2. Test endpoint response times")
    print("\n*** IMPORTANT: Make sure Flask app is STOPPED before starting ***")
    
    input("\nPress Enter to start database seeding...")
    
    # Step 1: Seed database (Flask must be stopped)
    if seed_database():
        print("\n" + "=" * 60)
        print("DATABASE SEEDING COMPLETE")
        print("=" * 60)
        print("\n*** NOW START THE FLASK APP ***")
        print("Run 'python -m flask run' in another terminal")
        input("\nPress Enter once Flask is running...")
        
        # Step 2: Test endpoints (Flask must be running)
        try:
            test_endpoints()
        except requests.exceptions.ConnectionError:
            print("\nError: Could not connect to Flask app. Make sure it's running!")
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)
    print("\nTo restore normal test data, run: python scripts/seed.py")