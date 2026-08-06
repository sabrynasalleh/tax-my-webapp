from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Database handler:
# Manages communication between Flask and the SQL database.
db = SQLAlchemy()

# Migration handler:
# Tracks changes to database models and creates migration files when tables/columns are modified.
migrate = Migrate()

# Authentication manager:
# Handles login sessions, user loading, and access control for protected pages.
login_manager = LoginManager()