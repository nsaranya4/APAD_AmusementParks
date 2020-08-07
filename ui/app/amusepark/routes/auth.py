from google.auth.transport import requests
import google.oauth2.id_token


# This code is written by using SampleProject as reference
def verify_auth(id_token):
    error_message = None
    claims = None
    firebase_request_adapter = requests.Request()
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            if 'email' not in claims:
                return {}, "USER EMAIL NOT FOUND"
            if 'name' not in claims:
                claims['name'] = claims['email'].split('@')[0]
        except ValueError as exc:
            error_message = str(exc)

    return claims, error_message
