from flask import request, render_template, Blueprint, url_for, redirect
from flask_security import current_user

pool = Blueprint('pool', __name__, url_prefix='/pool')

@pool.route('/')
def index():
    return 'Hello world'