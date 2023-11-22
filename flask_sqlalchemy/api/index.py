from typing import List
from flask import render_template, request, redirect, url_for, make_response
# from os import environ
from sys import path
from pathlib import Path
# path.append(str(Path(__file__).parent.parent.absolute()))
path.append(str(Path(__file__).parent.parent.parent.absolute()))

from api.models.user import User
from api.models.email import Email
from api.config import app, db, create_app


@app.route("/", methods=["GET"])
def init():
    with app.app_context():
        print("creating database...")
        db.create_all()
        users = db.session.execute(
            db.select(User).order_by(User.username)).scalars()
        return render_template("user/index.html", users=users)


@app.route("/users")
def user_list():
    users = db.session.execute(
        db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users)


@app.route("/data/users")
def data_users():
    users: List[User] = db.session.execute(
        db.select(User).order_by(User.username)).scalars()
    return make_response([user.to_dict() for user in users], 200)


@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        existing_user = (
            User.query.select_from(User)
            .filter_by(username=request.form["username"])
            .first()
        )
        if not existing_user:
            db.session.add(
                User(
                    username=request.form["username"],
                    # emails=request.form["email"],
                )
            )
            db.session.commit()
            existing_user = (
                User.query.select_from(User)
                .filter_by(username=request.form["username"])
                .first()
            )
        
        db.session.add(
            Email(
                email=request.form["email"], 
                user_id=existing_user.id
            )
        )
        
        db.session.commit()

        user = (
            User.query.select_from(User)
            .filter_by(username=request.form["username"])
            .first()
        )
        return redirect(url_for("user_detail", user=user))

    return render_template("user/create.html")


@app.route("/users/create-and-list", methods=["GET", "POST"])
def user_create_and_list():
    if request.method == "POST":
        existing_user = (
            User.query.select_from(User)
            .filter_by(username=request.form["username"])
            .first()
        )
        if not existing_user:
            db.session.add(
                User(
                    username=request.form["username"],
                    # emails=request.form["email"],
                )
            )
            # db.session.commit()
            existing_user = (
                User.query.select_from(User)
                .filter_by(username=request.form["username"])
                .first()
            )
        
        db.session.add(
            Email(
                email=request.form["email"], 
                user_id=existing_user.id
            )
        )
        
        db.session.commit()

        users = db.session.execute(
            db.select(User).order_by(User.username)).scalars()
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


if __name__ == "__main__":
    create_app()
    app.run(debug=True)
