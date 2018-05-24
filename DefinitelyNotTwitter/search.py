import functools

from flask import(
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)
from werkzeug.security import check_password_hash, generate_password_hash

from DefinitelyNotTwitter.database import get_db
from . import user
from . import database as db

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        db = get_db()
        query = request.form['query']
        error = None
        results = None

        if not query:
            error = "Type your search query above."

        if error is None:
            results = db.execute(
            'SELECT * FROM post WHERE content LIKE "%'+query+'%"'
            ).fetchall()

        if results is None:
            error = 'We couldnt find anything matching your query'

        if error is None:
            return render_template('search/results.html', results = results, page = 0)

        flash(error)
    return render_template('search/results.html')

@bp.route('/advanced', methods=('GET', 'POST'))
def advanced():
    db = get_db()

    if request.method == 'POST':
        userStr = request.form['username']
        content = request.form['content']
        userSearch = request.form['userSearch']
        stringSearch = request.form['stringSearch']
        error = None

        if userSearch:
            users = db.execute(
                'SELECT * FROM user WHERE name LIKE ?', ('%' + userStr + '%')
            )
