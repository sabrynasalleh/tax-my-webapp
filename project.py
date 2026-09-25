from flask import Blueprint, render_template, redirect, redirect, request, url_for, flash
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
        try:
            if start_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

            if end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        except ValueError:
            flash("Please enter valid dates.", "error")
            return redirect(url_for("project.project_management"))

        business_id = request.form.get("business_id")
        client_id = request.form.get("client_id")

        # Validation
        if not title:
            flash("Project title is required.", "error")
            return redirect(url_for('project.project_management'))

        if len(title) > 50:
            flash("Project title must have 50 characters or fewer.", "error")
            return redirect(url_for('project.project_management'))

        # Validate business and client selection
        if not business_id:
            flash("Please select a business.", "error")
            return redirect(url_for("project.project_management"))

        # Validate date error
        if start_date and end_date and end_date < start_date:
            flash("End date cannot be before start date.", "error")
            return redirect(url_for("project.project_management"))

        # Find selected business
        business_data = Business.query.filter_by(
            id=business_id,
            company_id=company.id
        ).first()

        # Business validation
        if not business_data:
            flash("Please select a valid business.", "error")
            return redirect(url_for("project.project_management"))

        # Find selected client
        client_data = Client.query.filter(
            Client.id == client_id,
            Client.businesses.any(Business.company_id == company.id)
        ).first()

        # Client validation
        if not client_data:
            flash("Please sekect a valid client.", "error")
            return redirect(url_for("project.project_management"))

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

        flash("Project created successfully.", "success")

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
        title = request.form.get("title", "").strip()
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
        if not title:
            flash("Project title is required.", "error")
            return redirect(
                url_for("project.edit_project", project_id=project_id)
            )

        if len(title) > 50:
            flash("Project title must be 50 characters or fewer.", "error")
            return redirect(
                url_for("project.edit_project", project_id=project_id)
            )

        if not business_id:
            flash("Please select a business.", "error")
            return redirect(
                url_for("project.edit_project", project_id=project_id)
            )

        if not client_id:
            flash("Please select a client", "error")
            return redirect(
                url_for("project.edit_project", project_id=project_id)
            )

        # Convert date strings into Python date objects
        try:
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

        except ValueError:
            flash("Please enter valid dates.", "error")
            return redirect(
                url_for("project.edit_project", project_id=project_id)
            )

        if start_date and end_date and end_date < start_date:
            flash("End date cannot be before the start date.", "error")
            return redirect(
                url_for("project.edit_project", project_id=project_id)
            )

       
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

# Route for deleting project
@project.route("/projects/delete/<int:project_id>", methods=["POST"])
@login_required
def delete_project(project_id):

    company = current_user.company

    # Find the project only if it belongs to the user's company
    project_data = Project.query.filter(
        Project.id == project_id,
        Project.business.has(Business.company_id == company.id)
    ).first_or_404()

    # Delete selected project
    db.session.delete(project_data)
    db.session.commit()

    return redirect(url_for("project.project_management"))



        