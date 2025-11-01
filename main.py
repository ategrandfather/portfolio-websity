from flask import Flask, render_template, url_for, redirect, flash, request, Response
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import ProjectPost, About, Status, db, Admin
from datetime import datetime
from forms import ProjectForm, AboutForm, StatusForm
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required,
)


# activate config, db, ckeditor
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# flask login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# load proper year for html footer
current_year = datetime.now().year


def initialize_default_values_db():
    """Adding default values in db.Models About and Status"""
    # Apparently it appears that even establishing default values in models.py doesn't actually fill DB with them,
    # but only creates table scheme, don't understand it intuitively yet, but this should prevent things
    # from going wrong and somebody from spending two days figuring this out (it was paintful)

    about = db.session.get(About, "main")
    if not about:
        about = About(id="main", content="Some default about")
        db.session.add(about)

    status = db.session.get(Status, "main")
    if not status:
        status = Status(id="main", message="Some default status")
        db.session.add(status)

    db.session.commit()


@app.route("/")
def index():
    projects = ProjectPost.query.all()
    about = About.query.get("main")
    status = Status.query.get("main")

    return render_template(
        "index.html",
        projects=projects,
        status=status,
        year=current_year,
        about=about,
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    form = ProjectForm()
    if form.validate_on_submit():
        new_project = ProjectPost(
            title=form.title.data,
            description=form.description.data,
            link=form.link.data,
        )
        db.session.add(new_project)
        db.session.commit()
        flash("Project added", "success")
        return redirect(url_for("index"))
    return render_template("add_project.html", form=form)


@app.route("/edit<int:post_id>", methods=["GET", "POST"])
def edit(post_id):
    project = ProjectPost.query.get_or_404(post_id)

    # import existing info to fill form up
    form = ProjectForm(
        title=project.title, description=project.description, link=project.link
    )

    # handle new info added to form
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.link = form.link.data

        db.session.commit()
        flash("Project updated", "success")
        return redirect(url_for("index"))
    return render_template("edit_project.html", form=form, project=project)


@app.route("/delete<int:post_id>", methods=["GET", "POST"])
def delete(post_id):
    project = ProjectPost.query.get_or_404(post_id)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted", "success")
    return redirect(url_for("index"))


@app.route("/edit_about", methods=["GET", "POST"])
def edit_about():
    about = About.query.get_or_404("main")
    form = AboutForm(about_text=about.content)

    if form.validate_on_submit():
        about.content = form.about_text.data
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit_about.html", form=form)


@app.route("/edit_status", methods=["GET", "POST"])
def edit_status():
    status = Status.query.get_or_404("main")

    form = StatusForm(status_text=status.message)

    if form.validate_on_submit():
        status.message = form.status_text.data
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit_status.html", form=form)


# login
@login_manager.user_loader
def load_user(user_id):
    try:
        return Admin.query.get(int(user_id))
    except Exception:
        return None


@app.route("/login", methods=["GET"])
def login():
    auth = request.authorization
    if not auth:
        return Response(
            "Login required", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'}
        )
    username = auth.username
    password = auth.password

    user = Admin.query.filter_by(username=username).first()
    if not user:
        return Response(
            "Invalid credentials",
            401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'},
        )

    if user.check_password(password):
        login_user(user)
        return redirect(url_for("index"))
    return Response(
        "Invalid credentials",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        initialize_default_values_db()
    app.run(debug=True)
