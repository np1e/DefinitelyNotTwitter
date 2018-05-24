import functools
import os
from . import auth as auth

from flask import(
    Blueprint, flash, redirect, render_template, request, session, url_for, g, current_app
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from DefinitelyNotTwitter.database import get_db
from werkzeug.utils import secure_filename

bp = Blueprint('user', __name__, url_prefix='/user')

def get_user(id):
    user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (id,)
    ).fetchone()

    if user is None:
        abort(404, 'User with id {} doesn\'t exist.'.format(id))

    return user

def follows(fid, uid):
    db = get_db()

    if db.execute(
        'SELECT * FROM follows WHERE fid = ? AND uid = ?', (fid, uid)
    ).fetchone() is not None:
        return True
    else:
        return False

@bp.route('/<int:id>')
def show_profile(id):
    db = get_db()
    user = get_user(id)
    following = follows(g.user['id'], user['id'])

    posts = db.execute(
        'SELECT * FROM post WHERE uid = ? ORDER BY created DESC', (id,)
    ).fetchall()

    return render_template('user/profile.html', user = user, follows = following, posts = posts)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from DefinitelyNotTwitter.auth import login_required
@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = get_user(id)

    if request.method == 'POST':
        username = request.form['username']
        desc = request.form['desc']
        newPwd = request.form['newPwd']
        confirm = request.form['confirm']
        db = get_db()
        error = None
        file = None
        imgAdded = False

        # check if the post request has the file part
        if 'file' in request.files:
              f = request.files['file']
              filename = secure_filename(f.filename)
              filetype = filename.rsplit('.', 1)[1].lower()
              f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], str(g.user["id"])+"."+filetype))
              imgAdded = True

        if not confirm:
            error = 'Password is required to confirm.'
        elif not check_password_hash(user['password'], confirm):
            error = 'Incorrect password.'

        if error is None:
            if username is not "":
                db.execute(
                    'UPDATE user SET name = ? WHERE id = ?', (username, id,)
                )
            if desc is not "":
                db.execute(
                    'UPDATE user SET descrip = ? WHERE id = ?', (desc, id,)
                )
            if newPwd is not "":
                db.execute(
                    'UPDATE user SET password = ? WHERE id = ?',
                    (generate_password_hash(newPwd), id,)
                )
            if imgAdded is True:
                db.execute(
                    'UPDATE user SET avatar = ? WHERE id = ?', (1, id,)
                )
            db.commit()
            return redirect(url_for('user.show_profile', id = user['id']))

        flash(error)

    return render_template('user/edit.html', user = user)

@bp.route('/<int:id>/follow')
def follow(id):

    user = get_user(id)
    error = None

    #if no user is logged in, redirect to login
    if not g.user:
        return redirect(url_for('auth.login'))

    #else add follower to user
    db = get_db()
    if db.execute(
        'SELECT * FROM follows where fid = ? AND uid = ?',(g.user['id'], user['id'])
    ).fetchone() is not None:
        error = 'You are already following {}'.format(user['name'])

    if error is None:
        db.execute(
            'INSERT INTO follows (fid, uid) VALUES (?, ?)', (g.user['id'], user['id'])
        )
        db.commit()
        return redirect(url_for('user.show_profile', id = user['id']))

    flash(error)

    return redirect(url_for('user.show_profile', id = user['id']))

@bp.route('/<int:id>/unfollow')
def unfollow(id):
    user = get_user(id)

    #if no user is logged in, redirect to login
    if not g.user:
        return redirect(url_for('auth.login'))

    #else add follower to user
    db = get_db()

    db.execute(
        'DELETE FROM follows WHERE fid = ? AND uid = ?', (g.user['id'], user['id'])
    )
    db.commit()

    return redirect(url_for('user.show_profile', id = user['id']))
