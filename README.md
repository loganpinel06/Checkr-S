# <img src="app/static/images/banner.svg" width="100%" height="350px">

# 💵 About the App
Checkr S is a secure and intuitive web application that is designed to allow users to track monthly transactions with ease.
This project aims to provide more than just a basic CRUD application by digging deeper and ensuring best security practices.
Built primarily with Flask, the app features strong authentication, session security, CSRF protection, rate limiting, and a clean user interface.

# 💡 Features
- ### 🔐 **Secure User Authentication**
    - Username and Password validation with Flask-WTF and Regepx to force strong inputs
    - Flask-Login for secure session handling
    - Configured Session Lifetime to ensure users are logged out after 30 minutes of inactivity
- ### 🗓 **Month and Year Selection**
    - Users can choose a specific year to log transactions in
        - Selections go from the year 2000 to whatever the current year is (future proof)
    - Users can choose a specific month to log transactions in to maintain an organized checkbook
- ### 💰 **Starting Balance Tracker**
    - Users a required to enter a starting balance for each month before they can begin entering transactions
    - This helps users keep track of their total balance just like a real checkbook does
    - After setting a starting balance for a given month, the amount is then updated each time a user creates, edits, or deletes a transaction
    and is marked as 'this months balance'.
- ### 🧾 **Transaction Management**
    - Users can create, edit, and delete transactions
    - Transactions have fields for type (deposit or withdrawal), date, description, and amount
- ### 🚦 **Rate Limiting**
    - This app manages rate limiting using Flask-Limiter and Redis hosted on Upstash to store rate limit data in-memory
    - The addition of rate limiting helps protect the login route from brute-force attacks by limiting the number of requests an individual ip address can make at a time before getting locked for 5 minutes
- ### 📄 **Error Logging**
    - Additionally, this app uses pythons logging module to log errors server-side to the console on Render (stdout)
    - This ensures that users dont obtain access to sensitive information from any potential errors and that errors are logged so they can be fixed
    - (if running the application locally, see the comments on lines 22 & 46 in `__init__.py` to log errors to a .log file using a RotatingFileHandler)

# ⚙️ Tech Stack
- ### **Core Technologies:**
    - Flask
    - HTML
    - SCSS
- ### **Flask Extensions:**
    - Flask-SQLAlchemy (ORM to create database models written in python)
    - Flask-WTF (create secure HTML form with CSRF protection)
    - Flask-Login (handle authentication logic)
    - Flask-Limiter (handle rate limiting to prevent brute force attacks)
- ### **Databases:**
    - PostgreSQL hosted on Supabase (stores all user, transaction, and balance data)
    - Redis hosted on Upstash (used for storing rate limiting data which is constantly being updated)

# 📁 Project Structure
```bash
├── README.md
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── images/
│   │   │   ├── app-logo.PNG
│   │   │   └── banner.svg
│   │   ├── styles.css
│   │   ├── styles.css.map
│   │   └── styles.scss
│   └── templates/
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── base.html
│       └── main/
│           ├── checkbook.html
│           ├── dashboard.html
│           └── edit.html
├── main.py
└── requirements.txt
```

# 🌐 Deployment
Checkr S is deployed via Render with the following production configurations:
- HTTPS enabled automatically with Render
- Gunicorn as the production WSGI server
- Logging to stdout for monitoring errors via Render Logs
Explore Checkr S here: ----

# 💾 Run the Project Locally
### Clone the Repository
```
git clone https://github.com/loganpinel06/CheckBook-App
```
### Create a Python Virtual Environment in the local repository
macOS:
```
python3 -m venv env
```
Windows:
```
python -m venv env
```
### Activate the Virtual Environment
macOS:
```
source env/bin/activate
```
Windows:
```
env\Scripts\activate
```
### Install Dependencies
```
pip install -r requirements.txt
```
### Setup a .env File With:
```
SECRET_KEY=your-secret-key
SUPABASE_CONNECTION_STRING=your-supabase-uri
REDIS_URI=your-redis-uri
```
1. Create a Secret Key which ensures session security and protection from attacks
    - Checkout this Article by [GeeksForGeeks](https://www.geeksforgeeks.org/python/secrets-python-module-generate-secure-random-numbers/) (see the section titled "Generating tokens")
2. Head over to [Supabase](https://supabase.com/) and create an account
    - Create a **FREE** project and follow the steps, **MAKE SURE TO SAVE PROJECT PASSWORD**, can store it in the .env file if you'd like
    - Next click on the **CONNECT** button at the top of the projects dashboard. Make sure the type is **URI** and copy the connection string into the .env
    - Lastly, replace the **'[YOUR-PASSWORD]'** part of the string with the password you saved earlier
3. Lastly head over to [Upstash](https://upstash.com/) and create an account
    - Create a Database and select the **FREE TIER**
    - Once on your new databases dashboard copy the url that starts with `redis://default:` and set it to the REDIS_URI in the .env file
    - Now replace the group of *'s with your databases token which can be copied from the same place as the uri string
### Run the Application
Navigate to main.py in the codebase and run the file!

# 🧠 What I Learned
This was my first attempt at building a full-stack application and I personally learned a ton!
I learned Flask from the ground up, how to write HTML and CSS to structure and style my webpages. I also learned how to manage my time and plan out a full-stack project effectively while keeping the code and codebase clean and understandable. This included keeping my app modular and maintaining a good structure to my project. I also learned many important general skill like how to learn new technologies, read documentation, and use AI as an effective learning tool when stuck. Creating this app has taught me a lot about what it means to be a software developer and how take a problem and leverage my skills in order to create a solution.

Listed here are some bullet points about general topics or features I learned throughout development:
- Flask Routing
    - Route variables, links, methods
- HTTP methods like "GET" & "POST"
- Jinja2 Templating
    - Variables, conditionals, loops
- Building custom database models with Flask-SQLAlchemy
- How to handle basic authentication with Flask-Login
- How to create secure forms with Flask-WTF to protect against CSRF attacks
- How to handle Rate Limiting with Flask-Limiter
- How to flash messages to the user with Flask's flash function
- How to log errors server-side instead of potentially displaying them to the user
- A number of security skills like protecting session cookies, adding session lifetime, secret keys
- How to connect to and use external cloud database providers
    - This includes Supabase and Upstash Redis
- How to build a MODULAR app and maintain structure and cleanliness in my code

# 📌 Future Development
Since this is my first attempt at a full-stack application there is a lot that could be added and developed moving forward both for the app and my personal learning.
These include:
- Adding JavaScript for a better front-end experience
- Using a JavaScript front-end framework like React
- Using a better authentication tool like OAuth or JWTokens
- Containerizing the app with Docker to learn more about DevOps and job-ready practices