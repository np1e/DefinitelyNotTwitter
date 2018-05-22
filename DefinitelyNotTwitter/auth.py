import functools

from flask import(
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)
from werkzeug.security import check_password_hash, generate_password_hash

from DefinitelyNotTwitter.database import get_db
from . import user

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    # when user submitted form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not password == confirm:
            error = 'Passwords must match.'
        elif db.execute(
            'SELECT id FROM user WHERE name = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            # insert new user in database
            db.execute(
                'INSERT INTO user (name, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            print("User inserted")
            db.commit()
            # redirect to login view
            return redirect(url_for('auth.login'))

        flash(error)

    # render register template
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE name = ?', (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('user.show_profile', id = session['user_id']))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
