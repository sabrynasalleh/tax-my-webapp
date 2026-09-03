from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models import Business

business = Blueprint("business", __name__)

# Route for business
@business.route("/business", methods=["GET", "POST"])
@login_required
def business_management():

    # Ensure the company opened belong to the current user
    company = current_user.company

    if request.method == "POST":
        business_name = request.form.get("business_name")
        description = request.form.get("description")

        new_business = Business(
            company_id = company.id,
            business_name = business_name,
            description = description
        )

        db.session.add(new_business)
        db.session.commit()

        return redirect(url_for("business.business_management"))

    businesses = Business.query.filter_by(company_id=company.id).all()

    return render_template(
        "business.html",
        businesses=businesses,
    )

@business.route("/business/edit/<int:business_id>", methods=["GET", "POST"])
@login_required
def edit_business(business_id):

    company = current_user.company

    business_data = Business.query.filter_by(
        id=business_id,
        company_id=company.id
    ).first_or_404()

    if request.method == "POST":
        business_data.business_name = request.form.get("business_name")
        business_data.description = request.form.get("description")

        db.session.commit()

        return redirect(url_for("business.business_management"))

    businesses = Business.query.filter_by(company_id=company.id).all()

    return render_template(
        "business.html",
        businesses=businesses,
        editing_business=business_data
    )

@business.route("/business/delete/<int:business_id>", methods=["POST"])
@login_required
def delete_business(business_id):

    company = current_user.company

    business_data = Business.query.filter_by(
        id=business_id,
        company_id=company.id
    ).first_or_404()

    db.session.delete(business_data)
    db.session.commit()

    return redirect(url_for("business.business_management"))