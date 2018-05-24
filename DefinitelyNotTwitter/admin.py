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
        if g.user is None:
            return redirect(url_for('auth.login'))
        elif g.user['admin'] != 1:
            return redirect(url_for('blog.feed'))

        return view(**kwargs)
    return wrapped_view

@bp.route('/user_view')
@admin_required
def user_view():
    db = get_db()
    from DefinitelyNotTwitter.user import get_user

    users = db.execute(
        'select * from user as u LEFT OUTER JOIN (select uid, count(uid) as follower from follows group by uid) as f on u.id = f.uid;'
    ).fetchall()



    return render_template('admin/userview.html', users = users)


@bp.route('/panel')
@admin_required
def admin_panel():
    db = get(db)
    return render_template('admin/panel.html')
