class Tour:
    def __init__(self, id, hotel_id, people, days, food, transport, price):
        self.id = int(id)
        self.hotel_id = int(hotel_id)
        self.people= int(people)
        self.days = int(days)
        self.food = int(food)
        self.transport = transport
        self.price = float(price)