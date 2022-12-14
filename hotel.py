class Hotel:
    def __init__(self, id, name, city_id, stars, rooms):
        self.id = int(id)
        self.name = name
        self.city_id = int(city_id)
        self.stars = int(stars)
        self.rooms = int(rooms)