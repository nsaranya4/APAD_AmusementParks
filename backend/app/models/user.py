from repos.db import db



class User(db.Document):
    user_name = db.StringField(required=True, unique=True)
    user_email = db.StringField(required=True, unique=True)
    image_id = db.StringField(required=True)
    user_type = db.StringField(required=True)
    

