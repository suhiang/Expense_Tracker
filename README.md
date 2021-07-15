# A simple application that allows end-users to:
1.	Track their daily expenses

Allow users to input their expenses, minimally the following information:
-	Date
-	Category (a list of pre-set categories, ex. Food, Electricity, Water, Phone, Loan, Grocery, Tax, Insurance, etc)
-	Amount

2.	View total expenses for each month
Allow users to have insight of their spending each month and by each category.

3.	Access the application from simple Graphics User Interface
Technical Requirements

Do design the following based on your expertise and frameworks that you are comfortable with. Below is just an example, for your reference.
1.	Backend Services (eg. Database, APIs etc)
2.	Frontend (eg. Web app, C# WPF etc)
3.	Build framework (eg. ASP.NET MVC, Node.js, Python Flask etc)
4.	Deployment (eg. two or three tiers implementation)
5.	Documentation (A simple architecture diagram to show the entire system components)

## Components used
1. Python Flask
2. SQLite
2. SQL Alchemy
3. Bootstrap

## Setup & Installation

1. Make sure you have the latest version of Python installed.
`Installed version 3.8 (developed using 3.8)`
2. Clone from github
3. Navigate to folder using desired cli (MSWIN: PoSh)
4. Setup environment using desired python version (MS Win)
    - PoSh:
    'C:\Users\suhia\AppData\Local\Programs\Python\Python38-32\python.exe -m venv env`
5. Activate environment
    - PoSh:
        `env\Scripts\activate`
    - Bash:
        `env/Scripts/activate`
6. Install requiremens in environment
    - PoSh/Bash:
        `pip install -r requirements.txt`

## Running The App
```
python main.py
```

## Viewing The App

Go to `http://127.0.0.1:5000`


## Notes:
1. Initial report is currently limited to current month spending.
2. rewrite APIs to handle query parameters
    1. Scenarios to GET various expense using API request with parameters like year and month (and userId)
3. Add/Enhanced GUI
    1. Explore methods to display expense: Tabular versus Charts
    2. Scout approach for Charts
        - tech: e.g. jscript
        - speed to delivery
        - suitability
        - support
        - features
4. Decide on a host for the Python Flask App
    - Heroku : [e.g](https://realpython.com/flask-by-example-part-1-project-setup/)


Deployed at https://vibrant-fromage-80934.herokuapp.com/