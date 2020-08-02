from flask import Blueprint, redirect, render_template, request, url_for, session
from flask import make_response, send_file, jsonify
from ..clients.post_client import PostClient
from ..clients.user_client import UserClient

user_crud = Blueprint('user', __name__)
post_client = PostClient("http://localhost:5000")
user_client = UserClient("http://localhost:5000")


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
    parks = user_client.get_subscriptions(user.id)
    return render_template('mysubscriptions.html', parks=parks, user=user)
