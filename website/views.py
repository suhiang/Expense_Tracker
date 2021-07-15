import requests
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Notes, Categories, Expenses
from . import db
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from . import dashboard
import requests
from sqlalchemy import asc, desc

from website import models

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def expenses():
    if request.method == 'POST':
        description = request.form.get('description')
        category = request.form.get('category')
        expensedate = datetime.strptime(request.form.get('expensedate'),'%Y-%m-%d')
        amount = request.form.get('amount')
        submittime = datetime.now()

        if len(description) < 1:
            flash('Description is too short!', category='error')
        else:
            new_expense = Expenses(description=description, category=category, expensedate=expensedate, amount=amount, submittime=submittime, user_id=current_user.id)
            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added!', category='success')

        print(request.form.get('expensedate'))

    # expensesCurrentmonth = dashboard.getTotalSpend_Month(current_user.id)
    # print('Total expense for this month',expensesCurrentmonth)

    # SpendingTrends = dashboard.getSpendingTrends(current_user.id)
    # print('Spending Trends for this month',SpendingTrends)

    # expensesMonthly = dashboard.getTotalMonthlySpend(current_user.id)
    # print('Monthly Spending',expensesMonthly)

    items = Expenses.query.all()
    categories = Categories.query.order_by(Categories.name).all()

    return render_template("expense.html", user=current_user, expenses=items, categories=categories)

@views.route('/delete-expense', methods=['POST'])
def delete_expense():
    expense = json.loads(request.data)
    expenseId = expense['expenseId']
    expense = Expenses.query.get(expenseId)
    print(expenseId)
    if expense:
       db.session.delete(expense)
       db.session.commit()

    return jsonify({})

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Notes(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Notes.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    # items = Categories.query.all()
    items = Categories.query.order_by(Categories.name).all()

    if request.method == 'POST':
        categoryname = request.form.get('category').strip()
        if not categoryname in map(lambda x: x.name,items):
            if len(categoryname) < 1:
                flash('category is too short!', category='error')
            else:
                new_category = Categories(name=categoryname)
                db.session.add(new_category)
                db.session.commit()
                flash('Category added!', category='success')
        else:
            flash('Exist', category='error')
    # items = Categories.query.all()
    return render_template("category.html", user=current_user, categories=items)

@views.route('/delete-category', methods=['POST'])
def delete_category():
    category = json.loads(request.data)
    categoryId = category['categoryId']
    category = Categories.query.get(categoryId)
    if category:
       db.session.delete(category)
       db.session.commit()

    return jsonify({})

@views.route('/reports', methods=['GET'])
@login_required
def reports():
    expensesCurrentmonth = dashboard.getTotalSpend_Month(current_user.id)
    print('Total expense for this month',expensesCurrentmonth)

    SpendingTrends = dashboard.getSpendingTrends(current_user.id)
    print('Spending Trends for this month',SpendingTrends)

    expensesMonthly = dashboard.getTotalMonthlySpend(current_user.id)

    href = 'http://127.0.0.1:5000/api/v1/expense/monthly'
    params = {
    'type': 'monthly',
    'userid': 1,
    }
    # return requests.get('http://example.com').content
    # expensesMonthly = requests.get('http://127.0.0.1:5000/api/v1/expense/monthly')
    expensesMonthlyJson = dashboard.getTotalMonthlySpendJson(current_user.id)

    js=json.loads(expensesMonthlyJson)
    print('Test 1 - Monthly Spending',expensesMonthly)
    print('Test 2 - Monthly Spending Json', js)   # Jinja parses json with single quote!!!
    print('Test 3 - Monthly Spending Json', expensesMonthlyJson) # Jinja uunable to parse json with double quote!!!


    return render_template("reports.html", user=current_user, expensesMonthly=js, expensesMonthlyJson=js)

@views.route('/api/v1/expense/monthly', methods=['GET'])
def api_monthly():
    # http://127.0.0.1:5000/api/v1/expense/monthly
    type = request.args.get('type')
    # expensesCurrentmonth = dashboard.getTotalMonthlySpend(current_user.id)
    expensesCurrentmonth = dashboard.getTotalMonthlySpendJson(1)
    print(expensesCurrentmonth)
    return expensesCurrentmonth

@views.route('/api/v1/expense/monthly/all', methods=['GET'])
def api_monthlyTotal_all():
    # http://127.0.0.1:5000/api/v1/expense/monthly/all
    expensesCurrentmonth = dashboard.getTotalSpend_Month(current_user.id)
    return jsonify(expensesCurrentmonth)

@views.route('/api/v1/expense/monthly/trend', methods=['GET'])
def api_monthlyTotal_trend():
    # http://127.0.0.1:5000/api/v1/expense/monthly/trend
    expensesCurrentmonth = dashboard.getSpendingTrends(current_user.id)
    return jsonify(expensesCurrentmonth)


# Examples of API query ------------------------------------------------------------------

@views.route('/query-example', methods=['GET'])
def query_example():
    # http://127.0.0.1:5000/query-example?language=Python
    # http://127.0.0.1:5000/query-example?language=Python&framework=Flask&website=DigitalOcean
    # if key doesn't exist, returns None
    language = request.args.get('language')

    # if key doesn't exist, returns a 400, bad request error
    framework = request.args['framework']

    # if key doesn't exist, returns None
    website = request.args.get('website')

    return '''
              <h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              <h1>The website value is: {}'''.format(language, framework, website)


# GET requests will be blocked
"""
    {
        "language" : "Python",
        "framework" : "Flask",
        "website" : "Scotch",
        "version_info" : {
            "python" : "3.9.0",
            "flask" : "1.1.2"
        },
        "examples" : ["query", "form", "json"],
        "boolean_test" : true
    }
"""
@views.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    language = None
    framework = None
    python_version = None
    example = None
    boolean_test = None

    if request_data:
        if 'language' in request_data:
            language = request_data['language']

        if 'framework' in request_data:
            framework = request_data['framework']

        if 'version_info' in request_data:
            if 'python' in request_data['version_info']:
                python_version = request_data['version_info']['python']

        if 'examples' in request_data:
            if (type(request_data['examples']) == list) and (len(request_data['examples']) > 0):
                example = request_data['examples'][0]

        if 'boolean_test' in request_data:
            boolean_test = request_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)