from flask import Flask
from flask_restful import Resource, Api
from resources.routes import initialize_routes
from dal.db import initialize_db

app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/database_name'
}
initialize_routes(api)
initialize_db(app)


if __name__ == '__main__':
    app.run(port=5000,debug=True)  # important to mention debug=True
