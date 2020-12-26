from flask import Flask
from flask_mongoengine import MongoEngine

# Import Installer
from .installer import *

# Import Utils
import time


def create_app(debug=False):
    """ Create an application."""
    app = Flask(__name__)
    app.debug = debug

    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'reacon_token'
    }

    MongoEngine(app)

    @app.cli.command()
    def install():
        """Initialize Settings."""
        install_settings()
        time.sleep(1)
        install_referral_generation_settings()
        time.sleep(1)
        install_currencies()

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
