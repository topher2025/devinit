from flask import Flask

from app.main import demo


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(demo)

    return app