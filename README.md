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
- **Python 3.11**
- **Django 2.2.28**
- **Virtualenv** (optional)

### Steps

### Option 1: Setup with **Anaconda** (recommended)
This method uses **Anaconda** for creating and managing virtual environments.

1. Install **Anaconda**  
   Download and install Anaconda from [here](https://www.anaconda.com/download/).

2. **Clone the repository**:
   ```sh
   git clone https://github.com/riabrez/UnidFood.git
   cd unidfood
   ```

3. Create a virtual environment and activate it:
   ```sh
   cd ~  # Navigate to your home directory
   mkdir Workspace  # Create a new directory if it doesn't exist
   cd Workspace  # Go into the Workspace directory
   conda create -n unidfood python=3.11  # Create a virtual environment named 'unidfood'
   conda activate unidfood  # Activate the virtual environment
   ```

### Option 2: Setup with **Python venv** (if you don't want to use Anaconda)
This method uses the standard **venv** module to create a virtual environment.

1. **Clone the repository:**
   ```sh
   git clone https://github.com/riabrez/UnidFood.git
   cd unidfood

2. Create a virtual environment:
   ```sh
   python3 -m venv unidfood  # Create a virtual environment named 'unidfood'
   ```
   
3. Activate the virtual environment:
   > On windows:
   ```sh
   unidfood\Scripts\activate
   ```
   > On Mac/Linux:
   ```sh
   source unidfood/bin/activate
   ```
### Common Steps
Once the virtual environment is activated, continue with the following steps:

4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

5. Create and apply migrations:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
   
6. Populate the database:
   ```sh
   python population_script.py

   ```

7. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```sh
   python manage.py runserver
   ```

## Usage

1. Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.
2. Sign up or log in.
3. Search for restaurants, leave reviews, and schedule meetups.





