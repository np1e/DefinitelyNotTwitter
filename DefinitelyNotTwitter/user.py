import functools
from . import auth
from flask import(
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from DefinitelyNotTwitter.database import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

def get_user(id):
    user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (id,)
    ).fetchone()

    if user is None:
        abort(404, 'User with id {} doesn\'t exist.'.format(id))

    return user

@bp.route('/<int:id>')
def show_profile(id):
    user = get_user(id)
    return render_template('user/profile.html', user = user)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    user = get_user(id)

    if id != g.user['id']:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        username = request.form['username']
        desc = request.form['desc']
        newPwd = request.form['newPwd']
        confirm = request.form['confirm']
        db = get_db()
        error = None

        if not confirm:
            error = 'Password is required to confirm.'
        elif not check_password_hash(user['password'], confirm):
            error = 'Incorrect password.'

        if error is None:
            if username is not None:
                db.execute(
                    'UPDATE user SET name = ? WHERE id = ?', (username, id,)
                )
            if desc is not None:
                db.execute(
                    'UPDATE user SET descrip = ? WHERE id = ?', (desc, id,)
                )
            if newPwd is not None:
                db.execute(
                    'UPDATE user SET password = ? WHERE id = ?',
                    (generate_password_hash(newPwd), id,)
                )
            db.commit()
            return redirect(url_for('user.show_profile', id = user['id']))

        flash(error)

    return render_template('user/edit.html', user = user)
