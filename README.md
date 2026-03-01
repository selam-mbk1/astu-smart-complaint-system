# ASTU Smart Complaint & Issue Tracking System

**Full-Stack Web Application** for managing campus complaints at **Adama Science and Technology University (ASTU)**.  
Built with **Django**, **REST API**, and **Tailwind CSS**, this system allows students, staff, and admins to efficiently submit, track, and manage complaints.

---

## 🔹 Features

### For Students
- Submit complaints/issues by category (Dormitory, Academic, Internet/Facilities).
- Dynamic location fields (Dorm Block, Building Name, Course Code) based on selected category.
- Attach files (images) with complaints.
- View complaint status and receive notifications via dashboard and email.

### For Staff
- View complaints related to their department.
- Update complaint status (Open, In Progress, Resolved) and add remarks.
- Receive notifications for new complaints in their department.

### For Admins
- Manage users (add, edit, delete).
- Manage complaint categories and departments.
- View analytics: total complaints, resolution rate, top issues, and charts.
- Oversee recent complaints and attachments.

### General
- AI-powered chatbot to guide users on submitting complaints.
- Role-based access control (Student, Staff, Admin).
- notifications for users and admins.
- Responsive and modern UI using Tailwind CSS.

---

## 🔹 Technology Stack

**Backend**
- Python 3.x
- Django 5.x
- Django REST Framework (DRF)
- SQLite / PostgreSQL

**Frontend**
- HTML, CSS, JavaScript
- Tailwind CSS
- Django Templates
- Chart.js for analytics

**Authentication & Security**
- Django authentication system
- JWT authentication (for API endpoints)

**Development Tools**
- Git & GitHub
- Virtual Environment (`venv`)
- VS Code / PyCharm

---

## 🔹 Installation & Setup

 **Clone the repository**
```bash
git clone https://github.com/selam-mbk1/astu-smart-complaint-system.git
cd astu-smart-complaint-system
Create a virtual environment

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Install dependencies

pip install -r requirements.txt

Run migrations

python manage.py migrate

Create superuser (admin)

python manage.py createsuperuser

Run the server

python manage.py runserver

Access the app

Open your browser: http://127.0.0.1:8000

🔹 Usage

Students submit complaints using the dashboard.

Staff members update complaint status and add remarks.

Admins manage users, categories, and monitor analytics.
