from repos.park_repo import ParkRepo
from repos.user_repo import UserRepo
from models.park import Park
from models.location import Location
from representations.park import CreateParkRequest, ParkSchema
from resources.errors import BadRequestError
import time


class ParkService:
    def __init__(self, park_repo: ParkRepo, user_repo: UserRepo):
        self.park_repo = park_repo
        self.user_repo = user_repo
        self.park_schema = ParkSchema()
        self.parks_schema = ParkSchema(many=True)

    def create(self, create_park_request: CreateParkRequest):
        park = Park()
        user, error = self.user_repo.get_by_id(create_park_request.user_id)
        if user is not None and error is None:
            park.user = user
        else:
            return None, error
        
        location = Location()
        location.lat = create_park_request.location.lat
        location.lng = create_park_request.location.lng
        park.name = create_park_request.name
        park.description = create_park_request.description
        park.image_id = create_park_request.image_id
        park.location = location
        park.created_at = time.time_ns()
        park, error = self.park_repo.create(park)
        if park is not None and error is None:
            return self.park_schema.dump(park).data, None
        else: 
            return None, error

    def get_batch(self, offset: int, limit: int, filters: dict):
        parks = self.park_repo.get_batch(offset, limit, filters)
        return self.parks_schema.dump(parks).data

    def get_by_id(self, id):
        park, error = self.park_repo.get_by_id(id)
        if park is not None and error is None:
            return self.park_schema.dump(park).data, None
        else:
            return None, error

    def delete_by_id(self, id):
        park, error = self.park_repo.get_by_id(id)
        if park is not None and error is None:
            return self.park_repo.delete(park), None
        elif park is None and error is not None:
            return None, BadRequestError
        else:
            return None, error
