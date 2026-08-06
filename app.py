from flask import Flask, render_template
from extensions import db, migrate, login_manager
import models

# Flask app creation
app = Flask(__name__)

# Database configuration:
# Defines where the application stores its database.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

# Prevents unnecessary tracking overhead from SQLAlchemy.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect database feature to Flask app
db.init_app(app)
migrate.init_app(app, db)

# Connect authentication system to Flask
# Enables login sessions and user authentication
login_manager.init_app(app)

# Redirects to login route if a user tries to access a protected page without logging in
login_manager.login_view = "login"

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/clients")
def clients():
    return render_template("clients.html")

@app.route("/income")
def income():
    return render_template("income.html")

@app.route("/expenses")
def expenses():
    return render_template("expenses.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True)