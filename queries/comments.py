"""
FILE: queries/comments.py
DESCRIPTION:
Database queries for comment management.
Handles comment creation, retrieval, and deletion for dataset discussions.
"""

from database import db

def add_comment(content, user_id, dataset_id):
    """
    Add a new comment to a dataset
    """
    sql = """INSERT INTO comments (content, user_id, dataset_id)
             VALUES (?, ?, ?)"""
    db.execute(sql, [content, user_id, dataset_id])

def get_comments(dataset_id):
    """
    Get all comments for a specific dataset, ordered newest first
    """
    sql = """SELECT c.id, c.content, c.created_at, c.user_id, u.username
             FROM comments c
             JOIN users u ON c.user_id = u.id
             WHERE c.dataset_id = ?
             ORDER BY c.created_at DESC"""
    return db.query(sql, [dataset_id])

def delete_comment(comment_id):
    """
    Delete a comment by ID
    """
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def get_comment(comment_id):
    """
    Get a single comment by ID (used for permission checks)
    """
    sql = """SELECT c.id, c.content, c.user_id, c.dataset_id
             FROM comments c
             WHERE c.id = ?"""
    result = db.query(sql, [comment_id])
    return result[0] if result else None

def get_user_comment_count(user_id):
    """
    Get total number of comments posted by a user
    """
    sql = "SELECT COUNT(*) FROM comments WHERE user_id = ?"
    return db.query(sql, [user_id])[0][0]
