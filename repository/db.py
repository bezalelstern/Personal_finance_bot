from datetime import datetime
from database.models import User, Categorise, FixedIncome, TemporaryIncome, init_db, FixedExpenses, TemporaryExpenses
from database.config import db_session




def setup_database():
    init_db()
    print("Connected to database and database is ready.")
    return


def create_report(user_id):


    new_user = User(id=user_id)
    db_session.add(new_user)
    db_session.commit()

    return new_user


def save_temporary_expenses_to_db(user_id, category, amount,time= datetime.now()):

    user = db_session.query(User).get(user_id)

    if not user:
        user = create_report(user_id)

    category_obj = db_session.query(Categorise).filter_by(category_name=category).first()  # חיפוש לפי שם הקטגוריה
    if not category_obj:
        category_obj = create_category(category)

    expense = TemporaryExpenses(user_id=user_id, category_id=category_obj.id, amount=amount, time=time)
    db_session.add(expense)
    db_session.commit()

    return expense


def save_fixed_expenses_to_db(user_id, category, amount,time= datetime.now()):

    user = db_session.query(User).get(user_id)

    if not user:
        user = create_report(user_id)

    category_obj = db_session.query(Categorise).filter_by(category_name=category).first()  # חיפוש לפי שם הקטגוריה
    if not category_obj:
        category_obj = create_category(category)

    expense = FixedExpenses(user_id=user_id, category_id=category_obj.id, amount=amount, time=time)
    db_session.add(expense)
    db_session.commit()

    return expense




def create_category(category_name):
    result = Categorise(category_name=category_name)
    db_session.add(result)
    db_session.commit()
    return result



def save_fixed_income_to_db(user_id, amount):

    user = db_session.query(User).get(user_id)
    if not user:
        raise ValueError(f"User with id {user_id} does not exist.")

    fixed_income = FixedIncome(user_id=user_id, amount=amount, time=datetime.now())
    db_session.add(fixed_income)
    db_session.commit()

    return fixed_income


def save_temporary_income_to_db(user_id, amount):

    user = db_session.query(User).get(user_id)
    if not user:
        raise ValueError(f"User with id {user_id} does not exist.")

    temporary_income = TemporaryIncome(user_id=user_id, amount=amount, time=datetime.now())
    db_session.add(temporary_income)
    db_session.commit()

    return temporary_income
