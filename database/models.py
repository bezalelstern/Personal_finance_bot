from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, BIGINT, BigInteger
from sqlalchemy.orm import relationship
from database.config import engine

Base = declarative_base()



class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)

    fixed_incomes = relationship("FixedIncome", back_populates="user", cascade="all, delete-orphan")
    temporary_incomes = relationship("TemporaryIncome", back_populates="user", cascade="all, delete-orphan")
    fixed_expenses = relationship("FixedExpenses", back_populates="user", cascade="all, delete-orphan")
    temporary_expenses = relationship("TemporaryExpenses", back_populates="user", cascade="all, delete-orphan")


class Categorise(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(80), nullable=False)

    fixed_expenses = relationship("FixedExpenses", back_populates="category", cascade="all, delete-orphan")
    temporary_expenses = relationship("TemporaryExpenses", back_populates="category", cascade="all, delete-orphan")


class TemporaryIncome(Base):
    __tablename__ = 'temporary_income'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    time = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="temporary_incomes")


class FixedIncome(Base):
    __tablename__ = 'fixed_income'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    time = Column(TIMESTAMP, nullable=False)


    user = relationship("User", back_populates="fixed_incomes")

class FixedExpenses(Base):
    __tablename__ = 'fixed_expenses'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    time = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="fixed_expenses")
    category = relationship("Categorise", back_populates="fixed_expenses")


class TemporaryExpenses(Base):
    __tablename__ = 'temporary_expenses'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    time = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="temporary_expenses")
    category = relationship("Categorise", back_populates="temporary_expenses")





def init_db():
    Base.metadata.create_all(engine)



