-- database/schema.sql

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE datasets (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE dataset_lines (
    id INTEGER PRIMARY KEY,
    content TEXT,
    added_at TEXT,
    user_id INTEGER REFERENCES users,
    dataset_id INTEGER REFERENCES datasets
);
CREATE INDEX idx_dataset_lines ON dataset_lines (dataset_id);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE dataset_tags (
    dataset_id INTEGER REFERENCES datasets ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags ON DELETE CASCADE,
    PRIMARY KEY (dataset_id, tag_id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    dataset_id INTEGER REFERENCES datasets ON DELETE CASCADE
);
CREATE INDEX idx_comments_dataset ON comments (dataset_id);