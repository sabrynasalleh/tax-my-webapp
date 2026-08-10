from flask import Blueprint, render_template
from flask_login import login_required, current_user

company = Blueprint("company", __name__)

# Displays company profile of the logged-in user
@company.route("/company")
@login_required
def company_profile():

    companies = current_user.companies

    return render_template("company_profile.html", companies=companies)