# Enterprise Management Web App
A web application for business management built with Python and Flask to help Malaysian Enterprise owners organise business activities, clients, projects, and financial records all in one place.

**Project Status:** In Development

## Overview

Managing an Enterprise involves coordinating business activities, maintaining client relationships, tracking projects and organising financial records. 

This project aims to bring all these workflows together in a centralised web application while laying the foundation for financial reporting and Malaysian Enterprise tax-related calculations.

## Features

### Implemented

- **User Authentication:** User login and logout using Flask-Login.
- **Enterprise Profile Management:** View and manage Enterprise information.
- **Business Management:** Create, edit, and manage business activities.
- **Client Management:** Create, edit, view, and delete client records.
- **Project Management:** Organise and manage projects associated with clients and business activities.
- **Database Management:** Manage schema changes using Flask-Migrate and Alembic.
- **Template Inheritance:** Reusable page layouts using Jinja2.

### Planned / In Development
- [] Income Management
- [] Expense Management
- [] Financial Dashboard
- [] Document and Receipt Management
- [] Financial Reprting
- [] Malaysian Enterprise Tax Calculation Module

## Technology Stack
| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Flask-SQLAlchemy | ORM and database models |
| Flask-Migrate | Database migrations |
| Alembic | Schema version control |
| Flask-Login | User authentication |
| SQLite | Development database |
| HTML5 | Web page structure |
| CSS3 | Styling |
| Jinja2 | Dynamic HTML templates |
| Git & GitHub | Version control |

## Application Structure

```text
User
└── Enterprise
    ├── Business Activities
    ├── Clients
    ├── Projects
    ├── Income          [Planned]
    ├── Expenses        [Planned]
    ├── Documents       [Planned]
    └── Financial Reports [Planned]
```

## Getting Started

### Prerequisites

- Python 3.10 or later, compatible with the project dependencies
- Git
- A code editor, (Ex: Visual Studio Code)

### 1. Clone the Repository

```bash
git clone https://github.com/sabrynasalleh/tax-my-webapp.git
cd tax-my-webapp
```

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/ Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Configure the environment variables required by the application, including a secure Flask secret key if applicable.

Do not commit passwords, secret keys, or private `.env` files.

### 5. Apply Database Migrations

After configuring Flask to discover the application, run:

```bash
flask db upgrade
```

### 6. Run the Application

If the application is configured for the Flask CLI:

```bash
flask run
```

Open the local address displayed in your terminal, usually:

`http://127.0.0.1:5000`

*Note: Startup commands and environment variable names may need adjustment to match the project configuration.*

## Development Workflow

The project uses Git feature branches to organise development and keep changes manageable

Example branches:

- `feature/base-layout`
- `feature/database`
- `feature/authentication`
- `feature/company-profile`
- `feature/client-management`
- `feature/project-management`
- `feature/income-management`

Features are developed incrementally, comitted with descriptive messages, tested and merged into `main` when ready.

## Project Goals

This project demonstrates practical skills such as:

- Python and Flask web development
- Relational database design and ORM relationships
- Authentication and access control
- CRUD operations and form validation
- Database migrations
- HTML, CSS, and Jinja2
- Git branching and version control
- Incremental software development and testing

## Future Improvements

- Complete income and expense tracking
- Financial summaries and visualisations
- Document and receipt uploads
- Automated testing and improved error handling
- Financial report generation
- Malaysian Enterprise tax calculations based on verified official guidance

## Disclaimer

This is a personal portfolio and learning project under active development. It is not a replacement for professional accounting software, qualified tax advice, or official Malaysian tax filing systems.

Tax-related calculations must be validated against applicable Malaysian legislation and current official guidance before being relied upon for real financial or tax decisions.

## Author

**Sabryna Salleh**

- GitHub: [@sabrynasalleh](https://github.com/sabrynasalleh)
- Repository: [tax-my-webapp](https://github.com/sabrynasalleh/tax-my-webapp) 
