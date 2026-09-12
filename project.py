from flask import Blueprint, render_template, redirect, redirect, request, url_for
from flask_login import current_user, login_required
from extensions import db
from datetime import datetime
from models import Project, Business, Client

project = Blueprint("project", __name__)

# Route
@project.route("/projects", methods=["GET", "POST"])
@login_required
def project_management():

    # Get the right company belonging to the current user
    company = current_user.company

    # Handle project creation form
    if request.method == "POST":

        # Get project information
        title = request.form.get("title")
        status = request.form.get("status")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        # Convert date time
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        business_id = request.form.get("business_id")
        client_id = request.form.get("client_id")

        # Find selected business
        business_data = Business.query.filter_by(
            id=business_id,
            company_id=company.id
        ).first()

        # Find selected client
        client_data = Client.query.filter(
            Client.id == client_id,
            Client.businesses.any(Business.company_id == company.id)
        ).first()

        # Business validity
        if not business_data:
            return "Invalid business selection.", 400

        # Client validity
        if not client_data:
            return "Invalid client selection.", 400

        # Create new project
        new_project = Project(
            title=title,
            status=status,
            start_date=start_date,
            end_date=end_date,
            business_id=business_data.id,
            client_id=client_data.id
        )

        # Add project to database
        db.session.add(new_project)
        db.session.commit()

        # Return to project page
        return redirect(url_for("project.project_management"))
    
    businesses = Business.query.filter_by(
        company_id=company.id
    ).all()

    clients = Client.query.filter(
        Client.businesses.any(Business.company_id == company.id)
    ).all()

    projects = Project.query.filter(
        Project.business.has(Business.company_id == company.id)
    ).all()

    return render_template(
        "projects.html",
        businesses=businesses,
        clients=clients,
        projects=projects
    )

# Route for editing project
@project.route("/projects/edit/<int:project_id>", methods =["GET", "POST"])
@login_required
def edit_project(project_id):

    company = current_user.company

    project_data = Project.query.filter(
        Project.id == project_id,
        Project.business.has(Business.company_id == company.id)
    ).first_or_404()

    if request.method == "POST":
        title = request.form.get("title")
        status = request.form.get("status")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        business_id = request.form.get("business_id")
        client_id = request.form.get("client_id")

        # Find the selected business within user's company
        business_data = Business.query.filter_by(
            id=business_id,
            company_id=company.id
        ).first()

        # Find the selected client
        client_data = Client.query.filter(
            Client.id == client_id,
            Client.businesses.any(Business.company_id == company.id)
        ).first()

        # Validation
        if not business_data:
            return "Invalid business selection.", 400

        if not client_id:
            return "Invalid client selection.", 400

        # Convert date strings into Python date objects
        if start_date:
            start_date = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).date()

        if end_date:
            end_date = datetime.strptime(
                end_date,
                "%Y-%m-%d"
            ).date()


        # Update existing project
        project_data.title = title
        project_data.status = status
        project_data.start_date = start_date
        project_data.end_date = end_date
        project_data.business_id = business_data.id
        project_data.client_id = client_data.id

        db.session.commit()

        return redirect(url_for("project.project_management"))

    # Get business

    businesses = Business.query.filter_by(
        company_id=company.id
    ).all()

    # Get client

    clients = Client.query.filter(Client.businesses.any(Business.company_id == company.id)
    ).all()

    # Get project

    projects = Project.query.filter(
        Project.business.has(Business.company_id == company.id)
    ).all()

    return render_template(
        "projects.html",
        businesses=businesses,
        clients=clients,
        projects=projects,
        editing_project=project_data
    )




        