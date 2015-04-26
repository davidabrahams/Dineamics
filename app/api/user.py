__author__ = 'davidabrahams'

from app.api import locu_database, restaurant, locu_setup, api, restaurant_attribute_parser, yelp_database

LOCU_FILE_NAME = 'locu_database.txt'
YELP_FILE_NAME = 'yelp_database.txt'


class User(object):
    """
    A class representing a user, contains his search criterion, location, and price
    """

    def __init__(self, term, location, price_max):
        self.term = term
        self.location = location
        self.price_max = price_max


    def __str__(self):
        return 'User looking for ' + self.term + ' in ' + self.location + ', paying up to $' + self.price_max + '.'

    def get_restaurants(self, yelp_database, database):
        restaurants = []
        
        if ((self.term, self.location)) in yelp_database.data:
                print 'Found ' + self.term + ' in Yelp database!'
                responses = yelp_database.data[(self.term, self.location)]
        else:
            print 'Querying Yelp for ' + self.term + '...'
            responses = api.get_restaurant_responses(self.term, self.location)
            yelp_database.data[(self.term, self.location)] = responses

        for i, response in enumerate(responses):
            name = restaurant_attribute_parser.get_name(response)
            address = restaurant_attribute_parser.get_address(response)
            locality = restaurant_attribute_parser.get_locality(response)
            categories = restaurant_attribute_parser.get_categories(response)
            image = restaurant_attribute_parser.get_image(response)
            unenc_name = restaurant_attribute_parser.get_name_nonenc(response)

            if ((unenc_name, locality)) in database.data:
                print 'Found ' + unenc_name + ' in Locu database!'
                menu = database.data[(unenc_name, locality)]
            else:
                print 'Querying Locu for ' + unenc_name + '...'
                menu = locu_setup.get_menu(unenc_name, locality)
                database.data[(unenc_name, locality)] = menu

            price = locu_setup.get_price_of_mains(menu)

            rest = restaurant.Restaurant(name, address, locality, categories, price, image, unenc_name)
            restaurants.append(rest)
        return restaurants


def create_user():

    term = raw_input("What would you like to eat? --> ")
    location = raw_input("Where are you? --> ")
    price_max = raw_input("How much are you willing to pay? --> ")

    return User(term, location, price_max)

def create_users():
    add_another = True
    users = []
    index = 0
    while add_another:
        print 'Creating user #' + str(index +1)
        user = create_user()
        users.append(user)
        input = raw_input("Would you like to add another user (Y/N)? --> ")
        add_another = input.upper() == 'Y'
        index += 1
        print

    return users

def average_price_location(users):
    price = []
    location = []
    for index, user in enumerate(users):    
        price.append(int(user.price_max))
        location.append(user.location)
    price = sum(price)/len(price)

    return price, location[0]

def get_users_restaurants(users):
    restaurant_lists = []
    
    print 'Loading database...'
    print

    """

    connection = MySQLdb.connect('127.0.0.1', 'testuser', 'test123', 'testdb')
    cursor = connection.cursor()
    cursor.execute("SELECT features FROM Locu WHERE card = 'testCard')

    """

    l_database = locu_database.load(LOCU_FILE_NAME)
    y_database = yelp_database.load(YELP_FILE_NAME)


    for index, user in enumerate(users):
        restaurants = user.get_restaurants(y_database, l_database)
        restaurant_lists.append(restaurants)
        print
    print 'Saving database...'
    print
    l_database.save(LOCU_FILE_NAME)
    y_database.save(YELP_FILE_NAME)
    return restaurant_lists

if __name__ == '__main__':
    for list in get_users_restaurants(create_users()):
        for r in list:
            print r