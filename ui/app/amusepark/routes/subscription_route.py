from flask import Blueprint, redirect, render_template, request, url_for
from ..clients.user_client import UserClient
from ..representations.subscription import CreateSubscriptionRequest

subscription_crud = Blueprint('subscription', __name__)
user_client = UserClient("http://127.0.0.1:5000")


@subscription_crud.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        user_id = data['user_id']
        park_id = data['park_id']
        create_subscription_request = CreateSubscriptionRequest(user_id=user_id, park_id=park_id)
        user_client.create_subscription(create_subscription_request)
        return redirect(url_for('park.view_posts', id=str(park_id)))
