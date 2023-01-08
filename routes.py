from flask import Blueprint, redirect, url_for, render_template, request, session, flash
from model import users
from extensions import db

routes = Blueprint("routes", __name__, template_folder="templates")

@routes.route("/")
@routes.route("/home")
def home():
    return render_template("index.html")

@routes.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

@routes.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["user_name"]
        session["user"] = user
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
        flash("Login Succesful!")
        return redirect(url_for("routes.user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("routes.user"))
        return render_template("login.html")

@routes.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("routes.login"))

@routes.route("/logout")
def logout():
    flash(f"You have been logged out!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("routes.login"))