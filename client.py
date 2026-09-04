from flask import Blueprint, request, url_for, render_template, redirect
from flask_login import login_required, current_user
from extensions import db
from models import Client, Business


client = Blueprint("client", __name__)

# Routes for displaying and adding clients
@client.route("/clients", methods=["GET", "POST"])
@login_required
def client_management():

    # Get company belonged to the current logged in user
    company = current_user.company

    # Handle client creation form
    if request.method == "POST":

        # Get submitted client information from the form
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        business_id = request.form.get("business_id")

        # Find selected business to the current user's company
        business_data = Business.query.filter_by(
            id=business_id,
            company_id=company.id
        ).first_or_404()

        # Create new client and associate with selected business
        new_client =  Client(
            name=name,
            email=email,
            phone=phone,
            business_id=business_data.id
        )

        db.session.add(new_client)
        db.session.commit()

        return redirect(url_for("client.client_management"))

    businesses = Business.query.filter_by(company_id=company.id).all()

    clients = Client.query.join(Business).filter(Business.company_id == company.id).all()

    # Display page
    return render_template(
        "clients.html",
        businesses=businesses,
        clients=clients
    )

# Route for editing client
@client.route("/clients/edit/<int:client_id>", methods=["GET", "POST"])
@login_required
def edit_client(client_id):

    # Get correct company belonging to the current user
    company = current_user.company

    client_data = Client.query.join(Business).filter(
        Client.id == client_id, 
        Business.company_id == company.id
    ).first_or_404()

    if request.method == "POST":
        client_data.name = request.form.get("name")
        client_data.email = request.form.get("email")
        client_data.phone = request.form.get("phone")
        business_id = request.form.get("business_id")

        business_data = Business.query.filter_by(
            id=business_id,
            company_id=company.id
        ).first_or_404()

        client_data.business_id = business_data.id

        db.session.commit()

        return redirect(url_for("client.client_management"))

    # Get all businesses
    businesses = Business.query.filter_by(
        company_id=company.id
    ).all()

    # Get all clients
    clients = Client.query.join(Business).filter(
        Business.company_id == company.id
    ).all()

    # Display client page with the selected client for editing
    return render_template(
        "clients.html",
        businesses=businesses,
        clients=clients,
        editing_client=client_data
    )