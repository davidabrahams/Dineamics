import urllib
import urllib2
import json
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


def filter_data(name, locality):
    response_data = get_menu(name, locality)

    prices = []
    key = 'price'
    if response_data != None:

        for entry in response_data:

            sections = entry['sections']

            for section in sections:

                subsections = section['subsections']

                for subsection in subsections:

                    contents = subsection['contents']

                    for content in contents:

                        if 'price' in content:

                            money = (content['price'].encode('utf-8'))

                            try:
                                money = float(money)
                                prices.append(money)
                            except ValueError:
                                #If the string can't be converted to a float, leave it the fuck alone
                                pass

    return prices


def get_price_of_mains(name, locality):

    prices = filter_data(name, locality)

    if prices != []:

        sorted_prices = sorted(prices, reverse=True)

        num = int(round(.25 * len(sorted_prices)))
        num1 = int(round(.5 * len(sorted_prices)))
        return round(sum(sorted_prices[num:num1]) / (num1 - num), 2)
    else:
        return None


if __name__ == '__main__':
    name = 'Neptune Oyster'
    locality = 'Boston'
    print get_price_of_mains(name, locality)

