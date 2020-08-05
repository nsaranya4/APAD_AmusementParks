from flask import Blueprint, redirect, render_template, request, url_for
from ..representations.post import CreatePostRequest
from ..representations.location import Location
from .auth import verify_auth


def construct_post_blueprint(user_client, post_client):
    post_crud = Blueprint('post', __name__)

    @post_crud.route('/<id>')
    def view(id):
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('token'))
        if claims == None or error_message != None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])

        post = post_client.get_by_id(id)
        return render_template('post.html', post=post, user=user)

    @post_crud.route('/tag/<tag>')
    def view_posts(tag):
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
        posts = post_client.get_batch({'tag': tag}, offset, limit)
        return render_template('myposts.html', posts=posts, user=user)

    @post_crud.route('/tag', methods=['POST'])
    def view_posts_with_tag():
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('token'))
        if claims == None or error_message != None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])

        data = request.form.to_dict(flat=True)
        tag = data['searchtext']
        page = request.args.get('page', None)
        if page:
            page = page.encode('utf-8')
            skip = int(page)
        else:
            skip = 0
        limit = 10
        offset = skip * 10
        posts = post_client.get_batch({'tag': tag}, offset, limit)
        return render_template('myposts.html', posts=posts, user=user)

    @post_crud.route('/create', methods=['POST'])
    def create():
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('token'))
        if claims == None or error_message != None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])

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
