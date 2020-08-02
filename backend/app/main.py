from flask import Flask
from flask_restful import Resource, Api
from resources.routes import initialize_routes
from repos.db import initialize_db
import os


config = {
    "development": "config.DevelopmentConfig",
    "production": "config.ProductionConfig",
}
config_name = os.getenv('FLASK_CONFIGURATION', 'development')

app = Flask(__name__)
app.config.from_object(config[config_name])
api = Api(app)
initialize_db(app)
initialize_routes(api)

if __name__ == '__main__':
    app.run()
