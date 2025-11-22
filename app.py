# app.py

import math, secrets, sqlite3
from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
import markupsafe
import config
from queries import datasets, users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)


# ========================================================== [HELPER FUNCTIONS]

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


# ========================================================== [GENERAL ROUTES]

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
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
    query = request.args.get("query")
    results = datasets.search(query) if query else []
    return render_template("search.html", query=query, results=results)

# ========================================================== [DATASET ROUTES]

@app.route("/new_dataset", methods=["GET", "POST"])
def new_dataset():
    require_login()
    
    if request.method == "GET":
        return render_template("datasets/new.html")
    
    if request.method == "POST":
        check_csrf()

        title = request.form["title"]
        description = request.form.get("description", "")
        if not title or len(title) > 100 or len(description) > 5000:
            abort(403)
        user_id = session["user_id"]

        dataset_id = datasets.add_dataset(title, description, user_id)
        return redirect("/dataset/" + str(dataset_id))

@app.route("/dataset/<int:dataset_id>")
def show_dataset(dataset_id):
    dataset = datasets.get_dataset(dataset_id)
    if not dataset:
        abort(404)
    lines = datasets.get_lines(dataset_id)
    stats = datasets.get_dataset_stats(dataset_id)
    return render_template("datasets/dataset.html", dataset=dataset, lines=lines, stats=stats)

@app.route("/edit_dataset/<int:dataset_id>", methods=["GET", "POST"])
def edit_dataset(dataset_id):
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
    response.headers["Content-Disposition"] = f"attachment; filename={filename}" # Triggers browser download of filtered dataset as .txt file
    return response


# ========================================================== [USER ROUTES]


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_datasets = users.get_datasets(user_id)
    return render_template("users/user.html", user=user, datasets=user_datasets)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("users/register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        if not username or len(username) > 16:
            abort(403)
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
            return render_template("register.html", filled=filled)

@app.route("/login", methods=["GET", "POST"])
def login():
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
        else:
            flash("ERROR: Wrong username or password")
            return render_template("users/login.html", next_page=next_page)

@app.route("/logout")
def logout():
    require_login()

    del session["user_id"]
    return redirect("/")

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
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
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response










