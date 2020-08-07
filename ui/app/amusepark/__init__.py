import os
from flask import Flask, redirect, url_for
from .routes.park_routes import construct_park_blueprint
from .routes.post_routes import construct_post_blueprint
from .routes.user_routes import construct_user_blueprint
from .routes.subscription_route import construct_subscription_blueprint
from .routes.auth_routes import construct_auth_blueprint
from .clients.park_client import ParkClient
from .clients.post_client import PostClient
from .clients.user_client import UserClient
from .clients.firebase_client import FirebaseClient


def create_app():
    config = {
        "development": "config.DevelopmentConfig",
        "production": "config.ProductionConfig",
    }
    config_name = os.getenv('ENVIRONMENT', 'development')
    app = Flask(__package__)
    app.config.from_object(config[config_name])
    firebase_config = {
        "apiKey": "AIzaSyB3DRvsjbOW3fERPd-WtUbixmfiZJvcWfE",
        "authDomain": "funtech-frontend.firebaseapp.com",
        "databaseURL": "https://funtech-frontend.firebaseio.com",
        "projectId": "funtech-frontend",
        "storageBucket": "funtech-frontend.appspot.com",
        "messagingSenderId": "679639892749"
    }

    # Set the secret key to some random bytes
    app.secret_key = os.urandom(16)
    backend_url = app.config['BACKEND_URL']
    park_client = ParkClient(backend_url)
    post_client = PostClient(backend_url)
    user_client = UserClient(backend_url)
    firebase_client = FirebaseClient(firebase_config)

    user_crud = construct_user_blueprint(firebase_client, user_client, post_client)
    app.register_blueprint(user_crud, url_prefix='/users')

    post_crud = construct_post_blueprint(firebase_client, user_client, post_client)
    app.register_blueprint(post_crud, url_prefix='/posts')

    park_crud = construct_park_blueprint(firebase_client, user_client, park_client, post_client)
    app.register_blueprint(park_crud, url_prefix='/parks')

    subscription_crud = construct_subscription_blueprint(user_client)
    app.register_blueprint(subscription_crud, url_prefix='/subscriptions')

    auth_crud = construct_auth_blueprint(user_client)
    app.register_blueprint(auth_crud, url_prefix='/')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
