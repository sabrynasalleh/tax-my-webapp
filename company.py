from flask import Blueprint, render_template
from flask_login import login_required, current_user

company = Blueprint("company", __name__)

# Displays company profile of the logged-in user
@company.route("/company")
@login_required
def company_profile():

    print("========== COMPANY ROUTE ==========")
    print("CURRENT USER:", current_user)
    print("CURRENT USER TYPE:", type(current_user))
    print("HAS COMPANY:", hasattr(current_user, "company"))
    print("HAS COMPANIES:", hasattr(current_user, "companies"))

    company = current_user.company

    return render_template("company_profile.html", company=company)