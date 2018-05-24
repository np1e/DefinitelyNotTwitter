import functools

from flask import(
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)
from werkzeug.security import check_password_hash, generate_password_hash

from DefinitelyNotTwitter.database import get_db
from . import user
from . import database as db
from . import user
from DefinitelyNotTwitter.auth import login_required

bp = Blueprint('admin', __name__, url_prefix='/admin')



def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['admin'] != 1:
            return redirect(url_for('blog.feed'))

        return view(**kwargs)
    return wrapped_view

@bp.route('/user_view')
@admin_required
def user_view():
    db = get_db()
    from DefinitelyNotTwitter.user import get_user
    user = get_user(g.user['id'])

    if user['admin'] == 1:
        return render_template('userview.html')
    else:
        error = "You are not an admin. Booh!"
        flash(error)
        return redirect(url_for('blog.feed'))

<<<<<<< HEAD
@bp.route('/panel')
def admin_panel():

    return render_template('admin/')
=======

@bp.route('/userview')
@admin_required
def user_view():


    return render_template('admin/userview.html')

@bp.route('/review')
@admin_required
def review_panel():

    
    return render_template('admin/panel.html')

@login_required
def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['admin'] != 1:
            error = "You have no admin privileges!"
            flash(error)
            return redirect(url_for('user.show_profile', id = g.user['id']))

        return view(**kwargs)
    return wrapped_view
>>>>>>> feature_admin
