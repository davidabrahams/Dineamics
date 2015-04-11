__author__ = 'davidabrahams'


class Restaurant:
    def __init__(self, name, address, locality, categories, price):
        self.name = name
        self.address = address
        self.locality = locality
        self.categories = categories
        self.price = price

    def __str__(self):
        return self.name + ', ' + self.locality

    def equals(self, other):
        return self.name == other.name and self.locality == other.locality

    def get_duplicate(self, rests):
        for rest in rests:
            if self.equals(rest):
                return rest
        return None
