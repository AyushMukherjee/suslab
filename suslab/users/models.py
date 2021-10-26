from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin
from flask_security import RoleMixin, UserMixin, current_user

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


class Pooler(db.Model):
    __tablename__ = 'poolers'

    # pooler-user relationship
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref=db.backref("pooler", uselist=False))


class Signup(db.Model):
    __tablename__ = 'signups'

    # signup-user relationship
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref=db.backref("signup", uselist=False))
