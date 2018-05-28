import functools

from flask import(
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)
from werkzeug.security import check_password_hash, generate_password_hash

from DefinitelyNotTwitter.database import get_db
from . import user
from . import database as db
from DefinitelyNotTwitter.user import isRestricted
from DefinitelyNotTwitter.auth import login_required
bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('<int:page>')
@login_required
def feedpage(page):
    db = get_db()
    error = None

    allPosts = db.execute(
        'SELECT * FROM post NATURAL JOIN (SELECT uid FROM follows WHERE fid = ?)  JOIN user WHERE user.id = post.uid AND reviewed = 0', (g.user['id'],)
    ).fetchall()
    pagecount = int(len(allPosts) / 5)+1

    order = request.args.get("order")

    if order == "asc":
        posts = db.execute(
            'SELECT * FROM post NATURAL JOIN (SELECT uid FROM follows WHERE fid = ?)  JOIN user WHERE user.id = post.uid AND reviewed = 0 ORDER BY created ASC LIMIT 5 OFFSET ?', (g.user['id'], str(page*5))
        ).fetchall()
    else:
        posts = db.execute(
            'SELECT * FROM post NATURAL JOIN (SELECT uid FROM follows WHERE fid = ?)  JOIN user WHERE user.id = post.uid AND reviewed = 0 ORDER BY created DESC LIMIT 5 OFFSET ?', (g.user['id'], str(page*5))
        ).fetchall()

    if posts is None:
        error = "No posts available."

    if error is None:
        if order == "asc":
            return render_template('blog/index.html', posts = posts, page = page, pagecount = pagecount, order="asc")
        else:
            return render_template('blog/index.html', posts = posts, page = page, pagecount = pagecount, order="desc")

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
                'INSERT INTO post(uid, content, reviewed) VALUES (?, ?, ?)', (g.user['id'], content, g.user['restricted'])
            )
            db.commit()
            return redirect(url_for('user.show_profile', id = g.user['id']))

        flash(error)

    return render_template('blog/create.html')
