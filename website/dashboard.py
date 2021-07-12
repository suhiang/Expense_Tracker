import decimal

from flask import redirect, render_template, request, session
from functools import wraps

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Categories, Expense
from . import db
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import DeclarativeMeta

# Converts a list of SQL Alchemy RowProxy objects into a list of dictionary objects with the column name as the key (https://github.com/cs50/python-cs50/blob/develop/src/cs50/sql.py#L328)
# Used for SQL SELECT .fetchall() results
def convertSQLToDict(listOfRowProxy):
    # Coerce types
    rows = [dict(row) for row in listOfRowProxy]
    for row in rows:
        for column in row:

            # Coerce decimal.Decimal objects to float objects
            # https://groups.google.com/d/msg/sqlalchemy/0qXMYJvq8SA/oqtvMD9Uw-kJ
            if type(row[column]) is decimal.Decimal:
                row[column] = float(row[column])

            # Coerce memoryview objects (as from PostgreSQL's bytea columns) to bytes
            elif type(row[column]) is memoryview:
                row[column] = bytes(row[column])

    return rows


    results = db.session.execute(
        "SELECT SUM(amount) AS expenses_month FROM expense WHERE user_id = :usersID AND strftime('%Y',expensedate) = strftime('%Y',date('now')) AND strftime('%m',expensedate) = strftime('%m',date('now'))",
        {"usersID": current_user.id}).fetchall()
    print(results)

# Get and return trends for every spending category that accounts for >1% of overall spend (bubble chart)
def getCurrentMthSpendingTrends(userID):

    spending_trends = []
    categoryTrend = {"name": None, "proportionalAmount": None,
                     "totalSpent": None, "totalCount": None}

    results = db.session.execute("SELECT category, COUNT(category) as count, SUM(amount) as amount FROM expense WHERE user_id = :usersID AND strftime('%Y',expensedate) = strftime('%Y',date('now')) AND strftime('%m',expensedate) = strftime('%m',date('now')) GROUP BY category ORDER BY COUNT(category) DESC",
                         {"usersID": userID}).fetchall()
    categories = convertSQLToDict(results)

    # Calculate the total amount spent
    totalSpent = 0
    for categoryExpense in categories:
        totalSpent += categoryExpense["amount"]

    for category in categories:
        # Do not include category in chart if it's spending accounts for less than 1% of the overall spending
        proportionalAmount = round((category["amount"] / totalSpent) * 100)
        if (proportionalAmount < 1):
            continue
        else:
            categoryTrend["name"] = category["category"]
            categoryTrend["proportionalAmount"] = proportionalAmount
            categoryTrend["totalSpent"] = category["amount"]
            categoryTrend["totalCount"] = category["count"]
            spending_trends.append(categoryTrend.copy())

    return spending_trends

    # Get and return the users total spend for the current month
def getTotalSpend_Month(userID):
    results = db.session.execute(
        "SELECT SUM(amount) AS expenses_month FROM expense WHERE user_id = :usersID AND strftime('%Y',expensedate) = strftime('%Y',date('now')) AND strftime('%m',expensedate) = strftime('%m',date('now'))",
        {"usersID": userID}).fetchall()

    totalSpendMonth = convertSQLToDict(results)

    return totalSpendMonth[0]['expenses_month']

def getSpendingTrends(userID):

    spending_trends = []
    categoryTrend = {"name": None, "proportionalAmount": None,
                     "totalSpent": None, "totalCount": None}

    results = db.session.execute("SELECT category, COUNT(category) as count, SUM(amount) as amount FROM expense WHERE user_id = :usersID AND strftime('%Y',expensedate) = strftime('%Y',date('now')) AND strftime('%m',expensedate) = strftime('%m',date('now')) GROUP BY category ORDER BY COUNT(category) DESC",
                         {"usersID": userID}).fetchall()
    categories = convertSQLToDict(results)

    # Calculate the total amount spent
    totalSpent = 0
    for categoryExpense in categories:
        totalSpent += categoryExpense["amount"]

    for category in categories:
        # Do not include category in chart if it's spending accounts for less than 1% of the overall spending
        proportionalAmount = round((category["amount"] / totalSpent) * 100)
        if (proportionalAmount < 1):
            continue
        else:
            categoryTrend["name"] = category["category"]
            categoryTrend["proportionalAmount"] = proportionalAmount
            categoryTrend["totalSpent"] = category["amount"]
            categoryTrend["totalCount"] = category["count"]
            spending_trends.append(categoryTrend.copy())

    return spending_trends

    # Get and return the users total spend for the each month
def getTotalMonthlySpend(userID):
    results = db.session.execute(
        "SELECT SUM(amount) AS amount, strftime('%m', expensedate) AS month, strftime('%Y', expensedate) AS year from expense \
        WHERE user_id = :usersID GROUP BY strftime('%m', expensedate)+strftime('%Y', expensedate) \
        ORDER BY YEAR DESC, MONTH DESC ",
        {"usersID": userID}).fetchall()

    getTotalMonthlySpend = convertSQLToDict(results)


    return results

    # Get and return the users total spend for the each month
def getTotalMonthlySpendJson(userID):
    results = db.session.execute(
        "SELECT SUM(amount) AS amount, strftime('%m', expensedate) AS month, strftime('%Y', expensedate) AS year from expense \
        WHERE user_id = :usersID GROUP BY strftime('%m', expensedate)+strftime('%Y', expensedate) \
        ORDER BY YEAR DESC, MONTH DESC ",
        {"usersID": userID}).fetchall()

    app_json = json.dumps(convertSQLToDict(results),sort_keys=True)
    return app_json