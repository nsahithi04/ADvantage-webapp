# ADvantage Backend

still in process, only initial steps of are done (login and signup flow)

## Overview

ADvantage is an AI-driven ad generation platform that uses LLMs and APIs to create personalized ads.  
This repository contains the backend, built with Django.

## Tech Stack

- **Backend:** Django
- **Database:** PostgreSQL

## How to Run

1. **Clone the Repository**

```bash
git clone https://github.com/nsahithi04/ADvantage-webapp.git
cd ADvantage-webapp

```

2. **Create a .env file in the root directory with the following details for email configuration:**

```bash
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password

```

3. **Run the Server**

```bash
python manage.py migrate
python manage.py runserver
```

Access it at http://127.0.0.1:8000/auth/signup/
