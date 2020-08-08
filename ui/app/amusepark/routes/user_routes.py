from flask import Blueprint, render_template, request, redirect, url_for
from .helper import verify_auth, pagination, more_pages


def construct_user_blueprint(firebase_client, user_client, post_client):
    user_crud = Blueprint('user', __name__)

    @user_crud.route('/<id>/posts')
    def view_posts(id):
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('funtech_token'))
        if claims is None or error_message is not None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])
        page, offset, limit = pagination(request)
        posts = post_client.get_batch({'user_id': id}, offset, limit+1)
        for post in posts:
            post.image_id = firebase_client.get_image_link(post.image_id)
        more = more_pages(limit, len(posts))
        return render_template('myposts.html', posts=posts, user=user, page=page, more=more)

    @user_crud.route('/<id>/subscriptions')
    def view_subscriptions(id):
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('funtech_token'))
        if claims is None or error_message is not None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])
        subscriptions = user_client.get_subscriptions(id)
        parks = []
        park_subscription_map = {}
        for subscription in subscriptions:
            parks.append(subscription.park)
            park_subscription_map[subscription.park.id] = subscription.id
        for park in parks:
            park.image_id = firebase_client.get_image_link(park.image_id)

        return render_template('mysubscriptions.html', parks=parks, user=user,  park_subscription_map=park_subscription_map)

    return user_crud
