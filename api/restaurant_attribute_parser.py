"""
This module is used to return attributes from a restaurant obtained from a Yelp API query
"""

import api
import locu_setup

TERM = 'mexican'
LOCATION = 'Boston, MA'


def get_name(response):
    return response["name"].encode('utf-8')


def get_name_nonenc(response):
    return response["name"]


def get_image(response):
    return response["image_url"]


def get_address(response):
    thing = []
    address = response["location"]["display_address"]
    for item in address:
        item = str(item)
        thing.append(item)
    return thing


def get_locality(response):
    locality = response["location"]["city"]
    return locality.encode('utf-8')


def get_categories(response):
    thing = []
    categories = response["categories"]
    for item in response["categories"]:
        thing.append(item)

    return thing


def query_and_print_restaurant(TERM, LOCATION):
    """
    Makes an API Query using the TERM and LOCATION parameters. Then parses the response data and prints it. Also finds
    price information from Locu API query.
    """
    response = api.get_restaurant(TERM, LOCATION)

    name = get_name(response)
    print get_image(response)

    address = get_address(response)
    categories = get_categories(response)
    print ""
    print name
    print ""
    print "The address of " + name + " is:"
    for i in address:
        print i
    print ""
    print name + " is in the following categories:"
    for i in categories:
        print i[0]
    print ""
    price = locu_setup.get_price_of_mains(get_name_nonenc(response), get_locality(response))
    if price != None:
        print "The average price per person at this restaurant is:"
        print price
    else:
        print "We're sorry! Price isn't available for this location."
        print "Check the website!"


if __name__ == '__main__':
    query_and_print_restaurant(TERM, LOCATION)