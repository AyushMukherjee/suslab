from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin
from flask_security import RoleMixin, UserMixin

from suslab import db

# TODO: Split files

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


class ReferenceUserMixin():
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id'))
    
    @declared_attr
    def user(cls):
        return db.relationship('User', backref=db.backref(cls.__name__.lower(), uselist=False))


class ProductBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


# Library Tables
class Product(ProductBase):
    __tablename__ = 'products'

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    needed_by = db.Column(db.DateTime, nullable=False)

    # borrower-product relationship: parent=product, child=borrower, many-one relationship
    borrower_id = db.Column(db.Integer, db.ForeignKey('borrowers.id'))
    borrower = db.relationship('Borrower', backref=db.backref('products'))

    # lender-product relationship: parent=product, child=lender, many-one relationship
    lender_id = db.Column(db.Integer, db.ForeignKey('lenders.id'))
    lender = db.relationship('Lender', backref=db.backref('products'))


class Borrower(ReferenceUserMixin, db.Model):
    __tablename__ = 'borrowers'

    id = db.Column(db.Integer, primary_key=True)


class Lender(ReferenceUserMixin, db.Model):
    __tablename__ = 'lenders'
    
    id = db.Column(db.Integer, primary_key=True)


# Pool Tables
pool_signup_table = db.Table(
    'pools_signups',
    db.Column('pools', db.Integer, db.ForeignKey('pools.id')),
    db.Column('signups', db.Integer, db.ForeignKey('signups.id')),
)

class Pool(ProductBase):
    __tablename__ = 'pools'

    from_ = db.Column(db.String(32), nullable=False)
    to_ = db.Column(db.String(32), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    vehicle = db.Column(db.String(32), nullable=False)
    spots = db.Column(db.Integer, nullable=False)

    # pooler-pool relationship: parent=pool, child=pooler, many-one relationship
    pooler_id = db.Column(db.Integer, db.ForeignKey('poolers.id'))
    pooler = db.relationship('Pooler', backref=db.backref('pools'))

    # pool-signup relationship: parent=pool, child=signup, many-many relationship
    signups = db.relationship('Signup', secondary='pools_signups', backref=db.backref('pools'))


class Pooler(ReferenceUserMixin, db.Model):
    __tablename__ = 'poolers'

    id = db.Column(db.Integer, primary_key=True)


class Signup(ReferenceUserMixin, db.Model):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
