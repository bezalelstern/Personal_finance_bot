import csv
from datetime import datetime
from database.models import User, Categorise, FixedIncome, TemporaryIncome, init_db, FixedExpenses, TemporaryExpenses
from database.config_postgres import db_session, engine
from graphs.graph_service.data_from_db import session


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

    category_obj = db_session.query(Categorise).filter_by(category_name=category).first()
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



def save_fixed_income_to_db(user_id, amount,description):

    user = db_session.query(User).get(user_id)
    if not user:
        raise ValueError(f"User with id {user_id} does not exist.")

    fixed_income = FixedIncome(user_id=user_id, amount=amount, time=datetime.now(),description=description)
    db_session.add(fixed_income)
    db_session.commit()

    return fixed_income


def save_temporary_income_to_db(user_id, amount,description):

    user = db_session.query(User).get(user_id)
    if not user:
        raise ValueError(f"User with id {user_id} does not exist.")

    temporary_income = TemporaryIncome(user_id=user_id, amount=amount, time=datetime.now(),description=description)
    db_session.add(temporary_income)
    db_session.commit()

    return temporary_income


def get_or_create_category(category_name):
    category = session.query(Categorise).filter_by(category_name=category_name).first()
    if not category:
        category = Categorise(category_name=category_name)
        session.add(category)
        session.commit()  # שמירה מיידית כדי לקבל ID
    return category.id



def insert_new_expense(csv_file_path):
    with open(csv_file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                date = datetime.strptime(row["date"], "%Y-%m-%d")
                category_id = get_or_create_category(row["category"])
                temp_expense = TemporaryExpenses(
                    user_id=6768207848,
                    category_id=category_id,
                    amount=int(row["amount"]),
                    time=date
                )
                session.add(temp_expense)
            except Exception as e:
                print(f"Error processing row {row}: {e}")
    try:
        session.commit()
        print("Data successfully inserted into the database!")
    except Exception as e:
        session.rollback()
        print(f"Error committing session: {e}")
    finally:
        session.close()



