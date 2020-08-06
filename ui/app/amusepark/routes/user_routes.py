from flask import Blueprint, render_template, request, redirect, url_for
from .auth import verify_auth
from .pagination import pagination


def construct_user_blueprint(user_client, post_client):
    user_crud = Blueprint('user', __name__)

    @user_crud.route('/<id>/posts')
    def view_posts(id):
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('token'))
        if claims == None or error_message != None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])
        page, offset, limit = pagination(request)
        posts = post_client.get_batch({'user_id': id}, offset, limit)
        if len(posts) < limit:
            more = False
        else:
            more = True
        return render_template('myposts.html', posts=posts, user=user, page=page, more=more)

    @user_crud.route('/<id>/subscriptions')
    def view_subscriptions(id):
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('token'))
        if claims == None or error_message != None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])
        subscriptions = user_client.get_subscriptions(id)
        parks = []
        park_subscription_map = {}
        for subscription in subscriptions:
            parks.append(subscription.park)
            park_subscription_map[subscription.park.id] = subscription.id

        return render_template('mysubscriptions.html', parks=parks, user=user,  park_subscription_map=park_subscription_map)

    return user_crud
