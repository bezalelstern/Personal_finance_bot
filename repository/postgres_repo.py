import csv
from datetime import datetime
import pandas as pd
from database.models import User, Categorise, FixedIncome, TemporaryIncome, init_db, FixedExpenses, TemporaryExpenses
from database.config_postgres import db_session, engine
from graphs.graph_service.data_from_db import session
import os


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


csv_file = "C:\\Users\\c0548\\PycharmProjects\\Personal_finance_bots\\february-2024.csv"
insert_new_expense(csv_file)


def export_to_csv_with_source_and_user(user_id, record_type):
    output_csv = f"C:\\Users\\c0548\\PycharmProjects\\Personal_finance_bots\\csv_files\\{user_id}_{record_type}.csv"
    try:
        fixed_records, temporary_records, source_types, categories = get_records_and_categories(session, user_id,
                                                                                                record_type)
        write_to_csv(output_csv, fixed_records, temporary_records, source_types, categories, record_type)
        print(f"Data exported successfully to {output_csv}")
        return output_csv
    except Exception as e:
        print(f"Error exporting data to CSV: {e}")
        return False
    finally:
        session.close()


def get_records_and_categories(session, user_id, record_type):
    if record_type == 'expenses':
        fixed_records = session.query(FixedExpenses).filter_by(user_id=user_id).all()
        temporary_records = session.query(TemporaryExpenses).filter_by(user_id=user_id).all()
        source_types = ["Fixed Expenses", "Temporary Expenses"]
        categories = {category.id: category.category_name for category in session.query(Categorise).all()}
    elif record_type == 'incomes':
        fixed_records = session.query(FixedIncome).filter_by(user_id=user_id).all()
        temporary_records = session.query(TemporaryIncome).filter_by(user_id=user_id).all()
        source_types = ["Fixed Incomes", "Temporary Incomes"]
        categories = {}
    else:
        raise ValueError("Invalid record type. Choose 'expenses' or 'incomes'")

    return fixed_records, temporary_records, source_types, categories


def write_to_csv(output_csv, fixed_records, temporary_records, source_types, categories, record_type):
    with open(output_csv, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)

        if record_type == 'expenses':
            writer.writerow(["Category", "Amount", "Time", "Source"])
            write_expenses(writer, fixed_records, temporary_records, categories, source_types)
        else:
            writer.writerow(["Amount", "Time", "Source"])
            write_incomes(writer, fixed_records, temporary_records, source_types)


def write_expenses(writer, fixed_records, temporary_records, categories, source_types):
    for record in fixed_records:
        category_name = categories.get(record.category_id, "Undefined")
        writer.writerow([category_name, record.amount, record.time.isoformat(), source_types[0]])

    for record in temporary_records:
        category_name = categories.get(record.category_id, "Undefined")
        writer.writerow([category_name, record.amount, record.time.isoformat(), source_types[1]])


def write_incomes(writer, fixed_records, temporary_records, source_types):
    for record in fixed_records:
        writer.writerow([record.amount, record.time.isoformat(), source_types[0]])

    for record in temporary_records:
        writer.writerow([record.amount, record.time.isoformat(), source_types[1]])




def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted successfully.")
        else:
            print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"Error deleting file: {e}")


