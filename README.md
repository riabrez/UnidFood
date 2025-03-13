# UnidFood

UniDFood is a web application designed for University of Glasgow students to review food spots near the university, discover student deals, and organize meetups with fellow students.

* Features

User Authentication: Signup, login, and logout functionality.

Restaurant Reviews: Users can add ratings and reviews for restaurants.

Meetup Scheduling: Users can schedule meetups at restaurants and invite others.

Search & Filter: Find restaurants based on location, rating, and affordability.

Installation

* Prerequisites

Ensure you have the following installed:

Python 3

Django

Virtualenv (optional but recommended)

* Steps

Clone the repository:

git clone https://github.com/your-repo/unidfood.git
cd unidfood

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Create a superuser:

python manage.py createsuperuser

Run the development server:

python manage.py runserver

* Usage

Visit http://127.0.0.1:8000/ in your browser.

Sign up or log in.

Search for restaurants, leave reviews, and schedule meetups.




