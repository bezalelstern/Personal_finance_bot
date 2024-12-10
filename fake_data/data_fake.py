import random
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from database.models import Base, User, Categorise, FixedIncome, TemporaryIncome, TemporaryExpenses, FixedExpenses  # import המודלים שלך

# אתחול של Faker לצורך יצירת נתונים רנדומליים
fake = Faker()

# חיבור לבסיס הנתונים
DATABASE_URL = "postgresql://admin:1234@localhost:5432/fake_data"  # שנה את זה ל-URL של בסיס הנתונים שלך
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def create_random_user():
    """יוצר משתמש רנדומלי"""
    return User(
        fixed_incomes=[],
        temporary_incomes=[],
        temporary_expenses=[],
        fixed_expenses=[]
    )


def create_random_category():
    """יוצר קטגוריה רנדומלית"""
    return Categorise(
        category_name=fake.word()
    )


def create_random_fixed_income(user_id):
    """יוצר הכנסה קבועה רנדומלית"""
    return FixedIncome(
        user_id=user_id,
        amount=random.randint(1000, 10000),
        time=fake.date_this_year()
    )


def create_random_temporary_income(user_id):
    """יוצר הכנסה זמנית רנדומלית"""
    return TemporaryIncome(
        user_id=user_id,
        amount=random.randint(100, 5000),
        time=fake.date_this_year()
    )


def create_random_temporary_expenses(user_id, category_id):
    """יוצר הוצאה זמנית רנדומלית"""
    return TemporaryExpenses(
        user_id=user_id,
        category_id=category_id,
        amount=random.randint(100, 5000),
        time=fake.date_this_year()
    )
def create_random_fixed_expenses(user_id, category_id):
    """יוצר הוצאה זמנית רנדומלית"""
    return FixedExpenses(
        user_id=user_id,
        category_id=category_id,
        amount=random.randint(100, 5000),
        time=fake.date_this_year()
    )


def seed_database():
    """מכניס 100,000 שורות רנדומליות לטבלאות"""
    # צור משתמשים רנדומליים
    users = [create_random_user() for _ in range(1000)]
    session.add_all(users)
    session.commit()

    # צור קטגוריות רנדומליות
    categories = [create_random_category() for _ in range(20)]
    session.add_all(categories)
    session.commit()

    # צור הכנסות קבועות, זמניות והוצאות רנדומליות
    for user in users:
        # הכנסות קבועות
        for _ in range(random.randint(1, 3)):
            user.fixed_incomes.append(create_random_fixed_income(user.id))

        # הכנסות זמניות
        for _ in range(random.randint(1, 3)):
            user.temporary_incomes.append(create_random_temporary_income(user.id))

        #   הוצאות
        for _ in range(random.randint(1, 5)):
            user.temporary_expenses.append(create_random_temporary_expenses(user.id, random.choice(categories).id))
        # הוצאות קבועות
        for _ in range(random.randint(1, 5)):
            user.fixed_expenses.append(create_random_fixed_expenses(user.id, random.choice(categories).id))

    session.commit()
    print("הנתונים נוספו בהצלחה!")


if __name__ == '__main__':
    seed_database()
