# ADvantage Backend

still in process, only initial steps are done

ADvantage is a Django-based web platform that allows users to generate personalized advertisements using current trends, AI agents, and external APIs. The system also includes a secure user authentication flow with features like password reset via OTP.

## Overview

ADvantage is an AI-driven ad generation platform that uses LLMs and APIs to create personalized ads.  
This repository contains the backend, built with Django.

## Tech Stack

- **Backend:** Django
- **Database:** PostgreSQL

## project structure

├── AD_gen/ # Ad generation scripts and agents
├── user_auth/ # Django app for user authentication
├── static/ # CSS and JS files
├── templates/ # HTML templates
├── create_tables.sql # SQL script to create necessary database tables
├── manage.py # Django project manager
├── requirements.txt # Required dependencies
└── README.md # You're here!

## How to Run

## 🔧 Prerequisites

- Python 3.9+
- Git
- PostgreSQL (or MySQL depending on your DB setup)
- pip

## 🚀 Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/nsahithi04/ADvantage-webapp/tree/main
   cd ADvantage
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**
   Make sure PostgreSQL or MySQL is running, then:
   - Create a database named `advantage`.
   - Create tables using the provided SQL script:
     - For PostgreSQL:
       ```bash
       psql -U your_user -d advantage -f create_tables.sql
       ```
     - For MySQL:
       ```bash
       mysql -u your_user -p advantage < create_tables.sql
       ```
   - Update your `settings.py` with your database credentials.

## 🧠 Set Up Trends Data (One-Time)

Run the following to populate the trends DB:

```bash
python AD_gen/google_trends.py
```

5. **Migrate & Setup Django**

```bash
python manage.py makemigrations
python manage.py migrate

```

6. **Run the Server**

```bash
python manage.py runserver
```

Access it at http://127.0.0.1:8000

7. **Folder Highlights**

AD_gen/
-google_trends.py: Fetches trends and saves to DB.
-trend_fetcher.py: Aggregates trend info.
-trend_research_agent.py: Uses LLM to expand trend.
-insert_db.py: Inserts finalized trends into DB.
-generate_ads_from_db.py: Generates ads from trends.

user_auth/
-Contains the core Django app for:
-User registration & login
-OTP management
-Password reset
-Dashboard

8. **To-Do After Setup**
   -Ensure .env for secure credentials e.g., DB credentials, API keys.
   -Add OpenAI / LLM API keys
   -Confirm DB access for all teammates
   -Finalize front-end flow if hosted
