from extensions import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# User model
# Represents a user who can log in and own company.
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One user own 1 company (1:1)

    company = db.relationship(
        "Company",
        backref="owner",
        uselist=False
    )

# Company model
# Represents company managed by a user
class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    company_name = db.Column(db.String(100), nullable=False)
    ssm_number = db.Column(db.String(50))
    financial_year_end = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One company can own many businesses
    businesses = db.relationship(
        "Business",
        backref="company",
        lazy=True

    )

# Business model
# Represents business(es) that a company runs

class Business(db.Model):
    __tablename__ = "businesses"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One business can have many clients
    clients = db.relationship(
        "Client", 
        backref="business", 
        lazy=True
    )

    # One business can have many projects
    projects = db.relationship(
        "Project",
        backref="business",
        lazy=True
    )

    # One business can have many incomes
    incomes = db.relationship(
        "Income",
        backref="business",
        lazy=True
    )

    # One business can have expenses
    expenses = db.relationship(
        "Expense", 
        backref="business",
        lazy=True
    )

# Client model
# Represents a client that belong to a company
class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One client can have many projects
    projects = db.relationship(
        "Project",
        backref="client",
        lazy=True
    )

    # One client can have many income records
    incomes = db.relationship(
        "Income",
        backref="client",
        lazy=True
    )

# Project model
# Represents projects by users for companies
class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="Ongoing")
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One project can have many income records
    incomes = db.relationship(
        "Income",
        backref="project",
        lazy=True
    )

# Income model
# Represents income received by a company (can be linked to clients and projects)
class Income(db.Model):
    __tablename__ = "income"

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=True)
    desc = db.Column(db.String(200))
    amount = db.Column(db.Float)
    date = db.Column(db.Date)
    created_at = db.Column (db.DateTime, default=datetime.utcnow)

# Expense model
# Represents a business expense ro overseee company spending and profit
class Expense (db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200))
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    receipt = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default = datetime.utcnow)