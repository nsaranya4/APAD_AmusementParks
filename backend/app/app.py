from flask import Flask
from flask_restful import Resource, Api
from resources.routes import initialize_routes
from repos.db import initialize_db

app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://127.0.0.1/funtech'
}
initialize_db(app)
initialize_routes(api)



if __name__ == '__main__':
    app.run(port=5000,debug=True)  # important to mention debug=True