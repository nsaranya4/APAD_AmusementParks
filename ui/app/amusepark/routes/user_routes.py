from flask import Blueprint, redirect, render_template, request, url_for, session
from flask import make_response, send_file, jsonify
from ..clients.post_client import PostClient

user_crud = Blueprint('user', __name__)
post_client = PostClient("http://localhost:5000")


@user_crud.route('/<manage>')
def management(manage):
    user_id = ""
    if manage == 'posts':
        return redirect(url_for('.view_posts', id=str(user_id)))
    elif manage == 'parks':
        return redirect(url_for('.view_parks', id=str(user_id)))
    elif manage == 'subscriptions':
        return redirect(url_for('.view_subscriptions', id=str(user_id)))
    else:
        return redirect(url_for('.view_posts', id=str(user_id)))


@user_crud.route('/<id>/posts')
def view_posts(id):
    return


@user_crud.route('/<id>/parks')
def view_parks(id):
    return


@user_crud.route('/<id>/subscriptions')
def view_subscriptions(id):
    return