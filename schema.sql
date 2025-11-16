-- schema.sql

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
