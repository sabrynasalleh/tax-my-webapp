# Authentication routes
# Handles user login, logout, password verification and user sessions

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
import models

# Blueprint separates authentication routes from main app routes
auth = Blueprint("auth", __name__)

# Handles user login
# GET: Displays login form. POST: Checks credentials & creates user session
@auth.route("/login", methods=["GET", "POST"])
def login():

     if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        # Find user by email
        user = models.User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("home"))

     return render_template("login.html")

@auth.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("auth.login"))