# Authentication routes
# Handles user login, logout, password verification and user sessions

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user
import models

# Blueprint separates authentication routes from main app routes
auth = Blueprint("auth", __name__)

# Handles user login
# GET: Displays login form. POST: Checks credentials & creates user session
@auth.route("/login", methods=["GET", "POST"])
def login():

     print("LOGIN ROUTE HIT")
     print("METHOD:", request.method)

     if request.method == "POST":

        print("LOGIN FORM RECEIVED")

        email = request.form.get("email")
        password = request.form.get("password")

        print(email)
        print(password)

        # Find user by email
        #user = models.User.query.filter_by(email=email).first()

       # if user:
            # Password checking WILL be added
        #    login_user(user)
         #   return redirect("home")

     return render_template("login.html")

@auth.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("auth.login"))