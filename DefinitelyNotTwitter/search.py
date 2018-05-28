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
            'SELECT * FROM post, user WHERE content LIKE ? AND user.id = post.uid', ('%' + query + '%',)
            ).fetchall()

        if results is None:
            error = 'We couldnt find anything matching your query'

        if error is None:
            return render_template('search/results.html', results = results, page = 0)

        flash(error)
    return render_template('search/results.html')

@bp.route('/refined', methods=('GET', 'POST'))
def searchrefined():
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        contentcontains = request.form['contentcontains']
        error = None

        if user is None and contentcontains is None:
            error = "You must enter some values for refined search."

        if error is None:
            if contentcontains is None and username is not None:
                results = db.execute(
                'SELECT * FROM post, user WHERE name LIKE ? AND user.id = post.uid', ('%' + username + '%',)).fetchall()
            elif contentcontains is not None and username is None:
                results = db.execute(
                'SELECT * FROM post, user WHERE content LIKE ? AND user.id = post.uid', ('%' + contentcontains + '%',)).fetchall()
            else:
                results = db.execute(
                'SELECT * FROM post, user WHERE name LIKE ? AND content LIKE ? AND user.id = post.uid', ('%' + username + '%', '%' + contentcontains + '%',)).fetchall()

        if results is None:
            error = 'We couldnt find anything matching your query'

        if error is None:
            return render_template('search/results.html', results = results, page = 0)

        flash(error)
    return render_template('search/results.html')
