from flask import Blueprint, redirect, render_template, request, url_for
from ..representations.park import CreateParkRequest
from ..representations.location import Location
from .auth import verify_auth


def construct_park_blueprint(user_client, park_client, post_client):
    park_crud = Blueprint('park', __name__)

    @park_crud.route('/')
    def view_parks():
        #check user login
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
        parks = park_client.get_batch({}, offset, limit)
        return render_template('parks.html', parks=parks, user=user)

    @park_crud.route('/<id>/posts')
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
        park = park_client.get_by_id(id)
        posts = post_client.get_batch({'park_id': id}, offset, limit)
        return render_template('posts.html', posts=posts, park=park, user=user)

    @park_crud.route('/<id>/posts/create')
    def create_post(id):
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('token'))
        if claims == None or error_message != None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])

        park = park_client.get_by_id(id)
        return render_template('createpost.html', park=park, user=user)

    @park_crud.route('/create', methods=['GET', 'POST'])
    def create():
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('token'))
        if claims == None or error_message != None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])

        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            park_request = CreateParkRequest(name=data['name'],
                                             description=data['description'],
                                             image_id='hardcoded',
                                             user_id=data['user_id'],
                                             location=Location(lat=data['lat'], lng=data['lng']))
            park = park_client.create(park_request)
            return redirect(url_for('.view_parks'))
        return render_template('createpark.html', user=user)

    return park_crud
