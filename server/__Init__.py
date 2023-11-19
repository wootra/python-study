from flask import render_template, request, redirect, url_for
from .models.user import User
from .config import app, db, create_app

create_app()


@app.route("/", methods=["GET"])
def init():
    with app.app_context():
        print("creating database...")
        db.create_all()
        users = db.session.execute(
            db.select(User).order_by(User.username)
        ).scalars()
        return render_template("user/index.html", users=users)


@app.route("/users")
def user_list():
    users = db.session.execute(
        db.select(User).order_by(User.username)
    ).scalars()
    return render_template("user/list.html", users=users)


@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.html")


@app.route("/users/create-and-list", methods=["GET", "POST"])
def user_create_and_list():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        users = db.session.execute(
            db.select(User).order_by(User.username)
        ).scalars()
        return render_template("user/list.html", users=users)

    return render_template("user/index.html")


@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)


@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", user=user)
