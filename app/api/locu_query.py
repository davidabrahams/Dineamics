import urllib
import urllib2
import json
import numpy
from unidecode import unidecode

LOCU_BASE = 'http://api.locu.com/v1_0/venue/search/?'
API_KEY = 'f60f052cf5d0473b25022a62a73b107cf0db0aad'


def get_locu_url(name, locality):
    """
    :param name: The name of a restaurant
    :param locality: The town/city a restaurant is in (check locality documentation at https://dev.locu.com/documentation/v1/)
    :return: A url to query the locu api
    """
    return LOCU_BASE + urllib.urlencode([('name', unidecode(name)), ('locality', locality), ('api_key', API_KEY)])


def get_ID(name, locality):
    """
    :param name: The name of a restaurant
    :param locality: The town/city a restaurant is in (check locality documentation at https://dev.locu.com/documentation/v1/)
    :return: The business ID of the restaurant, or None if that restaurant is not found in the locality
    """

    url = get_locu_url(name, locality)

    f = urllib2.urlopen(url)

    response_text = f.read()
    response_data = json.loads(response_text)
    objects = response_data["objects"]

    if len(objects) == 0:
        return None
    else:
        return response_data["objects"][0]["resource_uri"]


def get_menu(name, locality):
    """

    :param name: The name of a restaurant
    :param locality: The town/city a restaurant is in (check locality documentation at https://dev.locu.com/documentation/v1/):
    :return: menu, a list of dicts
    """
    ID = get_ID(name, locality)
    if ID != None:
        url = 'http://api.locu.com' + ID + '?' + urllib.urlencode([('api_key', API_KEY)])

        f = urllib2.urlopen(url)
        response_text = f.read()
        response_data = json.loads(response_text)
        return response_data["objects"][0]["menus"]
    else:
        return None


def get_prices_from_menu(menu):
    """
    :param menu: a list of dicts returned by the get_menu(name, locality) function
    :return: a list of prices that appear on a restaurant's menu.
    """

    prices = []

    if menu != None:

        for entry in menu:
            for section in entry['sections']:
                for subsection in section['subsections']:
                    for content in subsection['contents']:
                        if 'price' in content:
                            money = (content['price'].encode('utf-8'))
                            try:
                                money = float(money)
                                prices.append(money)
                            except ValueError:
                                pass  # If the string can't be converted to a float, leave it alone

    return prices


def get_price_of_mains(menu):
    """
    :param menu: a Locu menu returned by get_menu(name, locality)
    :return: An approximation for the average price of a main course at the restaurant. Found by calculating the average of all the prices in the 50th-75th percentile by price of the restaurant's menu.
    """

    prices = get_prices_from_menu(menu)

    if len(prices) >= 4:

        sorted_prices = sorted(prices, reverse=True)

        num = int(round(.25 * len(sorted_prices)))
        num1 = int(round(.5 * len(sorted_prices)))
        try:
            return round(sum(sorted_prices[num:num1]) / (num1 - num), 2)
        except ZeroDivisionError:
            print 'Taking the average failed. The menu contained the following prices: ' + str(prices)
            return numpy.mean(prices)
    else:
        return numpy.mean(prices)


if __name__ == '__main__':
    name = 'Neptune Oyster'
    locality = 'Boston'
    print get_prices_from_menu(get_menu(name, locality))

