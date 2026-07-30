from extensions import db
from datetime import datetime

# User model
# Represents a user who can log in and own company.
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Company model
# Represents company managed by a user
class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    ssm_number = db.Column(db.String(50))
    financial_year_end = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Client model
# Represents a client that belong to a company
class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    company_id = db.Column(db.String, db.ForeignKey("companies.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Project model
# Represents projects by users for companies
class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="Ongoing")
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)