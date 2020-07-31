import os
from flask import Flask, redirect, url_for


def create_app():
    app = Flask(__package__)

    # Set the secret key to some random bytes
    app.secret_key = os.urandom(16)

    from .routes.auth_routes import auth_crud
    app.register_blueprint(auth_crud, url_prefix='/')

    from .routes.post_routes import post_crud
    app.register_blueprint(post_crud, url_prefix='/posts')

    return app