from models.park import Park


class ParkRepo:

    def get_by_id(self, id: str):
        try:
            park = Park.objects.get(id=id)
            return park, None
        except Park.DoesNotExist:
            return None, None
        except Exception as e:
            return None, e
            
    def get_batch(self, offset: int, limit: int, filters: dict):
        park_list = Park.objects
        if filters.keys().__contains__('user_id'):
            park_list = park_list.filter(user=filters['user_id'])
        return park_list.order_by('-created_at').skip(offset).limit(limit)

    def create(self, park: Park):
        try:
            park = park.save()
            return park, None
        except Exception as e:
            return None, e

    def delete(self, park: Park):
        park.delete()
