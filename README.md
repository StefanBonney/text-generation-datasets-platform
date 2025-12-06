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

Implemented features, submission 1 & 2:
- User registration and authentication
- Create and manage datasets (collections of text lines)
- Bulk add text lines (paste multiple lines at once)
- Advanced filtering: alphanumeric only, no special chars, length-based, random sampling
- Download full datasets or filtered subsets
- Search datasets by keyword
- View dataset statistics (line count, length distribution, etc.)

Implemented features, submission 3:
- **Tags/Classifications**: Users can categorize datasets with predefined tags (Package Names, Variable Names, API Endpoints, etc.)
  - Dataset owners can add/remove multiple tags per dataset
  - Tags can be selected during dataset creation
  - Tags are visible to all users
- **Comments**: Users can discuss datasets through comment threads
  - Any logged-in user can comment on any dataset
  - Comment authors can delete their own comments
  - Dataset owners can moderate (delete) all comments on their datasets
  - Comments display username and timestamp
  - Comments are visible to all users
- **Enhanced User Statistics**: User profile pages now show comprehensive statistics
  - Datasets created, lines contributed, average lines per dataset
  - Member since date
  - Last modified dataset with timestamp

#### Implemented Fixes

Implemented fixes, submission 3:
- Redirect users to login page after registration (previously went to home)
- Hide register/login links from logged-in users in navigation
- Add user profile link to navbar for easy access
- Move dataset creation to dedicated page with navbar link (better UX than bottom-of-page form)
- Fix dataset creation error for empty datasets
- Preserve line breaks in dataset descriptions
- Add description preview on home page dataset listings
- Slight improvements to visual design


#### Testing

After seeding the database, login with a test user:
- **Usernames:** `user1`, `user2`, or `user3`
- **Password:** `password123`

Test the application, submission 1 & 2:
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

Test the application, submission 3:
1. **Tags/Classifications:**
   - Login as `user1` and view a dataset you own
   - Add tags using the dropdown (e.g., "Package Names", "Function Names")
   - Remove tags using the × button
   - Create a new dataset and select tags via checkboxes
   - View another user's dataset - verify you can see tags but not modify them
   - Logout and verify tags are visible but no modification controls appear

2. **Comments:**
   - Login as `user1`
   - Post a comment on any dataset (yours or others')
   - Verify comment appears with your username and timestamp
   - Delete your own comment
   - On your own dataset, delete a comment from another user (moderation)
   - On someone else's dataset, verify you cannot delete their comments
   - Logout and verify comments are visible but posting is disabled

3. **User Statistics:**
   - Login as `user1`
   - Click "Profile" in navbar to view your user page
   - Verify statistics display: datasets created, lines contributed, average lines per dataset
   - Add lines to a dataset, refresh profile, verify statistics update

###  Setup Instructions

#### Requirements

- Python 3.x
- Flask
- SQLite3

#### Running the Application

1. Create and activate virtual environment:
```
python -m venv .venv
.venv/bin/activate  # On Unix: source .venv/bin/activate
```

2. Install dependencies:
```
pip install flask
```

3. Initialize the database:
```
# Delete old database if exists
# del database.db 
sqlite3 database/database.db < database/schema.sql
```

4. (Optional) Seed with test data:
```
python scripts/seed.py
```

5. Run the application:
```
python -m flask run
```
6. Open browser to `http://127.0.0.1:5000`