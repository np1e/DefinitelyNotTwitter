import os

from flask import Flask
from flask_bootstrap import Bootstrap
from . import database as db
from . import auth
from . import user
from . import blog
from . import search

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE = os.path.join(app.instance_path, 'DefinitelyNotTwitter.sqlite'),
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
    app.add_url_rule('/', endpoint='index')

    return app
