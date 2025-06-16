from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import UserMixin
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# used to create the user class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    Age = db.Column(db.String, nullable=False)
    current_map = db.Column(db.String)


# user to create the map data class
class Map(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    map_points = db.Column(db.String, nullable=False)


def check_credentials(input_name, input_password):
    engine = create_engine('sqlite:///admins.db')
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()

    class Admin(Base):
        __tablename__ = 'admins'

        id = Column(Integer, autoincrement=True, primary_key=True)
        name = Column(String, unique=True, nullable=False)
        password = Column(String, nullable=False)

    Base.metadata.create_all(engine)
    admin = session.query(Admin).filter_by(name=input_name).first()
    if admin and check_password_hash(admin.password, input_password):
        return True
    return False


# function to create an admin
if __name__ == '__main__':
    engine = create_engine('sqlite:///admins.db')
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()


    class Admin(Base):
        __tablename__ = 'admins'

        id = Column(Integer, autoincrement=True, primary_key=True)
        name = Column(String, unique=True, nullable=False)
        password = Column(String, nullable=False)


    Base.metadata.create_all(engine)


    def add_admin(name, password):
        hashed_password = generate_password_hash(password)
        new_admin = Admin(name=name, password=hashed_password)
        session.add(new_admin)
        session.commit()


    # MANUALLY INPUT ADMIN INFO
    add_admin('erik', 'Erik_password')
