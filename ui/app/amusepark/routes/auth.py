import re
from google.auth.transport import requests
import google.oauth2.id_token


# We have taken this code from sampleProject
def verify_auth(id_token):
    error_message = None
    claims = None
    firebase_request_adapter = requests.Request()
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

            if 'email' not in claims:
                print('email not found\n', claims)
                error = 'FATAL ERROR! EMAIL NOT FOUND'
                return ([], error)

            if 'name' not in claims:
                regex = r'(.*)@(.*)\.(.*)'
                claims['name'] = re.match(regex, claims['email'])[1]
                print('name not found\n', claims)

        except ValueError as exc:
            error_message = str(exc)

    return claims, error_message
