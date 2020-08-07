import pyrebase
import random
import string


class FirebaseClient:
    def __init__(self, firebase_config):
        firebase = pyrebase.initialize_app(firebase_config)
        self.firebase_storage = firebase.storage()

    # Method to generate alphanumeric id of 32 chars
    def generate_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

    def store_image(self, image):
        image_id = "images/{}".format(self.generate_id())
        self.firebase_storage.child(image_id).put(image)
        return image_id

    def get_image_link(self, image_id):
        if image_id.startswith('images/'):
            return self.firebase_storage.child(image_id).get_url(None)
        else:
            return image_id


