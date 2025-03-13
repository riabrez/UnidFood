# UniDFood

UniDFood is a web application designed for University of Glasgow students to:
- Review food spots near the university
- Discover student deals
- Organize meetups with fellow students

## Features

- **User Authentication**: Signup, login, and logout functionality.
- **Restaurant Reviews**: Users can add ratings and reviews for restaurants.
- **Meetup Scheduling**: Users can schedule meetups at restaurants and invite others.
- **Search & Filter**: Find restaurants based on location, rating, and affordability.

## Installation

### Prerequisites
Ensure you have the following installed:
- **Python 3**
- **Django**
- **Virtualenv** (optional but recommended)

### Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/unidfood.git
   cd unidfood
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```sh
   python manage.py migrate
   ```

5. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```sh
   python manage.py runserver
   ```

## Usage

1. Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.
2. Sign up or log in.
3. Search for restaurants, leave reviews, and schedule meetups.





