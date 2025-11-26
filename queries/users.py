# queries/users.py

from werkzeug.security import check_password_hash, generate_password_hash
from database import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if len(result) == 1:
        user_id, password_hash = result[0]
        if check_password_hash(password_hash, password):
            return user_id

    return None

def get_user(user_id):
    sql = """SELECT id, username, image IS NOT NULL has_image
             FROM users
             WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_datasets(user_id):
    sql = """SELECT d.id,
                    d.title,
                    d.created_at
             FROM datasets d
             WHERE d.user_id = ?
             ORDER BY d.created_at DESC"""
    return db.query(sql, [user_id])

def update_image(user_id, image):
    sql = "UPDATE users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])

def get_image(user_id):
    sql = "SELECT image FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None

def get_user_statistics(user_id):
    """
    Get statistics for user page
    """
    sql = """SELECT 
                COUNT(DISTINCT d.id) as dataset_count,
                COUNT(DISTINCT dl.id) as line_count,
                CAST(COUNT(DISTINCT dl.id) AS FLOAT) / NULLIF(COUNT(DISTINCT d.id), 0) as avg_lines_per_dataset,
                MIN(d.created_at) as first_dataset_date,
                MAX(dl.added_at) as last_activity_date,
                (SELECT d2.title 
                 FROM dataset_lines dl2
                 JOIN datasets d2 ON dl2.dataset_id = d2.id
                 WHERE dl2.user_id = ?
                 ORDER BY dl2.added_at DESC
                 LIMIT 1) as last_modified_dataset_title
             FROM users u
             LEFT JOIN datasets d ON u.id = d.user_id
             LEFT JOIN dataset_lines dl ON u.id = dl.user_id
             WHERE u.id = ?"""
    result = db.query(sql, [user_id, user_id])
    return result[0] if result else None
