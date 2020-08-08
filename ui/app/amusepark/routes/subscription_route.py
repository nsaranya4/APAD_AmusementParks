from flask import Blueprint, redirect, request, url_for, render_template
from ..representations.subscription import CreateSubscriptionRequest
from .helper import verify_auth


def construct_subscription_blueprint(user_client):
    subscription_crud = Blueprint('subscription', __name__)

    @subscription_crud.route('/create', methods=['POST'])
    def create():
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('funtech_token'))
        if claims is None or error_message is not None:
            return redirect(url_for('auth.login'))

        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            user_id = data['user_id']
            park_id = data['park_id']
            create_subscription_request = CreateSubscriptionRequest(user_id=user_id, park_id=park_id)
            user_client.create_subscription(create_subscription_request)
            return redirect(url_for('park.view_posts', id=str(park_id)))

    @subscription_crud.route('/delete', methods=['POST'])
    def delete():
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('funtech_token'))
        if claims is None or error_message is not None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])

        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            subscription_id = data['subscription_id']
            # check if the subscription belongs to user. Can be done on backend also
            error = user_client.delete_subscription(subscription_id)
            if error is None:
                return redirect(url_for('user.view_subscriptions', id=str(user.id)))
            else:
                return render_template('error.html', user=user)

    return subscription_crud
