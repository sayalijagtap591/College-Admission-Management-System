College Admission Management System

Project Overview

The College Admission Management System is a web-based application developed using Django and Python. It helps students apply for college admission and allows administrators to manage admission applications and student documents.

Technologies Used

- Python
- Django
- HTML
- CSS
- JavaScript
- SQLite

Features

- Student Registration and Login
- Student Dashboard
- Course Listing
- Online Admission Application
- Student Document Upload
- Student Profile Management
- Admin Dashboard
- Admission Application Status Management
- Document Verification
- Secure Logout and Login Protection

Installation and Setup

1. Clone the Repository

git clone YOUR_GITHUB_REPOSITORY_URL

2. Open the Project Folder

cd admission_portal

3. Install Dependencies

python -m pip install -r requirements.txt

4. Apply Database Migrations

python manage.py migrate

5. Create an Administrator Account

python manage.py createsuperuser

Follow the prompts to create your administrator account.

6. Run the Development Server

python manage.py runserver

Open the application in your browser:

http://127.0.0.1:8000/

Admin Panel

http://127.0.0.1:8000/admin/

Project Purpose

This project demonstrates web application development using Django, database management, user authentication, admission application processing, and document verification.

Future Enhancements

- Email notifications for admission status updates
- Advanced search and filtering
- Admission reports and analytics
- Improved responsive user interface
