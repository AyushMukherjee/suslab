from flask import request, render_template, templating, url_for, redirect, Blueprint
from flask_security import SQLAlchemyUserDatastore, current_user
from flask_security.decorators import login_required
from suslab.users.forms import editUserInfoForm


users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/users-details',
                 template_folder='templates', static_folder='static')

def _edit_userinfo_db():
    from suslab.models import User, Role, db

    return User, Role, db


def get_user_datastore():
    from suslab.models import User, Role, db

    return SQLAlchemyUserDatastore(db, User, Role)



@login_required
@users_blueprint.route('/')
def user_detail_view():
    return render_template('user_profile.html')
    


@users_blueprint.route('/user-edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def user_edit_view(id):
    User, _, db = _edit_userinfo_db()
    user = User.query.get_or_404(id)
    if current_user.email != user.email:
        print("users mismatch!")
        return render_template('user_profile.html')

    form = editUserInfoForm()
    roles = _(id=None, name='user', description='')

    if form.validate_on_submit():
        user.name = form.name.data
        # user.roles = roles
        user.programme_name = form.programme_name.data
        user.address = form.address.data
        user.contact_number = form.contact_number.data     
        try:
            db.session.add(user)
            db.session.commit()
            return render_template('user_profile.html')
        except Exception as e:
            print('user is not edited ', e)
            return render_template('user_profile_edit.html')

    else:
        print("user did not validate ")
    
        return render_template('user_profile_edit.html', form=form, user=user)


