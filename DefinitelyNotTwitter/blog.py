import functools

from flask import(
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)
from werkzeug.security import check_password_hash, generate_password_hash

from DefinitelyNotTwitter.database import get_db
from . import user
from . import database as db
from DefinitelyNotTwitter.auth import login_required
bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/')
@login_required
def feed():
    db = get_db()
    error = None
    posts = db.execute(
    'SELECT * FROM post NATURAL JOIN (SELECT uid FROM follows WHERE fid = ?)  JOIN user WHERE user.id = post.uid', (g.user['id'],)
    ).fetchall()

    if posts is None:
        error = "No posts available."

    if error is None:
        return render_template('blog/index.html', posts = posts)

    flash(error)

    return render_template('blog/index.html')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    db = get_db()

    if request.method == 'POST':
        content = request.form['content']
        error = None

        if not content:
            error = "Content is required."

        if error is None:
            db.execute(
                'INSERT INTO post(uid, content) VALUES (?, ?)', (g.user['id'], content)
            )
            db.commit()
            return redirect(url_for('user.show_profile', id = g.user['id']))

        flash(error)

    return render_template('blog/create.html')
