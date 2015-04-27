"""
This module is used to return attributes from a restaurant obtained from a Yelp API query
"""

import locu_setup, api

TERM = 'mexican'
LOCATION = 'Boston, MA'


def get_name(response):
    return response["name"].encode('utf-8')


def get_name_nonenc(response):
    return response["name"]


def get_image(response):
    if "image_url" in response:
        return response["image_url"]
    else:
        return None

def get_url(response):
    return response["mobile_url"]

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
    cats = []
    if "categories" not in response:
        return []
    categories = response["categories"]
    for item in categories:
        # Each category is a list of different spellings of that category, ie ['Mexican', 'mexican']
        cats.append(item[0])
    return cats


def query_and_print_restaurant(TERM, LOCATION):
    """
    Makes an API Query using the TERM and LOCATION parameters. Then parses the response data and prints it. Also finds
    price information from Locu API query.
    """
    response = api.get_restaurant_response(TERM, LOCATION)

    print response

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


if __name__ == '__main__':
    query_and_print_restaurant(TERM, LOCATION)