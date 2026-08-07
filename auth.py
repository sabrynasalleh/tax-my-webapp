# Authentication routes
# Handles user login, logout, password verification and user sessions

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user

# Blueprint separates authentication routes from main app routes
auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return "Login page"

@auth.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("auth.login"))