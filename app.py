from flask import Flask, render_template
from extensions import db, migrate, login_manager
from auth import auth
from flask_login import login_required
from company import company
import models

# Flask app creation
app = Flask(__name__)

# Used to securely sign session dat.
app.config["SECRET_KEY"] = "secret-key-change-later"

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
login_manager.login_view = "auth.login"

# Register authentication routes
app.register_blueprint(auth)

# Register company route
app.register_blueprint(company)


# Loads user from database using user ID stored in session
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/projects")
@login_required
def projects():
    return render_template("projects.html")

@app.route("/clients")
@login_required
def clients():
    return render_template("clients.html")

@app.route("/income")
@login_required
def income():
    return render_template("income.html")

@app.route("/expenses")
@login_required
def expenses():
    return render_template("expenses.html")

@app.route("/reports")
@login_required
def reports():
    return render_template("reports.html")

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True)