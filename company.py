from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from datetime import datetime
from models import Company

company = Blueprint("company", __name__)

# Displays company profile of the logged-in user
@company.route("/company", methods=["GET", "POST"])
@login_required
def company_profile():

    company = current_user.company

    if request.method == "POST":

        if company is None:
            company = Company(
                user_id=current_user.id
            )
            db.session.add(company)

        company.company_name = request.form.get("company_name")
        company.ssm_number = request.form.get("ssm_number")
        financial_year_end = request.form.get("financial_year_end")

        if financial_year_end:
            company.financial_year_end = datetime.strptime(financial_year_end, "%Y-%m-%d").date()

        db.session.commit()

        return redirect(url_for("company.company_profile"))

    return render_template("company_profile.html", company=company)