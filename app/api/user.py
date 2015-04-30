from collections import Counter

__author__ = 'davidabrahams'

import locu_database, restaurant, locu_setup, api, restaurant_attribute_parser, yelp_database
from unidecode import unidecode

LOCU_FILE_NAME = 'locu_database.txt'
YELP_FILE_NAME = 'yelp_database.txt'


class User(object):
    """
    A class representing a user, contains his search criterion, location, and price
    """

    def __init__(self, term, location, price_max):
        self.term = term.lower()
        self.location = location.lower()
        self.price_max = float(price_max)


    def __str__(self):
        return 'User looking for ' + self.term + ' in ' + self.location + ', paying up to $' + self.price_max + '.'

    def get_restaurants(self, yelp_database, locu_database):
        """Gets the top restaurants for a given User.
        Args:
            yelp_database (YelpDatabase): a YelpDatabase object
            locu_database (MenuDatabase): a MenuDatabase object
        Returns:
            restaurants (list): a list of Restaurant objects.
        """
        restaurants = []

        # Look for the query in the yelp_database, and if it is, load the response from the database
        if ((self.term, self.location)) in yelp_database.data:
                print 'Found ' + self.term + ' in Yelp database!'
                responses = yelp_database.data[(self.term, self.location)]
        # Otherwise, make a Yelp API query
        else:
            print 'Querying Yelp for ' + self.term + '...'
            responses = api.get_restaurant_responses(self.term, self.location)
            yelp_database.data[(self.term, self.location)] = responses

        # Each response in responses represents a restaurant. Create a Restaurant out of it.
        for i, response in enumerate(responses):
            name = restaurant_attribute_parser.get_name(response)
            address = restaurant_attribute_parser.get_address(response)
            locality = restaurant_attribute_parser.get_locality(response)
            categories = restaurant_attribute_parser.get_categories(response)
            image = restaurant_attribute_parser.get_image(response)
            unenc_name = restaurant_attribute_parser.get_name_nonenc(response)
            url = restaurant_attribute_parser.get_url(response)
            display_name = unidecode(unenc_name)

            # Look for the restaurant in the locu_database. If it is, load the menu from it
            if ((unenc_name, locality)) in locu_database.data:
                print 'Found ' + unenc_name + ' in Locu database!'
                menu = locu_database.data[(unenc_name, locality)]
            #Otherwise, make a Locu query for the menu
            else:
                print 'Querying Locu for ' + unenc_name + '...'
                menu = locu_setup.get_menu(unenc_name, locality)
                locu_database.data[(unenc_name, locality)] = menu

            # get the average price of mains from the Locu menu
            price = locu_setup.get_price_of_mains(menu)

            # create the restaurant object
            rest = restaurant.Restaurant(name, address, locality, categories, price, image, unenc_name, url, display_name)
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

def create_users(food_list, location_list, price_list):
    return [User(food, location, price) for food, location, price in zip(food_list, location_list, price_list)]



def average_price_location(users):
    """Returns the average price and most common location for a list of users.
    """
    price = []
    location = []
    for index, user in enumerate(users):    
        price.append(user.price_max)
        location.append(user.location)
    price = sum(price)/len(price)

    c = Counter(location)
    loc = c.most_common(1)[0]

    return price, loc

def get_users_restaurants(users):
    """Gets the top restaurants for a list of Users.
        Args:
            users (list): a list of users
        Returns:
            restaurant_lists (list): a list of lists of Restaurant objects.
        """
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