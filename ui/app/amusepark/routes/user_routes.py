from flask import Blueprint, render_template, request


def construct_user_blueprint(user_client, post_client):
    user_crud = Blueprint('user', __name__)

    @user_crud.route('/<id>/posts')
    def view_posts(id):
        page = request.args.get('page', None)
        if page:
            page = page.encode('utf-8')
            skip = int(page)
        else:
            skip = 0
        limit = 10
        offset = skip * 10
        user = user_client.get_by_id(id)
        posts = post_client.get_batch({'user_id': id}, offset, limit)
        return render_template('myposts.html', posts=posts, user=user)

    @user_crud.route('/<id>/subscriptions')
    def view_subscriptions(id):
        user = user_client.get_by_id(id)
        subscriptions = user_client.get_subscriptions(user.id)
        parks = []
        for subscription in subscriptions:
            parks.append(subscription.park)
        return render_template('mysubscriptions.html', parks=parks, user=user)

    return user_crud
