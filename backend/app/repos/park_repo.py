from models.park import Park


class ParkRepo:

    def get_by_id(self, id: str):
        return Park.objects.get(id=id)

    def get_batch(self, offset: int, limit: int, filters: dict):
        park_list = Park.objects
        if filters.keys().__contains__('user_id'):
            park_list = park_list.filter(user=filters['user_id'])
        return park_list.skip(offset).limit(limit)

    def create(self, park: Park):
        park = park.save()
        return park

    def delete(self, park: Park):
        park = Park.objects()
        park.delete()
        #return park

