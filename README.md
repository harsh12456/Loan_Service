![Django](https://img.shields.io/badge/Django-5.x-green) ![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
# Loan Service Application

A  loan service application built using Django (backend) . The application allows users to register, apply for loans, make payments, and view statements. 
## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)
- [Contributions](#contributions)
- [License](#license)

## Features
- ✅ *User Registration* – Register users with Aadhar ID, email, and annual income.
- ✅ *Loan Application* – Apply for different types of loans (Home, Personal, Car, Business).
- ✅ *Payment Processing* – Make payments toward loans with automatic balance adjustments.
- ✅ *Statement Retrieval* – Fetch detailed loan and payment statements.


## Demo

### Registration Page
- Register user details including Aadhar ID, email, and annual income.

### Apply Loan Page
- Choose loan type, amount, interest rate, and term period.
- View calculated EMI before confirming the loan application.

### Make Payment Page
- Make payments toward approved loans.
- View updated outstanding principal and billing details.

### Statement Page
- View a detailed statement of all loans and payments.
- Track the due date, outstanding balance, and payment history.

## Installation

Follow these steps to set up and run the project locally:

### Backend Setup (Django)

1. *Clone the Repository:*
bash
git clone https://github.com/yourusername/loan-service.git
cd loan-service


2. *Set Up a Virtual Environment:*
bash
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate


3. *Install Dependencies:*
bash
pip install -r requirements.txt


4. *Run Migrations:*
bash
python manage.py makemigrations
python manage.py migrate


5. *Start the Django Server:*
bash
python manage.py runserver








4. *Access the Application:*
- Backend – [http://127.0.0.1:8000](http://127.0.0.1:8000)


## Usage

1. *Register User*
- Enter user details (Aadhar ID, email, and income).
- Register user and calculate the credit score automatically.

2. *Apply for Loan*
- Select loan type and input details (loan amount, interest rate, term period).
- View calculated EMI and apply for the loan.

3. *Make Payment*
- Select loan and enter payment amount.
- View updated outstanding principal and billing information.

4. *Get Statement*
- View detailed loan and payment history.
- Check upcoming due dates and outstanding balances.

## Technologies Used

*Backend:*
- Django
- Django REST Framework

*Database:*
- MySQL (or SQLite for development)

*Others:*
- Logging and Error Handling
- Async Task Handling using async/await

## Project Structure

loan-service/  
├── backend/  
│   ├── loan_service/  
│   │   ├── __init__.py  
│   │   ├── settings.py  
│   │   ├── urls.py  
│   │   ├── wsgi.py  
│   ├── credit/  
│   │   ├── models.py  
│   │   ├── views.py  
│   │   ├── serializers.py  
│   │   ├── urls.py     
├── manage.py  
├── README.md  


## Future Improvements
- ✅ Add OAuth-based authentication using Google or LinkedIn.
- ✅ Support more loan types and repayment options.
- ✅ Integrate email notifications for billing and payment reminders.
- ✅ Optimize async task handling using Celery + Redis instead of django-crontab.
- ✅ Add better error tracking and debugging with Sentry.
- ✅ Build a mobile-responsive frontend using React Native.

## Contributions

Contributions are welcome! If you’d like to add new features or improve the existing codebase, feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.
