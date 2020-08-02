from flask import Blueprint, redirect, render_template, request, url_for
from ..representations.post import CreatePostRequest
from ..representations.location import Location


def construct_post_blueprint(post_client):
    post_crud = Blueprint('post', __name__)

    @post_crud.route('/<id>')
    def view(id):
        post = post_client.get_by_id(id)
        return render_template('post.html', post=post)

    @post_crud.route('/create', methods=['POST'])
    def create():
        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            tags = [x.strip() for x in data['tags'].split(',')]
            post_request = CreatePostRequest(title=data['title'],
                                             description=data['description'],
                                             image_id='hardcode',
                                             user_id=data['user_id'],
                                             park_id=data['park_id'],
                                             location=Location(lat=data['lat'], lng=data['lng']),
                                             tags=tags)
            post = post_client.create(post_request)
            return redirect(url_for('park.view_posts', id=str(post.park.id)))

    return post_crud
