from models.park import Park


class ParkRepo():

    def get_by_id(self, id: str):
        return Park.objects.get_or_404(id=id)

    def get_batch(self, offset: int, limit: int):
        # TODO figure out how to use pagination while querying mongodb
        park_list = Park.objects()
        return park_list

    def create(self, park: Park):
        park.save()
        return park
