from flask import Blueprint, redirect, request, url_for
from ..representations.subscription import CreateSubscriptionRequest
from .auth import verify_auth

def construct_subscription_blueprint(user_client):
    subscription_crud = Blueprint('subscription', __name__)

    @subscription_crud.route('/create', methods=['POST'])
    def create():
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('token'))
        if claims == None or error_message != None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])

        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            user_id = data['user_id']
            park_id = data['park_id']
            create_subscription_request = CreateSubscriptionRequest(user_id=user_id, park_id=park_id)
            user_client.create_subscription(create_subscription_request)
            return redirect(url_for('park.view_posts', id=str(park_id)), user=user)

    return subscription_crud
