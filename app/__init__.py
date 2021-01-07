# Import Flask Things
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine

# Import Installer
from .installer import *
from .errors import handle_404_errors, handle_500_errors

# Import Utils
import os
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
    CORS(app)

    @app.cli.command()
    def install():
        """Initialize Settings."""
        print(f'Application Environment => {os.environ.get("FLASK_ENV")}')
        install_settings()
        time.sleep(1)
        install_referral_generation_settings()
        time.sleep(1)
        install_currencies()
        time.sleep(1)
        install_demo_user()

    app.register_error_handler(404, handle_404_errors)
    app.register_error_handler(500, handle_500_errors)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
