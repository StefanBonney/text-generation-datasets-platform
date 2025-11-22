# Text Generation Datasets Platform


The Text Generation Datasets Platform is designed for users to **share and modify single-column text datasets** (e.g. repository, product or variable names) for text generation purposes. The platform aims to be a **"mini-Kaggle"** specifically for text lines / words, allowing datasets to be forked, rated, commented on, and previewed with generators.

### Core Functionality

**User Management**
- Users can **create an account and log in**.
- **User pages** display relevant statistics (e.g., number of datasets and lines, average rating) and a list of the user's datasets.

**Dataset Management**
- Users can **view all datasets** added to the application and **their contents**.
- Users can **search for datasets** using keywords and **filter** them by tags.
- Users can **add, edit, and delete** datasets.
- Users can **add text lines** to datasets (via bulk paste into a text area) and **delete** lines.
- Users can **download** created datasets.

**Community & Interaction**
- Users can assign **one or more tags** to a dataset (categories/classifications).
- Users can **fork an existing dataset** to create a variation (e.g., "10,000 PyPI packages" → "5,000 popular packages").
- Users can give datasets a **rating (1-5 stars)** and see the average rating and vote count.
- Users can **discuss datasets in comment threads**.
- Users can add **links to projects** that use the dataset (URL + title).

In this application, the primary data object is a dataset, and the secondary data objects are comments and project links that complement the dataset.

### Development Progress and Testing Guidance

#### Implemented Features

- User registration and authentication
- Create and manage datasets (collections of text lines)
- Bulk add text lines (paste multiple lines at once)
- Advanced filtering: alphanumeric only, no special chars, length-based, random sampling
- Download full datasets or filtered subsets
- Search datasets by keyword
- View dataset statistics (line count, length distribution, etc.)

#### Testing

After seeding the database, login with a test user:
- **Usernames:** `user1`, `user2`, or `user3`
- **Password:** `password123`

Test the application:
1. Login (e.g., `user1` / `password123`)
2. Browse the home page to see all datasets
3. Click on a dataset you created (look for your username) to view/edit it
4. Add more text lines using the bulk paste feature
5. View dataset statistics (line counts, length distribution)
6. Create filtered subsets using the subset form
7. Download full or filtered datasets as .txt files
8. Edit or delete your own datasets
9. Search for datasets by keyword
10. View other users' datasets (you can view but not edit)

Or create your own account via `/register`.

###  Setup Instructions

#### Requirements

- Python 3.x
- Flask
- SQLite3

#### Running the Application

1. Install dependencies:
```
pip install flask
```

2. Initialize the database:
```
# Delete old database if exists
# del database.db 
sqlite3 database/database.db < database/schema.sql
```

3. (Optional) Seed with test data:
```
python scripts/seed.py
```

4. Run the application:
```
flask run
```
5. Open browser to `http://127.0.0.1:5000`