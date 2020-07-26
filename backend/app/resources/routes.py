from .park import Park, Parks


def initialize_routes(api):
    api.add_resource(Park, '/funtech/v1/parks/<string:id>')
    api.add_resource(Parks, '/funtech/v1/parks')
