from flask import Blueprint, redirect, render_template, request, url_for, session
from flask import make_response, send_file, jsonify, Response
from ..representations.post import CreatePostRequest
from ..representations.location import Location
from ..clients.post_client import PostClient

post_crud = Blueprint('post', __name__)
post_client = PostClient("http://localhost:5000")


@post_crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        post_request = CreatePostRequest()
        location = Location()
        post_request.tags = [x.strip() for x in data['tags'].split(',')]
        post_request.name = data['name']
        post_request.title = data['title']
        post_request.description = data['description']
        post_request.image_id = 'hardcode'
        post_request.user_id = data['user_id']
        post_request.park_id = data['park_id']
        location.lat = data['lat']
        location.lng = data['lng']
        post_request.location = location
        post = post_client.create(post_request)






