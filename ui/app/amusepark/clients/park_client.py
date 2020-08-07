import requests
from ..representations.park import CreateParkRequestSchema, ParkSchema


class ParkClient:
    def __init__(self, base_url):
        self.park_path = base_url + '/funtech/v1/parks'
        self.create_park_request_schema = CreateParkRequestSchema()
        self.park_schema = ParkSchema()
        self.parks_schema = ParkSchema(many=True)
        self.headers = {"Content-Type": "application/json", "Accept": "*/*"}

    def create(self, create_park_request):
        payload = self.create_park_request_schema.dump(create_park_request).data
        response = requests.post(self.park_path, json=payload, headers=self.headers)
        if response.status_code == 200:
            park = self.park_schema.load(response.json()).data
            return park, None
        else:
            return None, Exception("failed to create park")

    def get_by_id(self, id):
        response = requests.get(self.park_path + "/" + id)
        # TODO:: handle error codes
        park = self.park_schema.load(response.json()).data
        return park

    def get_batch(self, filters, offset, limit):
        pagination = {'offset': offset, 'limit': limit}
        params = {**filters, **pagination}
        response = requests.get(self.park_path, params=params)
        #TODO:: handle error codes
        posts = self.parks_schema.load(response.json()).data
        return posts
