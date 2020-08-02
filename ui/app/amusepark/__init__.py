import os
from flask import Flask, redirect, url_for


def create_app():
    app = Flask(__package__)

    # Set the secret key to some random bytes
    app.secret_key = os.urandom(16)

    from .routes.user_routes import user_crud
    app.register_blueprint(user_crud, url_prefix='/users')

    from .routes.post_routes import post_crud
    app.register_blueprint(post_crud, url_prefix='/posts')

    from .routes.park_routes import park_crud
    app.register_blueprint(park_crud, url_prefix='/parks')

    from .routes.subscription_route import subscription_crud
    app.register_blueprint(subscription_crud, url_prefix='/subscriptions')

    return app
