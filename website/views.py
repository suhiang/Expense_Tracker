from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Categories, Expense
from . import db
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from . import dashboard

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
            new_expense = Expense(description=description, category=category, expensedate=expensedate, amount=amount, submittime=submittime, user_id=current_user.id)
            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added!', category='success')

        print(request.form.get('expensedate'))

    expensesCurrentmonth = dashboard.getTotalSpend_Month(current_user.id)
    print('Total expense for this month',expensesCurrentmonth)

    SpendingTrends = dashboard.getSpendingTrends(current_user.id)
    print('Spending Trends for this month',SpendingTrends)

    expensesMonthly = dashboard.getTotalMonthlySpend(current_user.id)
    print('Monthly Spending',expensesMonthly)

    items = Expense.query.all()
    categories = Categories.query.all()

    return render_template("expense.html", user=current_user, expenses=items, categories=categories)


@views.route('/delete-expense', methods=['POST'])
def delete_expense():
    expense = json.loads(request.data)
    expenseId = expense['expenseId']
    expense = Expense.query.get(expenseId)
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
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    items = Categories.query.all()
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
    items = Categories.query.all()
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

