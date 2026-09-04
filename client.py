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
        business_ids = request.form.getlist("business_ids")

        # Validate client name
        if not name:
            return "Client name is required.", 400

        # Ensure at least one business is chosen
        if not business_ids:
            return "Please select at least one business.", 400

        # Find selected business to the current user's company
        selected_businesses = Business.query.filter(
            Business.id.in_(business_ids),
            Business.company_id == company.id
        ).all()

        # Make sure selected businesses are valid
        if len(selected_businesses) != len(business_ids):
            return "Invalid business selection.", 400

        # Create new client
        new_client =  Client(
            name=name,
            email=email,
            phone=phone
        )

        # Associate the client with selected business
        new_client.businesses = selected_businesses

        db.session.add(new_client)
        db.session.commit()

        return redirect(url_for("client.client_management"))

    businesses = Business.query.filter_by(company_id=company.id).all()

    clients = Client.query.filter(
        Client.businesses.any(Business.company_id == company.id)
    ).all()

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

    client_data = Client.query.filter(
        Client.id == client_id, 
        Client.businesses.any(Business.company_id == company.id)
    ).first_or_404()

    if request.method == "POST":
        client_data.name = request.form.get("name")
        client_data.email = request.form.get("email")
        client_data.phone = request.form.get("phone")
        business_ids = request.form.getlist("business_ids")

        # Validate client name
        if not client_data.name:
            return "Client name is required.", 400


        if not business_ids:
            return "Please select at least one business.", 400

        selected_businesses = Business.query.filter(
            Business.id.in_(business_ids),
            Business.company_id == company.id
        ).all()

         # Make sure selected businesses are valid
        if len(selected_businesses) != len(business_ids):
            return "Invalid business selection.", 400
        
        # Update business relationships
        client_data.businesses = selected_businesses

        db.session.commit()

        return redirect(url_for("client.client_management"))

    # Get all businesses
    businesses = Business.query.filter_by(
        company_id=company.id
    ).all()

    # Get all clients
    clients = Client.query.filter(
        Client.businesses.any(Business.company_id == company.id)
    ).all()

    # Display client page with the selected client for editing
    return render_template(
        "clients.html",
        businesses=businesses,
        clients=clients,
        editing_client=client_data
    )

# Route for deleting client
@client.route("/client/delete/<int:client_id>", methods=["POST"])
@login_required
def delete_client(client_id):

    company = current_user.company

    # Find client
    client_data = Client.query.join(Client.businesses).filter(
            Client.id == client_id, 
            Client.businesses.any(Business.company_id == company.id)
        ).first_or_404()

    # Delete client
    db.session.delete(client_data)
    db.session.commit()

    return redirect(url_for("client.client_management"))

