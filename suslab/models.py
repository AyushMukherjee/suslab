'This module implements the data model classes'

from sqlalchemy.ext.declarative import declared_attr
from sqlathanor import FlaskBaseModel, initialize_flask_sqlathanor

from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin
from werkzeug.local import LocalProxy

db = SQLAlchemy(model_class = FlaskBaseModel)
db = initialize_flask_sqlathanor(db)

# TODO: Split files

# User Tables
# Same user can have many roles and same role can have many users
roles_users = db.Table(
    'roles_users',
    db.Column('users', db.Integer(), db.ForeignKey('users.id')),
    db.Column('roles', db.Integer(), db.ForeignKey('roles.id')),
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, supports_json=True)
    email = db.Column(db.String(128), unique=True, supports_json=True)
    password = db.Column(db.String(32))
    name = db.Column(db.String(64), supports_json=True)
    active = db.Column(db.Boolean(), supports_json=True)
    confirmed_at = db.Column(db.DateTime(), supports_json=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class ReferenceUserMixin():
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id'), supports_json=True)
    
    @declared_attr
    def user(cls):
        return db.relationship('User', backref=db.backref(cls.__name__.lower(), uselist=False), supports_json=True)


class ProductBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, supports_json=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), supports_json=True)
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp(), supports_json=True)


# Library Tables
class Product(ProductBase):
    __tablename__ = 'products'

    name = db.Column(db.String(128), nullable=False, supports_json=True)
    description = db.Column(db.String(512), nullable=False, supports_json=True)
    duration = db.Column(db.Integer, nullable=False, supports_json=True)
    needed_by = db.Column(db.DateTime, nullable=False, supports_json=True)

    # borrower-product relationship: parent=product, child=borrower, many-one relationship
    borrower_id = db.Column(db.Integer, db.ForeignKey('borrowers.id'), supports_json=True)
    borrower = db.relationship('Borrower', backref=db.backref('products'), supports_json=True)

    # lender-product relationship: parent=product, child=lender, many-one relationship
    lender_id = db.Column(db.Integer, db.ForeignKey('lenders.id'), supports_json=True)
    lender = db.relationship('Lender', backref=db.backref('products'), supports_json=True)


class Borrower(ReferenceUserMixin, db.Model):
    __tablename__ = 'borrowers'

    id = db.Column(db.Integer, primary_key=True, supports_json=True)


class Lender(ReferenceUserMixin, db.Model):
    __tablename__ = 'lenders'
    
    id = db.Column(db.Integer, primary_key=True, supports_json=True)


# Pool Tables
pool_signup_table = db.Table(
    'pools_signups',
    db.Column('pools', db.Integer, db.ForeignKey('pools.id')),
    db.Column('signups', db.Integer, db.ForeignKey('signups.id')),
)

class Pool(ProductBase):
    __tablename__ = 'pools'

    from_ = db.Column(db.String(32), nullable=False, supports_json=True)
    to_ = db.Column(db.String(32), nullable=False, supports_json=True)
    time = db.Column(db.DateTime, nullable=False, supports_json=True)
    vehicle = db.Column(db.String(32), nullable=False, supports_json=True)
    spots = db.Column(db.Integer, nullable=False, supports_json=True)

    # pooler-pool relationship: parent=pool, child=pooler, many-one relationship
    pooler_id = db.Column(db.Integer, db.ForeignKey('poolers.id'), supports_json=True)
    pooler = db.relationship('Pooler', backref=db.backref('pools'), supports_json=True)

    # pool-signup relationship: parent=pool, child=signup, many-many relationship
    signups = db.relationship('Signup', secondary='pools_signups', backref=db.backref('pools'), supports_json=True)


class Pooler(ReferenceUserMixin, db.Model):
    __tablename__ = 'poolers'

    id = db.Column(db.Integer, primary_key=True, supports_json=True)


class Signup(ReferenceUserMixin, db.Model):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True, supports_json=True)
