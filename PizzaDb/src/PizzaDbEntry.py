class PizzaDbEntry:
    def __init__(self,
                 id=1,
                 item='Item',
                 price='Price',
                 type='Type',
                 status='In stock'):
        self.id = id
        self.item = item
        self.price = price
        self.type = type
        self.status = status
