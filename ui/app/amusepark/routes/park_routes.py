from flask import Blueprint, redirect, render_template, request, url_for, session
from ..clients.post_client import PostClient

park_crud = Blueprint('park', __name__)
post_client = PostClient("http://127.0.0.1:5000")


@park_crud.route('/<id>')
def view(id):
    post = post_client.get_by_id(id)
    return render_template('post.html', post=post)
