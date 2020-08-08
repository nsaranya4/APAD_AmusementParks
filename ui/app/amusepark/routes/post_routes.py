from flask import Blueprint, redirect, render_template, request, url_for
from ..representations.post import CreatePostRequest
from ..representations.location import Location
from .helper import verify_auth, pagination, more_pages


def construct_post_blueprint(firebase_client, user_client, post_client):
    post_crud = Blueprint('post', __name__)

    @post_crud.route('/<id>')
    def view(id):
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('funtech_token'))
        if claims is None or error_message is not None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])
        post = post_client.get_by_id(id)
        post.image_id = firebase_client.get_image_link(post.image_id)
        return render_template('post.html', post=post, user=user)

    @post_crud.route('/tag/<tag>')
    def view_posts(tag):
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('funtech_token'))
        if claims is None or error_message is not None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])
        page, offset, limit = pagination(request)
        posts = post_client.get_batch({'tag': tag}, offset, limit+1)
        for post in posts:
            post.image_id = firebase_client.get_image_link(post.image_id)
        more = more_pages(limit, len(posts))
        return render_template('myposts.html', posts=posts, user=user, page=page, more=more)

    @post_crud.route('/tag', methods=['POST'])
    def view_posts_with_tag():
        data = request.form.to_dict(flat=True)
        tag = data['searchtext']
        return redirect(url_for('.view_posts', tag=str(tag)))

    @post_crud.route('/create', methods=['POST'])
    def create():
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('funtech_token'))
        if claims is None or error_message is not None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])

        if request.method == 'POST':
            image = request.files['image']
            image_id = firebase_client.store_image(image)
            data = request.form.to_dict(flat=True)
            tags = [x.strip().lower().replace('#', '') for x in data['tags'].split(',')]
            post_request = CreatePostRequest(title=data['title'].strip(),
                                             description=data['description'].strip(),
                                             image_id=image_id,
                                             user_id=data['user_id'],
                                             park_id=data['park_id'],
                                             location=Location(lat=data['lat'], lng=data['lng']),
                                             tags=tags)
            post = post_client.create(post_request)
            return render_template('success.html', user=user, msg='Post created Successfully !!')

    return post_crud
