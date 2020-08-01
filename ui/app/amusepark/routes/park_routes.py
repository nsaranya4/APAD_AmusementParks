from flask import Blueprint, redirect, render_template, request, url_for, session
from ..clients.park_client import ParkClient
from ..clients.post_client import PostClient
from ..representations.park import CreateParkRequest, Park
from ..representations.location import Location

park_crud = Blueprint('park', __name__)
park_client = ParkClient("http://127.0.0.1:5000")
post_client = PostClient("http://127.0.0.1:5000")


@park_crud.route('/')
def view_all_park():
    page = request.args.get('page', None)
    if page:
        page = page.encode('utf-8')
        skip = int(page)
    else:
        skip = 0
    limit = 10
    offset = skip * 10
    parks = park_client.get_batch({}, offset, limit)
    return render_template('parks.html', parks=parks)


@park_crud.route('/<id>/posts')
def view_all_post():
    page = request.args.get('page', None)
    if page:
        page = page.encode('utf-8')
        skip = int(page)
    else:
        skip = 0
    limit = 10
    offset = skip * 10
    park = park_client.get_by_id(id)
    posts = post_client.get_batch({}, {'park_id': id}, offset, limit)
    return render_template('posts.html', posts=posts, park=park)


@park_crud.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        park_request = CreateParkRequest( name=data['name'],
                                          description=data['description'],
                                          image_id = 'hardcoded',
                                          user_id = data['user_id'],
                                          location = Location(lat=data['lat'], lng=data['lng'])
                                          )
        park = park_client.create(park_request)
        return redirect(url_for('.view_all_park'))

    return render_template('createpark.html')
