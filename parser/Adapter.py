class Adapter:
    
    def __init__(self, name: str, price_now: str, price_old: str, brand: str, made_in: str, expiration_date: str,
                 weight: str):
        self.name = name
        self.price_now = price_now
        self.price_old = price_old
        self.brand = brand
        self.made_in = made_in
        self.expiration_date = expiration_date
        self.weight = weight


    def __eq__(self, other):
        return isinstance(other, Adapter) and self.name == other.name


    def __hash__(self):
        return hash(self.name)
