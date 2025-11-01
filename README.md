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