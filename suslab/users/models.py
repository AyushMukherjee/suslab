from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin
from flask_security import RoleMixin, UserMixin, current_user

from suslab import db


# User Tables
# Same user can have many roles and same role can have many users
roles_users = db.Table(
    'roles_users',
    db.Column('users', db.Integer(), db.ForeignKey('users.id')),
    db.Column('roles', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(32))
    name = db.Column(db.String(64))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Library User Tables
# Same borrower can have many lenders and same lender can have many borrowers
class LibraryUser(User):
    # @declared_attr
    # def products(cls):
    #     return db.relationship('Product', backref=db.backref(cls.__tablename__))
    
    loan_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    due_date = db.Column(db.DateTime, default=db.func.current_timestamp())

borrowers_lenders = db.Table(
    'borrowers_lenders',
    db.Column('borrowers', db.Integer(), db.ForeignKey('borrowers.id')),
    db.Column('lenders', db.Integer(), db.ForeignKey('lenders.id'))
)

# TODO: abstract to mixin
class Borrower(db.Model):
    __tablename__ = 'borrowers'
    
    # borrower-user relationship
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref=db.backref("borrower", uselist=False))

    # borrower-product relationship
    products = db.relationship('Product', backref=db.backref('borrower'))

# TODO: abstract to mixin
class Lender(db.Model):
    __tablename__ = 'lenders'

    # lender-user relationship
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref=db.backref("lender", uselist=False))

    # lender-product relationship
    products = db.relationship('Product', backref=db.backref('lender'))

    # lender-borrower relationship
    borrowers = db.relationship('Borrower', secondary='borrowers_lenders',
                                backref=db.backref('lenders'))

# Library Tables
class ProductBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class Product(ProductBase):
    __tablename__ = 'products'

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=False)

    borrower_id = db.Column(db.Integer, db.ForeignKey('borrowers.id'))
    lender_id = db.Column(db.Integer, db.ForeignKey('lenders.id'))


# Pool Tables
class Pooler(db.Model):
    __tablename__ = 'poolers'

    # pooler-user relationship
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref=db.backref("pooler", uselist=False))

    # pooler-pool relationship
    pool = db.relationship('Pool', backref=db.backref('pooler'))


class Pool(Productbase):
    __abstract__ = True

    place = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(512))

    pooler_id = db.Column(db.Integer, db.ForeignKey('poolers.id'))
