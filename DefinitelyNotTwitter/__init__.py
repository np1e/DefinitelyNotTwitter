import os

from flask import Flask, g, redirect, url_for
from flask_bootstrap import Bootstrap
from . import database as db
from . import auth
from . import user
from . import blog
from . import search
from . import admin

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)

    UPLOAD_FOLDER = 'DefinitelyNotTwitter/static/img/'

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE = os.path.join(app.instance_path, 'DefinitelyNotTwitter.sqlite'),
        UPLOAD_FOLDER = UPLOAD_FOLDER
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(admin.bp)

    @app.route('/')
    def index():
        if g.user:
            return redirect(url_for('blog.feedpage', page=0))
        else:
            return redirect(url_for('auth.login'))

    return app
