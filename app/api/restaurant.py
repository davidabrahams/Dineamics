__author__ = 'davidabrahams'


class Restaurant(object):
    def __init__(self, name, address, locality, categories, price, image, unencoded_name, url):
        self.name = name
        self.address = address
        self.locality = locality
        self.categories = categories
        self.price = price
        self.image = image
        self.unencoded_name = unencoded_name
        self.url = url

    def __str__(self):
        return self.name + ', ' + self.locality + ', ' + self.image

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __key(self):
        return (self.name, self.locality)

    def __hash__(self):
        return hash(self.__key())

    def get_duplicate(self, rests):
        for rest in rests:
            if self.equals(rest):
                return rest
        return None
