import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE= os.path.join(app.instance_path, 'flaskr.sqlte')
    )

    if test_config is None:
        app.config.from_pyfile(app.instance_path, 'config.py')
    else:
        app.config.from_mapping(test_config)

    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return 'Hello, world !'

    from . import db
    db.init_app(app)

    return app
