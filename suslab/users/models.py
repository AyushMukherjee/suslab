from flask_login import UserMixin
from flask_security import RoleMixin, UserMixin, current_user
from suslab import db


# User Tables
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
    products = db.relationship('Product',
                               backref=db.backref('user'))


# Library Tables
products_users = db.Table(
    'products_users',
    db.Column('users', db.Integer(), db.ForeignKey('users.id')),
    db.Column('products', db.Integer(), db.ForeignKey('products.id'))
)


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
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
