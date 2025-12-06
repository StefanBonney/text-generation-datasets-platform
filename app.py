"""
FILE: app.py
DESCRIPTION:
Flask application routes and request handlers.
Defines all HTTP endpoints for the Text Generation Datasets Platform,
including dataset management, user authentication, comments, and tags.
"""


import math
import secrets
import sqlite3
from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
import markupsafe
import config
from queries import datasets, users, comments

app = Flask(__name__)
app.secret_key = config.secret_key

@app.template_filter()
def show_lines(content):
    """
    Convert newlines to HTML line breaks for template display.
    """
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)


# ========================================================== [HELPER FUNCTIONS]

def require_login():
    """
    Abort with 403 if user is not logged in.
    """
    if "user_id" not in session:
        abort(403)

def check_csrf():
    """
    Validate CSRF token, abort with 403 if invalid.
    """
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


# ========================================================== [GENERAL ROUTES]

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    """
    Display paginated list of all datasets.
    """
    dataset_count = datasets.dataset_count()
    page_size = 10
    page_count = math.ceil(dataset_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    all_datasets = datasets.get_datasets(page, page_size)
    return render_template("index.html", page=page, page_count=page_count, datasets=all_datasets)

@app.route("/search")
def search():
    """
    Search datasets by keyword in title or description.
    """
    query = request.args.get("query")
    results = datasets.search(query) if query else []
    return render_template("search.html", query=query, results=results)

# ========================================================== [DATASET ROUTES]

@app.route("/new_dataset", methods=["GET", "POST"])
def new_dataset():
    """
    Handle dataset creation form display and submission.
    """
    require_login()

    if request.method == "GET":
        all_tags = datasets.get_all_tags()
        return render_template("datasets/new.html", all_tags=all_tags)

    if request.method == "POST":
        check_csrf()

        # create dataset with title, description, user_id
        title = request.form["title"]
        description = request.form.get("description", "")
        if not title or len(title) > 100 or len(description) > 5000:
            abort(403)
        user_id = session["user_id"]

        dataset_id = datasets.add_dataset(title, description, user_id)

        # add selected tags
        selected_tag_ids = request.form.getlist("tag_ids")
        for tag_id in selected_tag_ids:
            datasets.add_dataset_tag(dataset_id, tag_id)

        return redirect("/dataset/" + str(dataset_id))


@app.route("/dataset/<int:dataset_id>")
def show_dataset(dataset_id):
    """
    Display dataset details, statistics, tags, and comments.
    """
    dataset = datasets.get_dataset(dataset_id)
    if not dataset:
        abort(404)
    lines = datasets.get_lines(dataset_id)
    stats = datasets.get_dataset_stats(dataset_id)
    tags = datasets.get_dataset_tags(dataset_id)
    all_tags = datasets.get_all_tags()
    dataset_comments = comments.get_comments(dataset_id)

    return render_template("datasets/dataset.html",
                          dataset=dataset,
                          lines=lines,
                          stats=stats,
                          tags=tags,
                          all_tags=all_tags,
                          comments=dataset_comments)

@app.route("/edit_dataset/<int:dataset_id>", methods=["GET", "POST"])
def edit_dataset(dataset_id):
    """
    Handle dataset editing form display and submission.
    """
    require_login()

    dataset = datasets.get_dataset(dataset_id)
    if not dataset or dataset["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("datasets/edit.html", dataset=dataset)

    if request.method == "POST":
        check_csrf()
        title = request.form["title"]
        description = request.form["description"]
        if not title or len(title) > 100 or len(description) > 5000:
            abort(403)
        datasets.update_dataset(dataset_id, title, description)
        flash("Dataset updated")
        return redirect("/dataset/" + str(dataset_id))

@app.route("/delete_dataset/<int:dataset_id>", methods=["GET", "POST"])
def delete_dataset(dataset_id):
    """
    Handle dataset deletion confirmation and execution.
    """
    require_login()

    dataset = datasets.get_dataset(dataset_id)
    if not dataset or dataset["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("datasets/delete.html", dataset=dataset)

    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            datasets.delete_dataset(dataset_id)
            flash("Dataset deleted")
        return redirect("/")

@app.route("/add_lines", methods=["POST"])
def add_lines():
    """
    Process bulk addition of text lines to a dataset.
    """
    check_csrf()
    require_login()

    content = request.form["content"]
    dataset_id = request.form["dataset_id"]
    user_id = session["user_id"]

    dataset = datasets.get_dataset(dataset_id)
    if not dataset or dataset["user_id"] != user_id:
        abort(403)

    lines = content.strip().split("\n")
    added_count = 0
    for line in lines:
        line = line.strip()
        if line:
            datasets.add_line(line, user_id, dataset_id)
            added_count += 1

    flash(f"Added {added_count} lines to dataset")
    return redirect("/dataset/" + str(dataset_id))

@app.route("/subset/<int:dataset_id>")
def view_subset(dataset_id):
    """
    Display filtered subset of dataset based on query parameters.
    """
    dataset = datasets.get_dataset(dataset_id)
    if not dataset:
        abort(404)

    filters = {
        'alphanumeric_only': request.args.get('alphanumeric_only') == '1',
        'no_special_chars': request.args.get('no_special_chars') == '1',
        'length_filter': request.args.get('length_filter', ''),
        'random': request.args.get('random') == '1'
    }
    limit = request.args.get("limit", type=int, default=100)

    lines = datasets.get_lines_filtered(dataset_id, filters, limit)
    stats = datasets.get_dataset_stats(dataset_id)

    filter_desc = []
    if filters['alphanumeric_only']:
        filter_desc.append('alphanumeric only')
    if filters['no_special_chars']:
        filter_desc.append('no special chars')
    if filters['length_filter']:
        filter_desc.append(filters['length_filter'] + ' length')
    if filters['random']:
        filter_desc.append('random order')
    filter_description = ', '.join(filter_desc) if filter_desc else 'no filters'

    return render_template("datasets/subset.html", dataset=dataset, lines=lines,
                         filters=filters, limit=limit, stats=stats,
                         filter_description=filter_description)

@app.route("/download/<int:dataset_id>")
def download_dataset(dataset_id):
    """
    Generate and download dataset as text file with optional filters.
    """
    dataset = datasets.get_dataset(dataset_id)
    if not dataset:
        abort(404)

    filters = {
        'alphanumeric_only': request.args.get('alphanumeric_only') == '1',
        'no_special_chars': request.args.get('no_special_chars') == '1',
        'length_filter': request.args.get('length_filter', ''),
        'random': request.args.get('random') == '1'
    }
    limit = request.args.get("limit", type=int)

    lines = datasets.get_lines_filtered(dataset_id, filters, limit)
    text_content = "\n".join([line["content"] for line in lines])

    filename_parts = [dataset['title'].replace(' ', '_')]
    if filters['alphanumeric_only']:
        filename_parts.append('alphanumeric')
    if filters['no_special_chars']:
        filename_parts.append('clean')
    if filters['length_filter']:
        filename_parts.append(filters['length_filter'])
    if filters['random']:
        filename_parts.append('random')
    if limit:
        filename_parts.append(f"n{limit}")
    filename = "_".join(filename_parts) + ".txt"

    response = make_response(text_content)
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    # Triggers browser download of filtered dataset as .txt file
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response

# ========================================================== [TAG ROUTES]

@app.route("/dataset/<int:dataset_id>/add_tag", methods=["POST"])
def add_tag(dataset_id):
    """
    Add a tag to a dataset (owner only).
    """
    check_csrf()
    require_login()

    dataset = datasets.get_dataset(dataset_id)
    if not dataset or dataset["user_id"] != session["user_id"]:
        abort(403)  # Only owner can add tags

    tag_id = request.form["tag_id"]
    datasets.add_dataset_tag(dataset_id, tag_id)

    return redirect(f"/dataset/{dataset_id}")

@app.route("/dataset/<int:dataset_id>/remove_tag/<int:tag_id>", methods=["POST"])
def remove_tag(dataset_id, tag_id):
    """
    Remove a tag from a dataset (owner only).
    """
    check_csrf()
    require_login()

    dataset = datasets.get_dataset(dataset_id)
    if not dataset or dataset["user_id"] != session["user_id"]:
        abort(403)  # Only owner can remove tags

    datasets.remove_dataset_tag(dataset_id, tag_id)

    return redirect(f"/dataset/{dataset_id}")

# ========================================================== [COMMENT ROUTES]

@app.route("/dataset/<int:dataset_id>/comment", methods=["POST"])
def add_comment(dataset_id):
    """
    Process new comment submission on a dataset.
    """
    check_csrf()
    require_login()

    content = request.form["content"].strip()
    if not content:
        flash("Comment cannot be empty")
        return redirect(f"/dataset/{dataset_id}")

    if len(content) > 1000:
        flash("Comment too long (max 1000 characters)")
        return redirect(f"/dataset/{dataset_id}")

    comments.add_comment(content, session["user_id"], dataset_id)
    flash("Comment added")

    return redirect(f"/dataset/{dataset_id}")

@app.route("/comment/<int:comment_id>/delete", methods=["POST"])
def delete_comment(comment_id):
    """
    Delete a comment (author or dataset owner only).
    """
    check_csrf()
    require_login()

    comment = comments.get_comment(comment_id)

    if not comment:
        abort(404)

    # only comment author or dataset owner can delete
    dataset = datasets.get_dataset(comment["dataset_id"])
    if comment["user_id"] != session["user_id"] and dataset["user_id"] != session["user_id"]:
        abort(403)

    comments.delete_comment(comment_id)
    flash("Comment deleted")

    return redirect(f"/dataset/{comment['dataset_id']}")


# ========================================================== [USER ROUTES]

@app.route("/user/<int:user_id>")
def show_user(user_id):
    """
    Display user profile page with datasets and statistics.
    """
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_datasets = users.get_datasets(user_id)
    stats = users.get_user_statistics(user_id)
    return render_template("users/user.html", user=user, datasets=user_datasets, stats=stats)

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Handle user registration form display and submission.
    """
    if request.method == "GET":
        return render_template("users/register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        if not username or not username.strip():
            flash("ERROR: Username cannot be empty")
            return render_template("users/register.html", filled={})
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            flash("ERROR: Passwords do not match")
            filled = {"username": username}
            return render_template("users/register.html", filled=filled)

        try:
            users.create_user(username, password1)
            flash("Account created successfully, you can now log in")
            return redirect("/login")
        except sqlite3.IntegrityError:
            flash("ERROR: Username already taken")
            filled = {"username": username}
            return render_template("users/register.html", filled=filled)

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login form display and authentication.
    """
    if request.method == "GET":
        return render_template("users/login.html", next_page=request.referrer)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(next_page)

        flash("ERROR: Wrong username or password")
        return render_template("users/login.html", next_page=next_page)

@app.route("/logout")
def logout():
    """
    Log out current user by clearing session.
    """
    require_login()

    del session["user_id"]
    return redirect("/")

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    """
    Handle profile image upload form display and submission.
    """
    require_login()

    if request.method == "GET":
        return render_template("users/add_image.html")

    if request.method == "POST":
        check_csrf()

        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            flash("ERROR: File is not a jpg file")
            return redirect("/add_image")

        image = file.read()
        if len(image) > 100 * 1024:
            flash("ERROR: File is too large")
            return redirect("/add_image")

        user_id = session["user_id"]
        users.update_image(user_id, image)
        flash("Image added successfully")
        return redirect("/user/" + str(user_id))

@app.route("/image/<int:user_id>")
def show_image(user_id):
    """
    Serve user profile image.
    """
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response
