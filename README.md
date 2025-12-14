# Text Generation Datasets Platform


The Text Generation Datasets Platform is designed for users to **share and modify single-column text datasets** (e.g. repository, product or variable names) for text generation purposes. The platform aims to be a **"mini-Kaggle"** specifically for text lines / words, allowing datasets to be forked, rated, commented on, and previewed with generators.

Course Project created for course: Tietokannat ja web-ohjelmointi  
**https://hy-tikawe.github.io/materiaali/**


##  Setup Instructions

This section details how the project can be set up and run.

#### Requirements

- Python 3.x
- Flask
- SQLite3

#### Running the Application

1. Create and activate virtual environment:
```
python -m venv .venv
.venv\Scripts\activate  # On Unix: source .venv/bin/activate
```

2. Install dependencies:
```
pip install flask
```

3. Initialize the database:
```
# Delete old database if exists
# del ".\database\database.db"

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


## Planned Functionality

This section outlines the core functionality set out to be built at the start of the course.

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


## Implemented Features

This section outlines the features that have been added to the project from the development done during the course.

Note: Not all features from the initial project plan have been implemented, with the development instead focusing on meeting the minimum requirements for the course grade. Features not implemented include: dataset forking, rating system (1-5 stars), project links (URLs to projects using datasets), and individual line deletion.

#### User Management
- User registration and authentication with secure password hashing
- User profile pages displaying:
  - Statistics (datasets created, lines contributed, average lines per dataset)
  - Member since date and last activity
  - List of user's datasets with details

#### Dataset Management
- Create, edit, and delete datasets (owners only)
- View all datasets with pagination
- Bulk add text lines (paste multiple lines at once via textarea)
- Dataset preview showing first 20 lines
- Detailed dataset statistics (line count, average/min/max length, character distribution)

#### Search and Discovery
- Search datasets by keyword (searches titles and descriptions)
- Filter and download subsets with advanced criteria:
  - Alphanumeric only or no special characters
  - Length-based filtering (short/medium/long)
  - Random order with configurable line limits
- Download full datasets or filtered subsets as text files

#### Tags and Classification
- Predefined tag system for categorizing datasets (Package Names, Variable Names, API Endpoints, etc.)
- Dataset owners can add/remove multiple tags per dataset
- Tags selectable during dataset creation
- Tags visible to all users

#### Community Interaction
- Comment threads on datasets
- Any logged-in user can comment on any dataset
- Comment authors can delete their own comments
- Dataset owners can moderate (delete) all comments on their datasets
- Comments display author username and timestamp


## Testing

This section outlines how the features added to the project can be tested. 

After seeding the database, login is created for test users:
- **Usernames:** `user1`, `user2`, or `user3`
- **Password:** `password123`

#### User Management
1. Register a new account via `/register`
2. Login with your credentials
3. Create a dataset first (statistics only display after creating at least one dataset)
4. Click "Profile" in navbar to view your user page
5. Verify statistics display: datasets created, lines contributed, average lines per dataset, member since date
6. Add lines to a dataset, refresh profile, verify statistics update (last modified info also appears)
7. View another user's profile by clicking their username on any dataset (from homepage)

#### Dataset Management
1. Login (e.g., `user1` / `password123`)
2. Browse the home page to see all datasets
3. Click on a dataset you created (look for your username) to view it
4. View dataset statistics (line counts, average/min/max length, character distribution)
5. View the preview showing first 20 lines
6. Add more text lines using the bulk paste feature
7. Edit your dataset's title and description (Edit description button)
8. Delete your own dataset
9. Try to edit/delete another user's dataset (should be restricted)

#### Search and Discovery
1. Use the search bar to find datasets by keyword (searches titles and descriptions)
	- type e.g. test
2. Navigate to a dataset page and create a filtered subset:
   - Select character filters (alphanumeric only, no special chars)
   - Choose length filter (short/medium/long)
   - Enable random ordering if desired
   - Set number of lines to include
3. Download full datasets or filtered subsets as .txt files
4. Test different "Quick download" options: First 100, First 1000, Random 500, Clean lines only 

#### Tags and Classification
1. Login (e.g., `user1` / `password123`)
2. Navigate to a dataset created by user
2. Add tags using the dropdown (e.g., "Package Names", "Function Names")
3. Remove tags using the × button
4. Create a new dataset and select tags during creation
5. View another user's dataset - verify you can see tags but not modify them
6. Logout and verify tags are visible but no modification controls appear

#### Community Interaction
1. Login (e.g., `user1` / `password123`)
2. Post a comment on any dataset (yours or others')
3. Verify comment appears with your username and timestamp
4. Delete your own comment
5. On your own dataset, delete a comment from another user (moderation)
6. On someone else's dataset, verify you cannot delete their comments
7. Logout and verify comments are visible but posting is disabled


## Documentation

Additional project documentation is available in the `documentation/` directory:
- **Course Checklist** (`documentation/checklist.md`): Requirements verification for course grading
- **Pylint Report** (`documentation/pylint-report.md`): Code quality analysis
- **Performance Report** (`documentation/performance-report.md`): Large dataset performance testing