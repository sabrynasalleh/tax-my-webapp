from flask import Flask, render_template
from extensions import db, migrate

# Flask app creation
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/app.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)

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