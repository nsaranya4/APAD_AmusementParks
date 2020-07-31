from flask import Blueprint, redirect, render_template, request, url_for, session
from ..clients.park_client import ParkClient
from ..representations.park import CreateParkRequest, Park
from ..representations.location import Location

park_crud = Blueprint('park', __name__)
park_client = ParkClient("http://127.0.0.1:5000")


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


@park_crud.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        park_request = CreateParkRequest()
        location = Location()
        park_request.name = data['name']
        park_request.description = data['description']
        park_request.image_id = 'hardcoded'
        park_request.user_id = data['user_id']
        # TODO:: check if lat lng exist
        park_request.location = Location(lat=data['lat'], lng=data[lng])
        park = park_client.create(park_request)
        return redirect(url_for('blog.index'))

    return render_template('createpark.html')
