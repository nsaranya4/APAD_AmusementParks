from flask import Blueprint, render_template, request, redirect, url_for
from .auth import verify_auth


def construct_user_blueprint(user_client, post_client):
    user_crud = Blueprint('user', __name__)

    @user_crud.route('/<id>/posts')
    def view_posts(id):
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('token'))
        if claims == None or error_message != None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])

        page = request.args.get('page', None)
        if page:
            page = page.encode('utf-8')
            skip = int(page)
        else:
            skip = 0
        limit = 10
        offset = skip * 10
        posts = post_client.get_batch({'user_id': id}, offset, limit)
        return render_template('myposts.html', posts=posts, user=user)

    @user_crud.route('/<id>/subscriptions')
    def view_subscriptions(id):
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('token'))
        if claims == None or error_message != None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])
        subscriptions = user_client.get_subscriptions(id)
        parks = []
        for subscription in subscriptions:
            parks.append(subscription.park)
        return render_template('mysubscriptions.html', parks=parks, user=user)

    return user_crud
