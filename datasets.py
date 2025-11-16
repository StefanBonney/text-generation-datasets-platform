# datasets.py

import db

def dataset_count():
    sql = "SELECT COUNT(*) FROM datasets"
    return db.query(sql)[0][0]

def get_datasets(page, page_size):
    sql = """SELECT d.id, d.title, d.description, d.user_id, u.username, 
                    COUNT(l.id) total, MAX(l.added_at) last
             FROM datasets d
             LEFT JOIN dataset_lines l ON d.id = l.dataset_id
             LEFT JOIN users u ON d.user_id = u.id
             GROUP BY d.id
             ORDER BY d.id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_dataset(dataset_id):
    sql = """SELECT d.id, d.title, d.description, d.user_id, d.created_at, u.username
             FROM datasets d, users u
             WHERE d.id = ? AND d.user_id = u.id"""
    result = db.query(sql, [dataset_id])
    return result[0] if result else None

def get_lines(dataset_id):
    sql = """SELECT l.id, l.content, l.added_at, l.user_id, u.username
             FROM dataset_lines l, users u
             WHERE l.user_id = u.id AND l.dataset_id = ?
             ORDER BY l.id"""
    return db.query(sql, [dataset_id])

def get_line(line_id):
    sql = "SELECT id, content, user_id, dataset_id FROM dataset_lines WHERE id = ?"
    result = db.query(sql, [line_id])
    return result[0] if result else None

def add_dataset(title, description, user_id):
    sql = "INSERT INTO datasets (title, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, description, user_id])
    return db.last_insert_id()

def add_line(content, user_id, dataset_id):
    sql = """INSERT INTO dataset_lines (content, added_at, user_id, dataset_id) VALUES
             (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, dataset_id])

def update_dataset(dataset_id, title, description):
    sql = "UPDATE datasets SET title = ?, description = ? WHERE id = ?"
    db.execute(sql, [title, description, dataset_id])

def delete_dataset(dataset_id):
    sql = "DELETE FROM dataset_lines WHERE dataset_id = ?"
    db.execute(sql, [dataset_id])
    sql = "DELETE FROM datasets WHERE id = ?"
    db.execute(sql, [dataset_id])

def get_lines_filtered(dataset_id, filters, limit=None):
    """
    Get filtered subset of dataset lines
    filters is a dict like: {
        'alphanumeric_only': True,
        'no_special_chars': False,
        'length_filter': 'short',
        'random': True
    }
    """
    
    base_sql = """SELECT l.id, l.content, l.added_at, l.user_id, u.username
                  FROM dataset_lines l, users u
                  WHERE l.user_id = u.id AND l.dataset_id = ?"""
    
    if filters.get('alphanumeric_only'):
        base_sql += " AND l.content NOT GLOB '*[^a-zA-Z0-9 ]*'"
    
    if filters.get('no_special_chars'):
        base_sql += " AND l.content NOT GLOB '*[^a-zA-Z0-9_-]*'"
    
    length_filter = filters.get('length_filter')
    if length_filter == "short":
        base_sql += " AND LENGTH(l.content) < 20"
    elif length_filter == "medium":
        base_sql += " AND LENGTH(l.content) BETWEEN 20 AND 50"
    elif length_filter == "long":
        base_sql += " AND LENGTH(l.content) > 50"
    
    if filters.get('random'):
        base_sql += " ORDER BY RANDOM()"
    else:
        base_sql += " ORDER BY l.id"
    
    if limit:
        base_sql += f" LIMIT {limit}"
    
    return db.query(base_sql, [dataset_id])

def get_dataset_stats(dataset_id):
    """Get statistics about the dataset"""
    sql = """SELECT 
                COUNT(*) as total_lines,
                AVG(LENGTH(content)) as avg_length,
                MIN(LENGTH(content)) as min_length,
                MAX(LENGTH(content)) as max_length,
                SUM(CASE WHEN content NOT GLOB '*[^a-zA-Z0-9 ]*' THEN 1 ELSE 0 END) as alphanumeric_count,
                SUM(CASE WHEN LENGTH(content) < 20 THEN 1 ELSE 0 END) as short_count,
                SUM(CASE WHEN LENGTH(content) BETWEEN 20 AND 50 THEN 1 ELSE 0 END) as medium_count,
                SUM(CASE WHEN LENGTH(content) > 50 THEN 1 ELSE 0 END) as long_count
             FROM dataset_lines
             WHERE dataset_id = ?"""
    result = db.query(sql, [dataset_id])
    return result[0] if result else None

def search(query):
    sql = """SELECT d.id dataset_id,
                    d.title,
                    d.description,
                    u.username,
                    d.created_at
             FROM datasets d, users u
             WHERE d.user_id = u.id AND
                   (d.title LIKE ? OR d.description LIKE ?)
             ORDER BY d.created_at DESC"""
    search_term = "%" + query + "%"
    return db.query(sql, [search_term, search_term])
