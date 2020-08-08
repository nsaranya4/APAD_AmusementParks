from flask import Blueprint, redirect, render_template, request, url_for
from ..representations.park import CreateParkRequest
from ..representations.location import Location
from .helper import verify_auth, pagination, more_pages


def construct_park_blueprint(firebase_client, user_client, park_client, post_client):
    park_crud = Blueprint('park', __name__)

    @park_crud.route('/')
    def view_parks():
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('funtech_token'))
        if claims is None or error_message is not None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])
        page, offset, limit = pagination(request)
        parks = park_client.get_batch({}, offset, limit+1)
        for park in parks:
            park.image_id = firebase_client.get_image_link(park.image_id)
        subscriptions = user_client.get_subscriptions(user.id)
        park_subscription_map = {}
        for subscription in subscriptions:
            park_subscription_map[subscription.park.id] = subscription.id
        more = more_pages(limit, len(parks))
        return render_template('parks.html', parks=parks, user=user, park_subscription_map=park_subscription_map, page=page, more=more)


    @park_crud.route('/<id>/posts')
    def view_posts(id):
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('funtech_token'))
        if claims is None or error_message is not None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])
        page, offset, limit = pagination(request)
        park = park_client.get_by_id(id)
        park.image_id = firebase_client.get_image_link(park.image_id)
        posts = post_client.get_batch({'park_id': id}, offset, limit+1)
        for post in posts:
            post.image_id = firebase_client.get_image_link(post.image_id)
        more = more_pages(limit, len(posts))
        return render_template('posts.html', posts=posts, park=park, user=user, page=page, more=more)

    @park_crud.route('/<id>/posts/create')
    def create_post(id):
        # check user login
        (claims, error_message) = verify_auth(request.cookies.get('funtech_token'))
        if claims is None or error_message is not None:
            return redirect(url_for('auth.login'))
        user = user_client.get_by_email_id(claims['email'])
        park = park_client.get_by_id(id)
        park.image_id = firebase_client.get_image_link(park.image_id)
        return render_template('createpost.html', park=park, user=user)

    @park_crud.route('/create', methods=['GET', 'POST'])
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
            park_request = CreateParkRequest(name=data['name'].strip(),
                                             description=data['description'].strip(),
                                             image_id=image_id,
                                             user_id=data['user_id'],
                                             location=Location(lat=data['lat'], lng=data['lng']))
            park, error = park_client.create(park_request)
            if error is not None:
                return render_template('error.html', user=user)
            else:
                return render_template('success.html', user=user, msg='Park created Successfully !!')

        return render_template('createpark.html', user=user)

    return park_crud
